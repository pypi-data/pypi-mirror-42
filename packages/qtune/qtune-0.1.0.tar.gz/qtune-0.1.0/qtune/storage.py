import warnings
import copy
import itertools
import logging

import threading
import queue
import multiprocessing

from typing import Union, Iterable, Generator

import h5py
import numpy as np
import pandas as pd

from qtune.util import time_string, get_version


__all__ = ["serializables", "HDF5Serializable", 'from_hdf5', 'AsynchronousHDF5Writer']


serializables = dict()


def _get_dtype(arr):
    if arr.dtype == 'O':
        if all(isinstance(t, str) for t in arr.ravel()):
            return h5py.special_dtype(vlen=str)
    return arr.dtype


def _import_all():
    import qtune.autotuner
    import qtune.evaluator
    import qtune.experiment
    import qtune.gradient
    import qtune.solver


class HDF5Serializable(type):
    """
    Metaclass for all serializable object. Serializable means that the class can be reloaded from memory.
    """
    def __new__(mcs, name, bases, attrs):
        if name in serializables:
            warnings.warn("Overwriting known serializable {}".format(name))
        cls = type.__new__(mcs, name, bases, attrs)

        serializables[name] = cls
        return cls

    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        if 'to_hdf5' not in cls.__dict__:
            raise AttributeError('Missing method: "to_hdf5" that should return all constructor arguments', name)


def _to_hdf5(hdf5_parent_group: h5py.Group, name, obj, serialized):
    """
    Serializes a class instance
    :param hdf5_parent_group: Storage group in the HDF5 library.
    :param name:
    :param obj:
    :param serialized: Serialized objects. Required to verify that the object has not been saved yet.
    :return: None
    """
    if id(obj) in serialized:
        hdf5_parent_group.create_dataset(name, data=serialized[id(obj)].ref)
        return

    if isinstance(obj, dict):
        hdf5_group = hdf5_parent_group.create_group(name)
        hdf5_group.attrs['#type'] = 'dict'
        for key, value in obj.items():
            _to_hdf5(hdf5_group, key, value, serialized)
        serialized[id(obj)] = hdf5_group
        return

    if isinstance(obj, (list, tuple)):
        hdf5_group = hdf5_parent_group.create_group(name)
        hdf5_group.attrs['#type'] = 'list' if isinstance(obj, list) else 'tuple'
        for idx, value in enumerate(obj):
            _to_hdf5(hdf5_group, str(idx), value, serialized)
        serialized[id(obj)] = hdf5_group
        return

    if type(obj).__name__ in serializables:
        hdf5_group = hdf5_parent_group.create_group(name)
        hdf5_group.attrs['#type'] = type(obj).__name__

        serialized[id(obj)] = hdf5_group

        data = obj.to_hdf5()
        for key, value in data.items():
            _to_hdf5(hdf5_group, key, value, serialized)
        return

    if isinstance(obj, pd.DataFrame):
        dset = hdf5_parent_group.create_dataset(name, data=obj)
        dset.attrs.create('index', data=obj.index, dtype=_get_dtype(obj.index))
        dset.attrs.create('columns', data=obj.columns, dtype=_get_dtype(obj.columns))
        dset.attrs['#type'] = 'DataFrame'

        serialized[id(obj)] = dset
        return

    if isinstance(obj, pd.Series):
        dset = hdf5_parent_group.create_dataset(name, data=obj, dtype=_get_dtype(obj))
        dset.attrs.create('index', data=obj.index, dtype=_get_dtype(obj.index))
        dset.attrs['#type'] = 'Series'

        serialized[id(obj)] = dset
        return

    if isinstance(obj, np.ndarray):
        dset = hdf5_parent_group.create_dataset(name, data=obj)
        serialized[id(obj)] = dset
        return

    if isinstance(obj, (float, int, complex, bool, np.generic)):
        hdf5_parent_group.create_dataset(name, data=obj, shape=())
        return

    if isinstance(obj, str):
        dt = h5py.special_dtype(vlen=str)
        dset = hdf5_parent_group.create_dataset(name, data=obj, dtype=dt)
        dset.attrs['#type'] = 'str'
        serialized[id(obj)] = dset
        return

    if obj is None:
        dset = hdf5_parent_group.create_dataset(name, dtype="f")
        dset.attrs['#type'] = 'NoneType'
        serialized[id(obj)] = dset
        return

    raise RuntimeError()


def to_hdf5(filename_or_handle: Union[str, h5py.Group], name: str, obj,
            reserved=None):
    if isinstance(filename_or_handle, h5py.Group):
        root = filename_or_handle
    else:
        root = h5py.File(filename_or_handle, mode='a')

    if '#version' not in root:
        root.attrs['#version'] = get_version()

    if not reserved:
        reserved = dict()

    serialized = dict()

    for key, value in reserved.items():
        dset = root.create_dataset(name=key, dtype='f')
        serialized[id(value)] = dset
        dset.attrs["#type"] = "#reserved"

    _to_hdf5(root, name, obj, serialized)


def _from_hdf5(root: h5py.File, hdf5_obj: h5py.HLObject, deserialized=None):
    """
    Reloads a saved object.
    :param root: Root file of the HDF5 library
    :param hdf5_obj: Object to be reloaded
    :param deserialized: Already loaded objects.
    :return: The reloaded object.
    """
    if isinstance(hdf5_obj, h5py.Reference):
        hdf5_obj = root[hdf5_obj]

    if hdf5_obj.id in deserialized:
        return deserialized[hdf5_obj.id]

    if isinstance(hdf5_obj, h5py.Group):
        if '#type' not in hdf5_obj.attrs or hdf5_obj.attrs['#type'] == 'dict':
            deserialized[hdf5_obj.id] = dict()
            result = deserialized[hdf5_obj.id]

            for k in hdf5_obj.keys():
                result[k] = _from_hdf5(root, hdf5_obj[k], deserialized)
            return result

        elif hdf5_obj.attrs['#type'] in serializables:
            cls = serializables[hdf5_obj.attrs['#type']]
            kwargs = {k: _from_hdf5(root, v, deserialized)
                      for k, v in hdf5_obj.items()}

            try:
                deserialized[hdf5_obj.id] = cls(**kwargs)
            except ValueError:
                import logging
                logging.getLogger().error(hdf5_obj.name)
                import pickle
                with open(r'D:\temp.txt', 'wb') as f:
                    pickle.dump(kwargs, f)
                logging.getLogger().error(kwargs)

                raise
            return deserialized[hdf5_obj.id]

        elif hdf5_obj.attrs['#type'] == 'list':
            deserialized[hdf5_obj.id] = list()
            result = deserialized[hdf5_obj.id]

            for idx in range(len(hdf5_obj.keys())):
                result.append(_from_hdf5(root, hdf5_obj[str(idx)], deserialized))
            return result

        elif hdf5_obj.attrs['#type'] == 'tuple':
            result = []
            for idx in range(len(hdf5_obj.keys())):
                result.append(_from_hdf5(root, hdf5_obj[str(idx)], deserialized))
            result = tuple(result)
            deserialized[hdf5_obj.id] = result
            return result

        else:
            warnings.warn('Unknown type: {}'.format(hdf5_obj.attrs['#type']))

    elif isinstance(hdf5_obj, h5py.Dataset):
        if '#type' in hdf5_obj.attrs:
            if hdf5_obj.attrs['#type'] == 'DataFrame':
                idx = hdf5_obj.attrs['index']
                col = hdf5_obj.attrs['columns']
                result = pd.DataFrame(data=np.asarray(hdf5_obj), index=idx, columns=col)
                deserialized[hdf5_obj.id] = result
                return result

            if hdf5_obj.attrs['#type'] == 'Series':
                idx = hdf5_obj.attrs['index']
                result = pd.Series(data=np.asarray(hdf5_obj), index=idx)
                deserialized[hdf5_obj.id] = result
                return result

            if hdf5_obj.attrs['#type'] == 'str':
                result = str(np.asarray(hdf5_obj))
                deserialized[hdf5_obj.id] = result
                return result

            if hdf5_obj.attrs['#type'] == 'NoneType':
                return None

        result = np.asarray(hdf5_obj)
        if result.shape == ():
            result = result[()]
        if isinstance(result, h5py.Reference):
            return _from_hdf5(root, result, deserialized)
        else:
            return result

    else:
        raise RuntimeError()


def from_hdf5(filename_or_handle, reserved):
    """
    Reload an HDF5 file.
    :param filename_or_handle:
    :param reserved: Reserved elements are those which are already reloaded or have to be created during the run time.
    :return: Loaded object.
    """
    _import_all()

    if isinstance(filename_or_handle, h5py.Group):
        root = filename_or_handle
    else:
        root = h5py.File(filename_or_handle, mode='r')

    deserialized = dict()

    for key, value in root.items():
        if "#type" in value.attrs and value.attrs["#type"] == "#reserved":
            deserialized[value.id] = reserved[key]

    return _from_hdf5(root, root, deserialized)


def _writer_target(write_queue: Union[multiprocessing.JoinableQueue, queue.Queue], logger='qtune'):
    while True:
        task = write_queue.get()
        try:
            if task is None:
                return
            else:
                name, file_name, obj, reserved = task

            try:
                to_hdf5(file_name, name, obj, reserved=reserved)
            except:
                logging.getLogger(logger).exception('Error while writing "%s"' % file_name)
                raise
        finally:
            write_queue.task_done()


class AsynchronousHDF5Writer:
    """
    The asynchronous writer can improve the performance by writing in separate threads.
    """
    def __init__(self, reserved, multiprocess=True):
        reserved = reserved.copy()

        self.reserved = reserved

        if multiprocess:
            self.QueueType = multiprocessing.JoinableQueue
            self.WorkerType = multiprocessing.Process
        else:
            self.QueueType = queue.Queue
            self.WorkerType = threading.Thread

        self._worker = None
        self._queue = None

        self._initialize()

    def _initialize(self):
        self._queue = self.QueueType()
        self._worker = self.WorkerType(target=_writer_target, args=(self._queue,))
        self._worker.start()

    def restart(self):
        self.join()

        self._initialize()

    def join(self):
        """Stop writing and join thread."""
        if self._worker.is_alive():
            self._queue.put(None)
            self._queue.join()

        elif self._queue.qsize():
            warnings.warn("Storage queue contains data but the writer worker is already dead.")

        self._worker.join()

    def __del__(self):
        self.join()

    def write(self, obj, file_name, name=None):
        if not self._worker.is_alive():
            raise RuntimeError('Writer already stopped')

        if name is None:
            name = time_string()

        obj, reserved = copy.deepcopy((obj, self.reserved))

        self._queue.put((name, file_name, obj, reserved))


class ParallelHDF5Reader:
    """
    The parallel reader can improve the performance by reading in separate threads.
    """
    def __init__(self, reserved, multiprocess=True, max_workers=None):
        import concurrent.futures
        if multiprocess:
            Executor = concurrent.futures.ProcessPoolExecutor
        else:
            Executor = concurrent.futures.ThreadPoolExecutor

        self._executor = Executor(max_workers=max_workers)
        self.reserved = reserved

    def read_iter(self, file_names: Iterable[str]) -> Generator:
        yield from self._executor.map(from_hdf5, file_names, itertools.repeat(self.reserved), chunksize=1)

    def shutdown(self):
        self._executor.shutdown()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def __del__(self):
        self.shutdown()

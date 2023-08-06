import os
import operator
import re
from typing import Optional, Set, Dict, Sequence, Tuple, List

import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axes
import logging

import qtune.storage
import qtune.autotuner
import qtune.solver
import qtune.gradient
import qtune.parameter_tuner
import qtune.util
import qtune.evaluator


parameter_information = {
    "origin x": {
        "entity_unit": "Transition Position Lead A (V)",
        "name": "Transition Position Lead A",
        "gradient_unit": "Gradient Transition Lead A (V/V)"
    },
    "origin y": {
        "entity_unit": "Transition Position Lead B (V)",
        "name": "Transition Position Lead B",
        "gradient_unit": "Gradient Transition Lead B (V/V)"
    },
    "tunnel_coupling": {
        "entity_unit": "Transition Position Lead B (V)",
        "name": "Transition Position Lead B",
        "gradient_unit": "Gradient Transition Lead B (V/V)"
    },
    "lead time": {
        "entity_unit": "Transition Position Lead B (V)",
        "name": "Transition Position Lead B",
        "gradient_unit": "Gradient Transition Lead B (V/V)"
    },
    "position_RFA": {
        "entity_unit": "Transition Position Lead A (V)",
        "name": "Transition Position Lead A",
        "gradient_unit": "Gradient Transition Lead A (V/V)"
    },
    "position_RFB": {
        "entity_unit": "Transition Position Lead B (V)",
        "name": "Transition Position Lead B",
        "gradient_unit": "Gradient Transition Lead B (V/V)"
    },
    "parameter_tunnel_coupling": {
        "entity_unit": "Tunnel Coupling (\mu V)",
        "name": "Inter-Dot Tunnel Coupling AB",
        "gradient_unit": "Gradient Tunnel Coupling (\mu V / V)"
    },
    "current_signal": {
        "entity_unit": "Signal (a.u.)",
        "name": "Current SDot Signal",
        "gradient_unit": "Gradient Current SDot Signal (a.u.)"
    },
    "optimal_signal": {
        "entity_unit": "Signal (a.u.)",
        "name": "Optimal SDot Signal",
        "gradient_unit": "Gradient Optimal SDot Signal (a.u.)"
    },
    "position_SDB2": {
        "entity_unit": "Voltage (V)",
        "name": "Voltage on SDB2",
        "gradient_unit": "Gradient Voltage on SDB2 (V/V)"
    },
    "position_SDB1": {
        "entity_unit": "Voltage (V)",
        "name": "Voltage on SDB1",
        "gradient_unit": "Gradient Voltage on SDB1 (V/V)"
    },
    "parameter_time_load": {
        "entity_unit": "Time (ns)",
        "name": "Singlet Reload Time",
        "gradient_unit": "Gradient Singlet Reload Time(ns/V)"
    }
}


def read_files(file_or_files, reserved=None):
    if isinstance(file_or_files, str):
        files = [file_or_files]
    else:
        files = list(file_or_files)

    data = []

    for file_name in files:
        with h5py.File(file_name, 'r') as root:
            entries = [key for key in root.keys() if not key.startswith('#')]

            for entry in entries:
                entry_data = qtune.storage.from_hdf5(root[entry], reserved)

                data.append((entry, entry_data))

    return data.sort(key=operator.itemgetter(0))


class History:
    """
    Saves all relevant information of the Autotuner.
    """
    _parameter_variance_name = '{parameter_name}#var'
    _gradient_name = '{parameter_name}#{gate_name}#grad'
    _gradient_covariance_name = '{parameter_name}#{gate_name_1}#{gate_name_2}#cov'

    def __init__(self, directory_or_file: Optional[str], experiment: Optional=None):
        """
        Initialize the history by loading an HDF5 library or a single entry from a library or starting a new history.
        :param directory_or_file: Directory of the HDF5 library if the whole library shall be reloaded. Single
        file of the library if only one entry in the library shall be loaded. None if a new history shall be
        initialized.
        :param experiment: Experiment corresponding to the Autotuner. Can be None.
        """
        self._data_frame = pd.DataFrame()
        self._gate_names = set()
        self._parameter_names = set()
        self._gradient_controlled_parameters = dict()
        self._evaluator_data = pd.DataFrame()
        self._evaluator_names = []
        self.experiment = experiment
        self._logger = 'qtune'
        self._paths_for_reload = []
        if directory_or_file is None:
            pass
        elif os.path.isdir(directory_or_file):
            self.load_directory(directory_or_file)
        elif os.path.isfile(directory_or_file):
            self.load_file(directory_or_file)
        else:
            raise RuntimeWarning("The directory of file used to instantiate the qtune.history.History object could not"
                                 "be identified as such. An empty History object is instantiated.")

    @property
    def logger(self):
        return logging.getLogger(self._logger)

    @property
    def gate_names(self) -> Set[str]:
        return self._gate_names

    @property
    def parameter_names(self) -> Set[str]:
        return self._parameter_names

    @property
    def gradient_controlled_parameter_names(self) -> Dict[str, Set[str]]:
        return self._gradient_controlled_parameters

    @property
    def evaluator_names(self):
        return self._evaluator_data.columns

    @property
    def mode_options(self):
        return ["all_voltages", "all_parameters", "all_gradients", "with_grad_covariances", "with_par_variances"]

    @property
    def evaluator_data(self):
        return self._evaluator_data[list(self.evaluator_names)]

    @property
    def number_of_stored_iterations(self):
        return self._data_frame.index.size

    def get_reload_path(self, i):
        return self._paths_for_reload[i]

    def get_evaluator_data(self, evaluator_names=None):
        if evaluator_names is None:
            evaluator_names = self.evaluator_names
        return self._evaluator_data[evaluator_names]

    def get_parameter_values(self, parameter_name) -> pd.Series:
        return self._data_frame[parameter_name]

    def get_parameter_std(self, parameter_name) -> pd.Series:
        return self._data_frame[self._parameter_variance_name.format(parameter_name=parameter_name)].apply(np.sqrt)

    def get_gate_values(self, gate_name) -> pd.Series:
        return self._data_frame[gate_name]

    def get_gradients(self, parameter_name: str) -> pd.DataFrame:
        """
        History of a gradient.
        :param parameter_name: Parameter of the gradient of interest.
        :return: Gradient history.
        """
        regex = re.compile(self._gradient_name.format(parameter_name=parameter_name,
                                                      gate_name=r'([\w\s\d]+)'))
        return self._data_frame.filter(regex=regex).rename(lambda name: regex.findall(name)[0], axis='columns')

    def get_gradient_covariances(self, parameter_name) -> pd.DataFrame:
        """
        History of a gradients covariance.
        :param parameter_name: Parameter of the gradient's covariance of interest.
        :return: Gradient covariance history.
        """
        regex = re.compile(self._gradient_covariance_name.format(parameter_name=parameter_name,
                                                                 gate_name_1=r'([\w\s\d]+)',
                                                                 gate_name_2=r'([\w\s\d]+)'))
        df = self._data_frame.filter(regex=regex)
        df = df[sorted(df.columns, key=regex.findall)]

        return pd.DataFrame(df, columns=pd.MultiIndex.from_tuples(map(regex.findall, df.columns)))

    def get_gradient_variances(self, parameter_name) -> pd.DataFrame:
        """
        History of the diagonal of a gradient's covariance.
        :param parameter_name: Parameter of the gradient's covariance of interest.
        :return: History of the diagonal of the covariance matrix.
        """
        regex = re.compile(self._gradient_covariance_name.format(parameter_name=parameter_name,
                                                                 gate_name_1=r'(?P<gatename>[\w\s\d]+)',
                                                                 gate_name_2=r'(?P=gatename)'))
        return self._data_frame.filter(regex=regex).rename(columns=lambda name: regex.search(name).group('gatename'))

    def read_autotuner_to_data_frame(self, autotuner: qtune.autotuner.Autotuner, start: int = 0,
                                     end: Optional[int] = None) -> pd.DataFrame:
        """
        Reads all relevant information of an Autotuner instance into a pandas DataFrame.
        :param autotuner:
        :param start: Start of the index in the History.
        :param end:  End of the index in the History.
        :return: Dataframe of the voltages, parameters, variances, gradients, gradient's covariances and the tuner index
        """
        if end is None:
            end = len(autotuner.tuning_hierarchy)
        elif end == 0:
            voltages = extract_voltages_from_hierarchy(autotuner.tuning_hierarchy)
            return pd.DataFrame(dict(voltages), index=[0, ])

        if self._data_frame.empty:
            voltages = extract_voltages_from_hierarchy(autotuner.tuning_hierarchy)
            self._gate_names = set(voltages.index)
            parameters, variances = extract_parameters_from_hierarchy(autotuner.tuning_hierarchy)
            self._parameter_names = set(parameters.index)
            gradients, grad_covariances = extract_gradients_from_hierarchy(autotuner.tuning_hierarchy)
            self._gradient_controlled_parameters = {parameter_name: set(gradient.index) or set()
                                                    for parameter_name, gradient in gradients.items()}
        else:
            relevant_hierarchy = autotuner.tuning_hierarchy[int(start):end]
            voltages = extract_voltages_from_hierarchy(autotuner.tuning_hierarchy)
            # voltages are extracted from the first and therefore most updated partuner
            parameters, variances = extract_parameters_from_hierarchy(relevant_hierarchy)
            gradients, grad_covariances = extract_gradients_from_hierarchy(relevant_hierarchy)

        voltages = dict(voltages)
        parameters = dict(parameters)
        variances = {self._parameter_variance_name.format(parameter_name=par_name): variance
                     for par_name, variance in variances.items()}
        gradients = {self._gradient_name.format(parameter_name=par_name, gate_name=gate_name): grad_entry
                     for par_name, gradient in gradients.items()
                     for gate_name, grad_entry in gradient.items()}
        grad_covariances = {k: v
                            for parameter_name, gradient_covariance_matrix in grad_covariances.items()
                            for k, v in self._unravel_gradient_covariance_matrix(parameter_name,
                                                                                 gradient_covariance_matrix).items()}
        tuner_index = {"tuner_index": autotuner.current_tuner_index}

        return pd.DataFrame({**voltages, **parameters, **variances, **gradients, **grad_covariances,
                             **tuner_index}, index=[0, ], dtype=float)

    def append_autotuner(self, autotuner: qtune.autotuner.Autotuner, path = None):
        """
        Appends an Autotuner instance to the History.
        :param autotuner:
        :return: None
        """
        if path is None:
            path = autotuner.last_save_file

        voltages = extract_voltages_from_hierarchy(autotuner.tuning_hierarchy).sort_index()
        evaluated_tuner_index = autotuner.current_tuner_index
        if autotuner.voltages_to_set is not None or autotuner.current_tuner_status:
            evaluated_tuner_index += 1

        if self._data_frame.empty:
            self._paths_for_reload.append(path)
            new_information = self.read_autotuner_to_data_frame(autotuner)
            self._data_frame = self._data_frame.append(new_information, ignore_index=True, sort=True)
            new_evaluator_data = read_evaluator_data_from_autotuner(autotuner)
            for evaluator_name in new_evaluator_data.columns:
                if new_evaluator_data.loc[new_evaluator_data.index[0], evaluator_name]['raw_y_data'] is None:
                    new_evaluator_data.loc[new_evaluator_data.index[0], evaluator_name] = np.nan
            self._evaluator_data = self._evaluator_data.append(new_evaluator_data, ignore_index=True, sort=True)
        if voltages.equals(self._data_frame[sorted(self.gate_names)].iloc[-1]):
            # stay in the row
            self._paths_for_reload[-1] = path
            start = self._data_frame['tuner_index'].iloc[-1]
            new_information = self.read_autotuner_to_data_frame(autotuner, start=start, end=evaluated_tuner_index)
            self._data_frame.loc[self._data_frame.index[-1], new_information.columns] = new_information.iloc[0]
            new_evaluator_data = read_evaluator_data_from_autotuner(autotuner, start=start, end=evaluated_tuner_index)
            if not new_evaluator_data.empty:
                self._evaluator_data.loc[self._evaluator_data.index[-1], new_evaluator_data.columns] = \
                    new_evaluator_data.iloc[0]
        else:
            self._paths_for_reload.append(path)
            new_information = self.read_autotuner_to_data_frame(autotuner, end=evaluated_tuner_index)
            self._data_frame = self._data_frame.append(new_information, ignore_index=True, sort=True)
            new_evaluator_data = read_evaluator_data_from_autotuner(autotuner, end=evaluated_tuner_index)
            self._evaluator_data = self._evaluator_data.append(new_evaluator_data, ignore_index=True, sort=True)

    def load_directory(self, path):
        """
        Loads an HDF5 library.
        :param path: Path of the library.
        :return: None
        """
        with qtune.storage.ParallelHDF5Reader(reserved={'experiment': self.experiment}, multiprocess=False) as reader:
            directory_content = [os.path.join(path, file)
                                 for file in sorted(os.listdir(path))]
            for file, loaded_data in zip(directory_content, reader.read_iter(directory_content)):
                autotuner = loaded_data['autotuner']
                self.append_autotuner(autotuner, file)

    def load_file(self, path):
        """
        Loads an entry of an HDF5 library.
        :param path: Path of the library.
        :return: None
        """
        hdf5_handle = h5py.File(path, mode="r")
        loaded_data = qtune.storage.from_hdf5(hdf5_handle, reserved={"experiment": self.experiment})
        autotuner = loaded_data["autotuner"]
        self.append_autotuner(autotuner=autotuner, path=path)

    def plot_tuning(self, voltage_indices=None, parameter_names=None, gradient_parameter_names=None, mode=""):
        """
        Plots the History
        :param voltage_indices: Indices of the voltages to be plotted.
        :param parameter_names: Names of the parameters to be plotted.
        :param gradient_parameter_names: Names of the parameters who's gradients shall be plotted.
        :param mode: Possible modes are:
        all_voltages: plot all voltages
        all_parameters: plot all parameters
        all_gradients: plot all gradients
        with_grad_covariances: plot the diagonal elements of the covariance matrix as error bars on the gradients.
        with_par_variences: plot the errors on the parameters.
        :return: List of figures, List of Axes
        """
        if "all_voltages" in mode:
            voltage_indices = sorted(self.gate_names)
        if "all_parameters" in mode:
            parameter_names = sorted(self.parameter_names)
        if "all_gradients" in mode:
            gradient_parameter_names = sorted(self.gradient_controlled_parameter_names)
        if "with_grad_covariances" in mode:
            with_grad_covariances = True
        else:
            with_grad_covariances = False
        if "with_par_variances" in mode:
            with_par_variances = True
        else:
            with_par_variances = False

        if voltage_indices is None:
            voltage_fig = None
            voltage_ax = None
        else:
            voltage_fig, voltage_ax = plot_voltages(self._data_frame[voltage_indices])

        if parameter_names is None:
            parameter_fig = None
            parameter_ax = None
        else:
            if with_par_variances:
                parameter_std = pd.DataFrame({par_name: self.get_parameter_std(parameter_name=par_name)
                                              for par_name in parameter_names})
            else:
                parameter_std = None
            parameter_fig, parameter_ax = plot_parameters(self._data_frame[parameter_names], parameter_std)

        if gradient_parameter_names is None:
            gradient_fig = None
            gradient_ax = None
        else:
            gradients = {par_name: self.get_gradients(parameter_name=par_name)
                         for par_name in gradient_parameter_names}
            if with_grad_covariances:
                gradient_variances = {par_name: self.get_gradient_variances(parameter_name=par_name)
                                      for par_name in gradient_parameter_names}
            else:
                gradient_variances = None
            gradient_fig, gradient_ax = plot_gradients(gradients, gradient_variances)

        return [voltage_fig, parameter_fig, gradient_fig], [voltage_ax, parameter_ax, gradient_ax]

    def plot_evaluator_data(self, start: int=0, end: Optional[int]=None, evaluator_names: Sequence[str]=None):
        """
        Plots the raw data of evaluators.
        :param start: Start index in the History.
        :param end: End index in the History.
        :param evaluator_names: Names of the evaluator to be plotted.
        :return: Figure, Axes
        """
        for name in evaluator_names:
            if name not in self._evaluator_data.columns:
                self.logger.warning(name + ' is not in the evaluation data.')
                evaluator_names.remove(name)

        if end is None:
            end = start + 1
        eval_data_figs = []
        eval_data_axs = []
        for i in range(start, end):
            if i not in self._evaluator_data.index:
                raise RuntimeError('These indices are not in the aquired data!')
            number_measurements = [
                len(self._evaluator_data.loc[self._evaluator_data.index[i], evaluator]['measurements'])
                for evaluator in evaluator_names
                if not self._evaluator_data.loc[self._evaluator_data.index[i], evaluator] != self._evaluator_data.loc[
                    self._evaluator_data.index[i], evaluator]]
            relevant_evaluators = [
                evaluator
                for evaluator in evaluator_names
                if not self._evaluator_data.loc[self._evaluator_data.index[i], evaluator] != self._evaluator_data.loc[
                    self._evaluator_data.index[i], evaluator]]
            eval_data_fig, eval_data_ax = plt.subplots(nrows=2,
                                                       ncols=sum(number_measurements) // 2 + sum(
                                                           number_measurements) % 2)
            eval_data_figs.append(eval_data_fig)
            eval_data_axs.append(eval_data_ax)
            ax_list = [eval_data_ax.ravel()[sum(number_measurements[0:j]):sum(number_measurements[0:j + 1])] for j in
                       range(len(number_measurements))]
            for evaluator, axs in zip(relevant_evaluators, ax_list):
                plot_data = self._evaluator_data.loc[self._evaluator_data.index[i], evaluator]
                if not plot_data != plot_data:
                    plot_function_matching[evaluator](ax=axs, evaluator_hdf5=plot_data, evaluator=evaluator)
                    for ax in axs:
                        ax.set_title(evaluator)
            eval_data_fig.tight_layout()
        return eval_data_figs, eval_data_axs

    def plot_single_evaluator_data(self, ax, evaluator_name, tune_run_number=0):
        if evaluator_name not in self.evaluator_names:
            self.logger.warning(evaluator_name + ' is not in the evaluation data.')
            return
        plot_data = self._evaluator_data.loc[self._evaluator_data.index[tune_run_number], evaluator_name]
        plot_function_matching[evaluator_name](ax=ax, evaluator_hdf5=plot_data, evaluator=evaluator_name)

    @classmethod
    def _unravel_gradient_covariance_matrix(cls, parameter_name, covariance_matrix: pd.DataFrame):
        return {
            cls._gradient_covariance_name.format(parameter_name=parameter_name,
                                                 gate_name_1=gate_1,
                                                 gate_name_2=gate_2): cov_entry
            for gate_1, cov_column in covariance_matrix.items()
            for gate_2, cov_entry in cov_column.items()
        }

    @classmethod
    def create_name_parameter_variance(cls, parameter_name: str) -> str:
        return cls._parameter_variance_name.format(parameter_name=parameter_name)

    @classmethod
    def create_gradient_name(cls, parameter_name: str, gate_name: str) -> str:
        return cls._gradient_name.format(parameter_name=parameter_name, gate_name=gate_name)


def plot_voltages(voltage_data_frame: pd.DataFrame):
    voltage_fig, voltage_ax = plt.subplots()
    voltage_ax.plot(voltage_data_frame)
    voltage_ax.legend(voltage_data_frame.columns)
    voltage_ax.set_title("Gate Voltages")
    voltage_ax.set_xlabel("Measurement Number")
    voltage_ax.set_ylabel("Voltage (V)")
    return voltage_fig, voltage_ax


def plot_parameters(parameter_data_frame: pd.DataFrame,
                    parameter_std: Optional[pd.DataFrame],
                    axes: Optional[Sequence[matplotlib.axes.Axes]]=None):
    if parameter_std is None:
        parameter_std = pd.DataFrame()
    if axes is None:
        parameter_fig, parameter_ax = plt.subplots(nrows=len(parameter_data_frame.columns))
    else:
        parameter_fig, parameter_ax = None, axes
    parameter_ax = parameter_data_frame.plot(subplots=True, yerr=parameter_std,
                                             ax=parameter_ax, sharex=True, legend=False)
    for ax, par_name in zip(parameter_ax, parameter_data_frame.columns):
        ax.set_ylabel(parameter_information[par_name]["entity_unit"])
        ax.set_title(parameter_information[par_name]["name"])
    parameter_ax[-1].set_xlabel("Measurement Number")
    return parameter_fig, parameter_ax


def plot_gradients(gradients: Dict[str, pd.DataFrame],
                   gradient_std: Optional[Dict[str, pd.DataFrame]],
                   axes: Optional[Sequence[matplotlib.axes.Axes]]=None):
    if gradient_std is None:
        gradient_std = dict()

    if axes is None:
        grad_fig, grad_ax = plt.subplots(nrows=len(gradients))
    else:
        grad_fig, grad_ax = None, axes

    for ax, (parameter_name, gradient) in zip(grad_ax, gradients.items()):
        if parameter_name in gradient_std:
            gradient.plot(ax=ax, yerr=gradient_std[parameter_name].applymap(np.sqrt))

        else:
            gradient.plot(ax=ax)

        ax.set_ylabel(parameter_information[parameter_name]["gradient_unit"])
    grad_ax[0].set_title("Response Matrix")
    grad_ax[-1].set_xlabel("Measurement Number")
    return grad_fig, grad_ax


def extract_voltages_from_hierarchy(tuning_hierarchy) -> pd.Series:
    return tuning_hierarchy[0].last_voltages


def extract_parameters_from_hierarchy(tuning_hierarchy) -> (pd.Series, pd.Series):
    parameters = pd.Series()
    variances = pd.Series()
    for par_tuner in tuning_hierarchy:
        parameter, variance = par_tuner.last_parameters_and_variances
        if isinstance(par_tuner, qtune.parameter_tuner.SubsetTuner):
            relevant_parameters = par_tuner.solver.target.desired.index[
                ~par_tuner.solver.target.desired.apply(np.isnan)]
            parameters = parameters.append(parameter[relevant_parameters])
            variances = variances.append(variance[relevant_parameters])
        else:
            parameters = parameters.append(parameter)
            variances = variances.append(variance)
    return parameters, variances


def extract_gradients_from_hierarchy(tuning_hierarchy) -> (Dict[str, pd.Series], Dict[str, pd.DataFrame]):
    gradients = dict()
    covariances = dict()
    for tuner in tuning_hierarchy:
        if isinstance(tuner.solver, qtune.solver.NewtonSolver):
            for i, grad_est in enumerate(tuner.solver.gradient_estimators):
                if grad_est.estimate() is None:
                    gradients[tuner.solver.target.index[i]] = pd.Series
                else:
                    gradients[tuner.solver.target.index[i]] = grad_est.estimate()
                if grad_est.covariance() is None:
                    covariances[tuner.solver.target.index[i]] = pd.Series
                else:
                    covariances[tuner.solver.target.index[i]] = grad_est.covariance()
    return gradients, covariances


def extract_diagonal_from_data_frame(df: pd.DataFrame) -> pd.Series:
    if not set(df.index) == set(df.columns):
        raise ValueError("The index must match the columns to extract diagonal elements!")
    return pd.Series(data=[df[i][i] for i in df.index], index=df.index)


def read_evaluator_data_from_autotuner(autotuner: qtune.autotuner.Autotuner, start: int=0, end: Optional[int] = None) \
        -> pd.DataFrame:
    if end is None:
        end = len(autotuner.tuning_hierarchy)
    relevant_tuner = autotuner.tuning_hierarchy[int(start):end]
    evaluator_data = pd.DataFrame()
    for par_tuner in relevant_tuner:
        if isinstance(par_tuner, qtune.parameter_tuner.SensingDotTuner):
            relevant_evaluators = par_tuner.cheap_evaluators
            if not par_tuner.cheap_evaluation_only:
                relevant_evaluators += par_tuner.expensive_evaluators
            for evaluator in relevant_evaluators:
                if evaluator.raw_data is not None:
                    eval_data = evaluator.to_hdf5()
                    evaluator_data[evaluator.name] = [eval_data, ]
        else:
            for evaluator in par_tuner.evaluators:
                if evaluator.raw_data is not None:
                    eval_data = evaluator.to_hdf5()
                    evaluator_data[evaluator.name] = [eval_data, ]
    return evaluator_data


def plot_load_time(ax, evaluator_hdf5, **_):
    qtune.util.plot_raw_data_fit(y_data=evaluator_hdf5['raw_y_data'], x_data=evaluator_hdf5['raw_x_data'],
                                 fit_function=qtune.evaluator.func_load_time,
                                 function_args=evaluator_hdf5['fit_results'],
                                 initial_arguments=evaluator_hdf5['initial_fit_arguments'], ax=ax[0])
    ax[0].legend(['Data', 'Fit', 'Initial_parameters'])


def plot_inter_dot_tc(ax, evaluator_hdf5: dict, **_):
    if isinstance(ax, List) or isinstance(ax, Tuple) or isinstance(ax, np.ndarray):
        axi = ax[0]
    else:
        axi = ax
    if isinstance(axi, List) or isinstance(axi, Tuple) or isinstance(axi, np.ndarray):
        axi = axi[0]
    qtune.util.plot_raw_data_fit(y_data=evaluator_hdf5['raw_y_data'], x_data=evaluator_hdf5['raw_x_data'],
                                 fit_function=qtune.evaluator.func_inter_dot_coupling,
                                 function_args=evaluator_hdf5['fit_results'],
                                 initial_arguments=evaluator_hdf5['initial_fit_arguments'], ax=axi)
    axi.legend(['Data', 'Fit', 'Initial_parameters'])


def plot_lead_time(ax, evaluator_hdf5: dict, **_):
    if isinstance(ax, List) or isinstance(ax, Tuple) or isinstance(ax, np.ndarray):
        axi = ax[0]
    else:
        axi = ax
    if isinstance(axi, List) or isinstance(axi, Tuple) or isinstance(axi, np.ndarray):
        axi = axi[0]
    qtune.util.plot_raw_data_fit(y_data=evaluator_hdf5['raw_y_data'], x_data=evaluator_hdf5['raw_x_data'],
                                 fit_function=qtune.evaluator.func_lead_times_v1,
                                 function_args=evaluator_hdf5['fit_results'],
                                 initial_arguments=evaluator_hdf5['initial_fit_arguments'], ax=axi)
    axi.legend(['Data', 'Fit', 'Initial_parameters'])


def plot_transition(ax, evaluator_hdf5: dict, **_):
    for i, axi in enumerate(ax):
        qtune.util.plot_raw_data_vertical_marks(y_data=evaluator_hdf5['raw_y_data'][i],
                                                x_data=evaluator_hdf5['raw_x_data'][i],
                                                marking_position=evaluator_hdf5['transition_positions'][i],
                                                ax=axi)
        axi.set_title(evaluator_hdf5['parameters'][i])


def plot_1dim_sensing_dot_scan(ax, evaluator_hdf5: dict, **_):
    if isinstance(ax, Tuple) or isinstance(ax, List):
        ax = ax[0]
    qtune.util.plot_raw_data_vertical_marks(y_data=evaluator_hdf5['raw_y_data'],
                                            x_data=evaluator_hdf5['raw_x_data'],
                                            marking_position=evaluator_hdf5['optimal_position'],
                                            ax=ax)


def plot_2dim_sensing_dot_scan(ax, evaluator_hdf5: dict, **_):
    qtune.util.plot_raw_data_2_dim_marks(y_data=evaluator_hdf5['raw_y_data'],
                                         x_data=evaluator_hdf5['raw_x_data'],
                                         ax=ax[0],
                                         marking_position=evaluator_hdf5['new_voltages'])


def plot_average_evaluator(ax, evaluator_hdf5: dict, mode="last measurement", **_):
    if mode == "last measurement":
        plot_function_matching[evaluator_hdf5['evaluator'].name](ax=ax,
                                                                 evaluator_hdf5=evaluator_hdf5['evaluator'].to_hdf5())
    else:
        raise ValueError("Mode not specified")


plot_function_matching = {'InterDotTCByLineScan': plot_inter_dot_tc,
                          'LoadTime': plot_load_time,
                          'LeadTransitionRFA': plot_transition,
                          'LeadTransitionRFB': plot_transition,
                          'SensingDot1D': plot_1dim_sensing_dot_scan,
                          'SensingDot2D': plot_2dim_sensing_dot_scan,
                          'LeadTransition': plot_transition,
                          'AveragingInterDotTCByLineScan': plot_average_evaluator,
                          'AveragingLeadTunnelTimeByLeadScan': plot_average_evaluator,
                          'LeadTunnelTimeByLeadScan': plot_lead_time}

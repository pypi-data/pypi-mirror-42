from typing import Sequence, List, Tuple, Optional

import numpy as np
import pandas as pd

from qtune.evaluator import Evaluator
from qtune.solver import Solver, NewtonSolver
from qtune.storage import HDF5Serializable

import logging


class ParameterTuner(metaclass=HDF5Serializable):
    """This class tunes a specific set of parameters which are defined by the given evaluators."""

    def __init__(self,
                 evaluators: Sequence[Evaluator],
                 solver: Solver,
                 tuned_voltages=None,
                 last_voltage: Optional[pd.Series]=None,
                 last_parameter_values: Optional[pd.Series]=None,
                 last_parameters_variances: Optional[pd.Series]=None,
                 last_evaluation_failed: bool=False,
                 evaluatable_voltages=None,
                 last_parameter_covariances=None): # for backward compatibility
        """
        Initialize the ParamterTuner
        :param evaluators: List of evaluators representing the parameters to be tuned.
        :param solver: Optimization algorithm.
        :param tuned_voltages: List of voltages at which the parameters agreed with their set points.
        :param last_voltage:
        :param last_parameter_values:
        :param last_parameters_variances:
        :param last_evaluation_failed: True if the last evaluation has failed.
        :param evaluatable_voltages: Voltages where the evaluation of the parameters has not failed. Important for
        recovery mechanisms.
        """
        self._tuned_voltages = tuned_voltages or []
        self._solver = solver
        self._last_voltage = last_voltage
        self.last_voltages = last_voltage
        self._logger = 'qtune'
        self._last_evaluation_failed = last_evaluation_failed
        self._evaluatable_voltages = evaluatable_voltages or []

        if last_parameter_values is None:
            not_na_index = self.target.drop([ind for ind in self.target.columns if self.target.isna().all()[ind]],
                                            axis='columns').dropna().index
            self._last_parameter_values = pd.Series(index=not_na_index)
        else:
            # commented code was used for a debug attempt of the asynchron reader
            # import pickle
            # data = pickle.dumps(self.target)
            # import random
            # storage_path = r'D:\debug_%d.txt' % random.randint(0,10000)
            # with open(storage_path, 'wb') as file:
            #     file.write(data)
            assert set(self.target.dropna(how='all').index).issubset(set(last_parameter_values.index))
            self._last_parameter_values = last_parameter_values

            # import os
            # os.remove(storage_path)

        if last_parameters_variances is None:
            not_na_index = self.target.drop([ind for ind in self.target.columns if self.target.isna().all()[ind]],
                                            axis='columns').dropna().index
            self._last_parameters_variances = pd.Series(index=not_na_index)
        else:
            assert set(self.target.index).issubset(set(last_parameters_variances.index))
            self._last_parameters_variances = last_parameters_variances

        self._evaluators = tuple(evaluators)

        parameters = sorted(parameter
                            for evaluator in self._evaluators
                            for parameter in evaluator.parameters)
        if len(parameters) != len(set(parameters)):
            raise ValueError('Parameter duplicates: ', {p for p in parameters if parameters.count(p) > 1})
        assert set(self.target.dropna().index).issubset(set(parameters))

    @property
    def logger(self):
        return logging.getLogger(self._logger)

    @property
    def last_voltages(self) -> pd.Series:
        return self._last_voltage

    @last_voltages.setter
    def last_voltages(self, new_voltages: pd.Series):
        if self.last_voltages is None or self.last_voltages.empty:
            self._last_voltage = new_voltages
        else:
            index_intersection = self.last_voltages.index.intersection(new_voltages)
            self._last_voltage[index_intersection] = new_voltages[index_intersection]

    @property
    def solver(self) -> Solver:
        return self._solver

    @property
    def state(self) -> pd.Series:
        return self.solver.state

    @property
    def target(self) -> pd.DataFrame:
        return self.solver.target

    @target.setter
    def target(self, changes):
        self.solver.target = changes

    @property
    def parameters(self) -> Sequence[str]:
        """Alphabetically sorted parameters"""
        return self.solver.target.index

    @property
    def last_parameters_and_variances(self) -> Tuple[pd.Series, pd.Series]:
        """Last parameter values with variances."""
        return self._last_parameter_values, self._last_parameters_variances

    @property
    def tuned_voltages(self) -> List[pd.Series]:
        """A list of the positions where the parameter set was successfully tuned."""
        return self._tuned_voltages

    @property
    def last_evaluation_failed(self) -> bool:
        return self._last_evaluation_failed

    @property
    def evaluators(self) -> Tuple[Evaluator, ]:
        return self._evaluators

    def evaluate(self) -> Tuple[pd.Series, pd.Series]:
        """
        Evaluates the parameters.
        :return: Values as pandas Series, Variances as pandas Series.
        """
        parameters = []
        variances = []
        for evaluator in self._evaluators:
            self.logger.info('Evaluating %s' % evaluator.name)
            parameter, variance = evaluator.evaluate()
            parameters.append(parameter)
            variances.append(variance)
        return pd.concat(parameters)[self.parameters], pd.concat(variances)[self.parameters]

    def is_tuned(self, voltages: pd.Series) -> bool:
        """
        Checks if current parameters already match the requirements stated in the solver. Thereby these parameters are
        evaluated.
        :param voltages: current voltages
        :return: True if requirement is met. False otherwise.
        """
        raise NotImplementedError()

    def get_next_voltages(self, tuned_parameters=None) -> pd.Series:
        """The next voltage in absolute values.
        :return: next_voltages
        """
        raise NotImplementedError()

    def restart(self, new_voltages):
        self.last_voltages = new_voltages
        self.solver.restart(new_voltages)

    def to_hdf5(self) -> dict:
        return dict(evaluators=self._evaluators,
                    solver=self._solver,
                    tuned_voltages=self._tuned_voltages,
                    last_voltage=self._last_voltage,
                    last_parameter_values=self._last_parameter_values,
                    last_parameters_variances=self._last_parameters_variances,
                    last_evaluation_failed=self._last_evaluation_failed,
                    evaluatable_voltages=self._evaluatable_voltages)


class SubsetTuner(ParameterTuner):
    """This tuner uses only a subset of gates to tune the parameters"""

    def __init__(self, evaluators: Sequence[Evaluator], gates: Sequence[str], maximal_step_size: float=np.nan,
                 maximal_step_number: int=1, number_queued_steps: int=0, **kwargs):
        """
        Initializes the SubsetTuner. Verifies that the gates correspond to the current positions.
        :param evaluators:
        :param gates: Gates which are used to tune the parameters
        :param tuned_voltages:
        :param last_voltage:
        :param last_parameter_values:
        """
        super().__init__(evaluators, **kwargs)

        self._tunable_gates = sorted(gates)
        assert set(gates) == set(self.solver.current_position.index)

        self._maximal_step_size = maximal_step_size
        self._maximal_step_number = maximal_step_number
        self._number_queued_steps = number_queued_steps

    @property
    def tunable_gates(self):
        return self._tunable_gates

    def is_tuned(self, voltages: pd.Series) -> bool:
        """
        Checks if the parameters agree with the target within the tolarance.
        :param voltages: Voltages of the Evaluation.
        :return: True if the parameters agree with the target.
        """
        self._last_voltage = voltages

        if self._number_queued_steps != 0:
            self.solver.current_position = voltages
            return False

        current_parameters, current_variances = self.evaluate()

        self.solver.rescale_values(current_parameters, current_variances)
        self._last_parameter_values = current_parameters[self._last_parameter_values.index]
        self._last_parameters_variances = current_variances[self._last_parameter_values.index]

        # check for an evaluation failure (only relevant parameters)
        if self._last_parameter_values.isnull().values.any():
            self._last_evaluation_failed = True
            return False
        self._last_evaluation_failed = False
        self._evaluatable_voltages.append(voltages)

        self._solver.update_after_step(voltages, current_parameters, current_variances)
        if ((self.target.desired - current_parameters).abs().fillna(0.) < self.target['tolerance'].fillna(
                np.inf)).all():
            self._tuned_voltages.append(voltages)
            return True
        else:
            return False

    def get_next_voltages(self, tuned_parameters=None):
        """
        Slices the update step given by the solver into the maximal step size.
        :param tuned_parameters: Parameters which are below in the tuning hierarchy.
        :return: New voltages.
        """
        if self._last_evaluation_failed:
            return 0.5 * (self._evaluatable_voltages[-1] + self._last_voltage)

        solver_voltage = self._solver.suggest_next_position(tuned_parameters)
        new_voltages = pd.Series(self._last_voltage).copy(deep=True)
        new_voltages[solver_voltage.index] = solver_voltage
        step = new_voltages - self._last_voltage

        if np.linalg.norm(step) > self._maximal_step_size:
            if self._number_queued_steps == 0:
                number_of_steps = int(np.linalg.norm(step) / self._maximal_step_size)
                self._number_queued_steps = min(number_of_steps, self._maximal_step_number)
            self._number_queued_steps -= 1
            step *= self._maximal_step_size / np.linalg.norm(step)

        rescaled_new_voltages = self._last_voltage + step
        return rescaled_new_voltages

    def to_hdf5(self):
        parent_dict = super().to_hdf5()
        return dict(parent_dict,
                    gates=self._tunable_gates,
                    maximal_step_size=self._maximal_step_size,
                    maximal_step_number=self._maximal_step_number,
                    number_queued_steps=self._number_queued_steps)


class SensingDotTuner(ParameterTuner):
    """
    This tuner directly tunes to voltage points of interest. The evaluators return positions
    """

    def __init__(self, cheap_evaluators: Sequence[Evaluator], expensive_evaluators: Sequence[Evaluator],
                 gates: Sequence[str], cheap_evaluation_only=True, **kwargs):
        """
        Designed for the sensing dot which requires no solver but allows cheap and expensive measurements.
        :param cheap_evaluators: An evaluator with little measurement costs. (i.e. one dimensional sweep of gates
        defining the sensing dot.) This evaluator needs to detect at least if the parameter already meets the
        conditions defined in the target. It can also detect additional information (i.e. voltages with higher contrast
        in the sensing dot.)
        :param expensive_evaluators: An evaluator which finds the optimal position of the sensing dot, or information
        leading to its position(i.e. two dimensional sensing dot scan.). The parameters can be specified using
        last_parameter_values and last_parameters_covariances or they will be deduced from the evaluators.
        :param gates: The gates which will be used to tune the parameters
        :param min_threshhold: If the parameters are below this threshold, the experiment is not tuned. This doesnt
        regard the optimal signal found but only the current one.
        :param cost_threshhold: If the parameters are below this threshold, the expensive evaluation will be used.
        :param kwargs: Must contain the argument 'solver' for the init function of the ParameterTuner parent class.
        """
        last_parameter_values_covariances = []
        for string in ["last_parameter_values", "last_parameters_variances"]:
            if string not in kwargs:
                parameter_names = [name for evaluator_list in [cheap_evaluators, expensive_evaluators]
                                   for evaluator in evaluator_list
                                   for name in evaluator.parameters]
                parameter_names = set(parameter_names)
                parameter_names = sorted(list(parameter_names))
                series = pd.Series(index=parameter_names)
            else:
                series = kwargs[string]
                del kwargs[string]
            last_parameter_values_covariances.append(series)

        self._tunable_gates = sorted(gates)
        self.cheap_evaluation_only = cheap_evaluation_only

        super().__init__(cheap_evaluators, last_parameter_values=last_parameter_values_covariances[0],
                         last_parameters_variances=last_parameter_values_covariances[1], **kwargs)
        self._tunable_gates = sorted(gates)
        self._cheap_evaluators = cheap_evaluators
        self._expensive_evaluators = expensive_evaluators

    @property
    def evaluators(self) -> Tuple[Evaluator, ]:
        return tuple(self._cheap_evaluators) + tuple(self._expensive_evaluators)

    @property
    def cheap_evaluators(self):
        return tuple(self._cheap_evaluators)

    @property
    def expensive_evaluators(self):
        return tuple(self._expensive_evaluators)

    def is_tuned(self, voltages: pd.Series):
        current_parameter, variances = self.evaluate(cheap=True)
        self.solver.rescale_values(current_parameter, variances)
        self._last_voltage = voltages
        self._last_parameter_values[current_parameter.index] = current_parameter[current_parameter.index]
        self._last_parameters_variances[current_parameter.index] = variances[current_parameter.index]

        if self._last_parameter_values[current_parameter.index].isnull().values.any():
            self._last_evaluation_failed = True
            return False
        self._last_evaluation_failed = False

        if current_parameter.le(self.target["minimum"]).any():
            self.cheap_evaluation_only = True
            if current_parameter.le(self.target["cost_threshold"]).any():
                self.logger.info('Expensive evaluation required.')
                self.cheap_evaluation_only = False
                current_parameter, variances = self.evaluate(cheap=False)
                self.solver.rescale_values(current_parameter, variances)
                self._last_parameter_values[current_parameter.index] = current_parameter[current_parameter.index]
                self._last_parameters_variances[current_parameter.index] = variances[current_parameter.index]

            self.solver.update_after_step(voltages, current_parameter, variances)
            return False
        else:
            self.cheap_evaluation_only = True
            self._tuned_voltages.append(voltages)
            return True

    def get_next_voltages(self, tuned_parameters=None):
        if self._last_evaluation_failed:
            return 0.5 * (self.tuned_voltages[-1] + self._last_voltage)
        next_voltages = self._solver.suggest_next_position(tuned_parameters=tuned_parameters)
        return next_voltages

    def evaluate(self, cheap=True, **kwargs) -> (pd.Series, pd.Series):
        #  no list comprehension for easier debugging
        #  cheap = kwargs["cheap"]
        parameters = []
        variances = []
        if cheap:
            for evaluator in self._cheap_evaluators:
                self.logger.info('Evaluating the cheap evaluator %s' % evaluator.name)
                parameter, variance = evaluator.evaluate()
                parameters.append(parameter)
                variances.append(variance)
        else:
            for evaluator in self._expensive_evaluators:
                self.logger.info('Evaluating the expensive evaluator %s' % evaluator.name)
                parameter, variance = evaluator.evaluate()
                parameters.append(parameter)
                variances.append(variance)
        return pd.concat(parameters).sort_index(), pd.concat(variances).sort_index()

    def to_hdf5(self):
        return dict(cheap_evaluators=self._cheap_evaluators,
                    expensive_evaluators=self._expensive_evaluators,
                    gates=self._tunable_gates,
                    solver=self.solver,
                    last_voltage=self._last_voltage,
                    last_parameter_values=self._last_parameter_values,
                    last_parameters_variances=self._last_parameters_variances,
                    cheap_evaluation_only=self.cheap_evaluation_only)

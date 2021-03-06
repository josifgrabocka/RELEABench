
# a benchmark is a collection of meta-datasets
# metadatasets: is a list of instances from the MetaDataset class
class MFBenchmark:
    def __init__(self, name=None, metadatasets=None):
        self.name = name
        # the collection of meta-datasets
        self.metadatasets = metadatasets

# a meta-dataset is a collection of evaluations in different tasks
# config_space: is an instance from the https://automl.github.io/ConfigSpace/master/ class
# fidel_space: is an instance from the https://automl.github.io/ConfigSpace/master/ class
# tasks: is a list of instances from the Task class
# is_progressive: a boolean setting that indicates that the fidel_space is progressive
class MetaDataset:
    def __init__(self, name=None, config_space=None, fidel_space=None, tasks=None):
        self.name = name
        # the configuration and the fidelities space
        self.config_space = config_space
        self.fidel_space = fidel_space
        # the list of evaluations in the form of instances of the Evaluation class
        self.tasks = tasks

# a task represents the evaluations of configurations on a dataset
# eval_list: is a list of Evaluation class instances
# eval_function: a function that takes as an input a configuration and a fidelity, both Configuration instances and evaluates
# notice that either the task will have an eval_function, or an eval_list, but not both
class Task:
    def __init__(self, name=None, eval_list=None, eval_function=None):
        self.name = name
        # the list of evaluations in the form of instances of the Evaluation class
        self.evaluations = eval_list

        # is the task a continuous or discrete one, if continuous
        self.has_eval_function = False
        if eval_list is None and eval_function is not None:
            self.has_eval_function = True
            self.eval_function = eval_function

        # initialize the task_information class that encapsulates the derived information on this task
        self.task_information = TaskInformation(task=self, is_continuous=self.has_eval_function)

    # return the unique configurations of the task
    def fetch_unique_configurations(self):
        # read all the configurations in a list
        configs = []
        for eval in self.evaluations:
            configs.append(eval.configuration)
        # return a list of the unique configurations
        return list(set(configs))

    # return the unique fidelities of a configuration
    # or belonging to one particular configuration
    def fetch_unique_fidelities(self, configuration):
        # read all the configurations in a list
        fidelities = []
        for eval in self.evaluations:
            if eval.configuration == configuration:
                fidelities.append(eval.fidelities)
        # return a list of the unique configurations
        return list(set(fidelities))

    # return the response and runtime of a configuration at the given fidelity, if not found return None
    def evaluate(self, configuration, fidelities):
        # querying the continuous surrogate
        if self.has_eval_function:
            return self.eval_function(configuration=configuration, fidelities=fidelities)
        else:
            for eval in self.evaluations:
                if eval.configuration == configuration and eval.fidelities == fidelities:
                    return eval.response_series, eval.runtime_series
            # evaluation not found
            return None

# encapsulate the information about a task, that are needed by HPO methods to decide on the initial design
# what configurations and fidelities to suggest, etc.
class TaskInformation:

    __task = None

    def __init__(self, task=None, is_continuous=False):
        self.__task = task
        self.is_continuous = is_continuous

        if self.__task is not None:
            # the feasible configurations for non-continuous spaces
            if not self.is_continuous:
                # the unique configurations among the ones evaluated in the task, derived from the self.evaluations
                self.feasible_configurations = self.__task.fetch_unique_configurations()
                # create empty dictionary of the fidelities per config
                self.feasible_fidelities_per_config = {}
                for config in self.feasible_configurations:
                    self.feasible_fidelities_per_config[config] = set()
                # store the unique values of the fidelities for each configuration
                for eval in self.__task.evaluations:
                    self.feasible_fidelities_per_config[eval.configuration].add(eval.fidelities)


# an evaluation is a tuple of (configuration, fidelities, response, runtime), where
# configuration is a Configuration from the ConfigSpace library
# fidelities is a Configuration from the ConfigSpace library
# response [float] indicate the response of evaluating a configuration at the respective fidelities, e.g. validation accuracy
# auxiliary_responses "list of [float]" indicate the auxiliary responses of evaluating a configuration at the respective fidelities, e.g. training loss, accuracy, etc.
# runtime [float] indicate the wallclock runtime in seconds of evaluating a configuration at the respective fidelities
class Evaluation:
    def __init__(self, configuration=None, fidelities=None, val_response=None, test_response=None, runtime=None, auxiliary_responses=None):
        self.configuration = configuration
        self.fidelities = fidelities
        self.val_response = val_response
        self.test_response = test_response
        self.auxiliary_responses = auxiliary_responses
        self.runtime = runtime

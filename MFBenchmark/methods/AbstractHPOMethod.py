
# an abstract HPO method
class AbstractHPOMethod:

    # initialize a HPO method providing task information and the budget as contructor informaiton
    def __init__(self, task_information, max_trials=None, max_wallclock_time=None):
        self.task_information = task_information
        # store the budget
        self.max_num_trials = max_trials
        self.max_wallclock_time = max_wallclock_time

    # suggests a list of next configurations, and for what fidelity to try those configurations
    # returns a list of tuples (configurations, fidelities), where the length of the list is num_configurations
    # this step is commonly referred to as the acquisition function
    # this method should be run after suggest_initial
    def suggest(self):
        return None

    # provide the evaluated configurations to the method as observations
    # this step is commonly referred as surrogate fitting and updating the history
    def observe(self, configurations, fidelities, responses, runtimes):
        pass
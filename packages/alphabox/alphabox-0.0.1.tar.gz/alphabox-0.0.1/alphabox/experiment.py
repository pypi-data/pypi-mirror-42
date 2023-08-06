"""
    Implements a trial object.

    This trial objects records all observations

"""
import requests

# TODO: Add authroization logic
class Experiment:

    # TODO: Add if it's a minimization or a maximization task

    def __init__(self, experiment_id=None, experiment_description=None, search_method=None, minimize=True, local=False):
        """

        This experiment finds the minimum value amongst all items

        Exactly one of
            experiment_id or parameter_names
        has to be not None

        :param experiment_id:
            If not None, loads the experiment from the database

        :param experiment_description:
            If not None, creates  anew experiment
            {
                "parameter_names": ["a", "b", "c"],
                "parameter_types": ["float", "float", "float"],
                "parameter_ranges": [[0.0, 10.0], [5.0, 8.0], [10.0, 20.0]]
            }

        :param search_method:
            One of the following [None, "random", "grid"].
            If it is `None`, then our Bayesian optimization algorithms are used.
            If it is `random`, then random search is used
            If it is `grid`, then grid-search is used
        """

        self.search_method = search_method
        self.minimize = True

        # constant definitions
        if local:
            self.baselink = "http://127.0.0.1:5000/"
        else:
            self.baselink = "https://bayesianoptimizationx.appspot.com/"
        self.endpoint_suggestion = self.baselink + "get-suggestion"


        assert (experiment_id and not experiment_description) or (not experiment_id and experiment_description), (
            "Not exactly one of experiment_id or parameter_array is not None", experiment_id, experiment_description)

        self._trials = []

        if experiment_id is None:
            self._experiment_description = experiment_description
        else:
            # TODO: load from experiment from the database
            self._experiment_description = {
                "parameter_names": ["a", "b", "c"],
                "parameter_types": ["float", "float", "float"],
                "parameter_ranges": [[0.0, 10.0], [5.0, 8.0], [10.0, 20.0]]
            }

    @property
    def experiment_description(self):
        return self._experiment_description

    @property
    def trials(self):
        # TODO: replace with trials
        return dict({
            "observations": self._trials
        })

    @property
    def suggestion(self):
        return self._suggestion()

    def _suggestion(self, request_json=None, verbose=False):
        """
            Given all observations,
            queries the endpoint to get the next suggest parameter combination
        :return:
        """
        if request_json is None:
            request_json = dict()
            request_json.update(self.experiment_description)
            request_json.update(self.trials)

        # Make random search if asked for random search:
        if self.search_method is not None:
            request_json.update(
                dict({"method": self.search_method})
            )


        if verbose:
            print("Posting...", request_json)

        r = requests.post(
            url=self.endpoint_suggestion,
            json=request_json
        )
        try:
            data = r.json()
        except Exception as e:
            print(e)
            print("Something went wrong trying to decode the object into a json")
            print("The following is the object!")
            print(r)
            print(r.content)
            assert False
            exit(-1)

        if verbose:
            print(data)
            # print(data['Y'])

        out = data['suggestion']
        return out

    def add(self, parameter_configuration, value):
        """
        :param parameter_configuration:
            Dictionary of key-value pairs. The keys are the parameter names. The values are the realized parameter configurations.
        :param value:
            Is the value that the ran experiment returns
        :return:
        """

        tmp_parameters = dict()
        tmp_parameters.update(parameter_configuration)
        tmp_value = dict({"value": value})
        tmp_value.update(tmp_value)

        tmp = dict()
        tmp.update(tmp_parameters)
        tmp.update(tmp_value)

        self._trials.append(
            tmp
        )

    @property
    def best_config(self):
        min_config = None
        min_score = 10000000.
        for x in self._trials:
            if x['value'] < min_score:
                min_config = x
                min_score = x['value']

        return min_config





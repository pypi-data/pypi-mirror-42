from hyperyaml.reader import YAMLReader
from hyperyaml.runner import Runner
import yaml


class HyperYaml:
    def __init__(self, model_config, model_builder, max_evals):
        self.params = YAMLReader.read(model_config)
        self.model_builder = model_builder
        self.max_evals = max_evals

    def run(self):
        runner = Runner(self.params, self.model_builder, self.max_evals)
        best, trials = runner.run()
        print(f"Hyperparameter optimization complete, best loss was {min(trials.losses())}")
        self.best_set = best
        return best, trials

    def write(self, out):
        with open(out, "w") as stream:
            yaml.dump(self.best_set, stream=stream, default_flow_style=False)


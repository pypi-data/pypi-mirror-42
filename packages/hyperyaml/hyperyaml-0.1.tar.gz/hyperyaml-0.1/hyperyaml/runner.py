from hyperopt import hp, fmin, tpe, Trials



class Runner:
    def __init__(self, params, model_builder,max_evals):
        self.params = params
        self.search_space = self._build_search_space()
        self.names = [p.name for p in params]
        self.model_builder = model_builder
        self.max_evals = max_evals

    def _build_search_space(self):
        space = []
        for parm in self.params:
            if parm.dtype == "int":
                sub = hp.quniform(parm.name, parm.min, parm.max, 1)
            else:
                sub = hp.uniform(parm.name, parm.min, parm.max)
            space.append(sub)
        return space

    def _decorator(self, params):
        args = dict((zip(self.names, params)))
        return self.model_builder.build(args)


    def run(self):
        objective = self._decorator
        trials = Trials()
        best = fmin(objective,
                    space=self.search_space,
                    algo=tpe.suggest,
                    max_evals=self.max_evals,
                    trials=trials)
        return best, trials

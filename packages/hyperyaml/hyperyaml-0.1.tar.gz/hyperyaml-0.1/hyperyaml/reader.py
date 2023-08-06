from hyperyaml.types import Parameter
import os
import yaml


class YAMLReader:
    @staticmethod
    def read(fp):
        if not os.path.isfile(fp):
            raise ValueError(f"no such file {fp}")
        with open(fp) as stream:
            doc = yaml.load(stream)
        params = []
        for key in doc:
            p = Parameter(key, doc[key]["TYPE"], doc[key]["MIN"], doc[key]["MAX"])
            params.append(p)
        return params


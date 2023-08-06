from setuptools import setup

def get_requirements():
    reqs = []
    with open("requirements.txt") as fh:
        for line in fh:
            reqs.append(line)
    return reqs

setup(name='hyperyaml',
      version='0.1',
      description='A library to build and run hyperparameter tuning schemes from yaml files',
      url='https://github.com/josmcg/HyperYAML',
      author='Josh McGrath',
      author_email='joshuawmcgrath@gmail.com',
      license='MIT',
      packages=['hyperyaml'],
      test_suite="nose.collector",
      install_requires=get_requirements(),
      zip_safe=False)
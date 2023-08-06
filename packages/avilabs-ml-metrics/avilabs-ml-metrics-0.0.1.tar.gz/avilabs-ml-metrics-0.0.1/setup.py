from setuptools import setup, find_packages

setup(
    name='avilabs-ml-metrics',
    version='0.0.1',
    description='Machine Learning Metrics',
    url='https://gitlab.com/avilay/ml-metrics',
    author='Avilay Parekh',
    author_email='avilay@avilaylabs.net',
    license='MIT',
    packages=find_packages(exclude=['mlmetrics.tests'])
)

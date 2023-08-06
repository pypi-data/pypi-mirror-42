from setuptools import setup, find_packages


long_description = '''
# ML Metrics
A simple and flexible API to log metrics. Currently a metrics logger for logging to SQLite is implemented. Other backends can be implemented as needed.

# Quickstart
## Write Logs
```python
from mlmetrics.sqlitemetrics.sqlite_metric import SqliteMetric

db = './metrics.db'
metric = SqliteMetric(db, name='fuel_gauge', labels={'model', 'trip'})
metric.log(model='toyota', trip='short', value=1.2)
```

## Query Logs
```python
from mlmetrics.sqlitemetrics.sqlite_metric import SqliteMetric

db = './metrics.db'
logs = metric.logs(start=1550554038.80172, end=1550554038.80265)
for row in logs:
    for fld in row.keys():
        print(fld, row[fld])
```

For more details see the [Homepage](https://gitlab.com/avilay/ml-metrics)
'''

setup(
    name='avilabs-ml-metrics',
    version='1.0.1',
    description='Metrics for Machine Learning',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Avilay Parekh',
    author_email='avilay@gmail.com',
    license='MIT',
    url='https://gitlab.com/avilay/ml-metrics',
    packages=find_packages()
)

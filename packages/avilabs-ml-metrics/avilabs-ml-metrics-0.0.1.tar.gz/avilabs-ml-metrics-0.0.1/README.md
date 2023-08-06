# Purpose
A simple metric library with a built-in implementation that logs metrics to SQLite databases. It is possible to implement other backing datastores as well.

# Installation
```bash
pip install avilabs-ml-metrics
```

# Usage
## Instantiating
```python
db = './metrics.db'
metric = SqliteMetric(db, name='fuel_gauge', labels={'model', 'trip'})
```

This will create a table called `fuel_gauge` in `metrics.db` if it doesn't exist. If it does that will be used. The table will have the following fields:
  * `model` which is a text field
  * `trip` which is a text field
  * `timestamp` which is a real field
  * `value` which is a real field
  
## Writing Metrics
```python
metric.log(model='toyota', trip='short', value=1.2)
```
Will add a row in the `fuel_gauge` table. The timestamp will be added automatically. It is just `datetime.now().timestamp()`.

## Querying Metrics
```python
logs = metric.logs(model='toyota')
for row in logs:
    for fld in row.keys():
        print(fld, row[fld])
```

## Snapshots
### Writing
It is possible that a bunch of logs represent the value of the metric at a single instant in time. Ideally all these logs will have the same timestamp. Howeverm, writing them one by one will result in each log having a different timestamp. To prevent this from happening and ensuring that all subsequent logs should have the same timestamp, use `snapshots`.

```python
metric.start_snapshot()
for _ in range(10):
    metric.log(model='toyota', trip='short', value=val)
metric.end_snapshot()
```

### Querying
It is possible to query snapshots instead of individual logs.
```python
snapshots = metric.snapshots(start=1550554038.80172, end=1550554038.80265)
for snapshot in snapshots:
    for row in snapshot:
        for fld in row.keys():
            print(fld, row[fld])
```
The `snapshots` method will return an iterator of snapshots, each snapshot is a sequence of logs with the same timestamp.

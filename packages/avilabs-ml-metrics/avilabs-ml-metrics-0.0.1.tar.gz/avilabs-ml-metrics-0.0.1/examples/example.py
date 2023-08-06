import logging
import os.path as path
import random

from mlmetrics.sqlitemetrics.sqlite_metric import SqliteMetric

logging.basicConfig(level=logging.INFO)

db = path.expanduser(path.join('~', 'temp', 'metrics.db'))
metric = SqliteMetric(db, 'state_values', {'run_id', 'operation', 'state'})


def write():
    run_id = 'sparkling-crystal-1233'
    op = 'planning'
    for e in range(1000):
        print(f'Processing epoch {e}')
        metric.start_snapshot()
        for i in range(3):
            for j in range(3):
                metric.log(run_id=run_id, operation=op, state=f'({i},{j})', value=random.random())
        metric.stop_snapshot()


def query():
    snapshots = metric.snapshots(start=1550554038.80172, end=1550554038.80265)
    for snapshot in snapshots:
        print('\nNEW SNAPSHOT-')
        for row in snapshot:
            for fld in row.keys():
                print(fld, row[fld])


def query2():
    logs = metric.logs(start=1550554038.80172, end=1550554038.80265)
    for row in logs:
        for fld in row.keys():
            print(fld, row[fld])


query2()
metric.close()
print('DONE')

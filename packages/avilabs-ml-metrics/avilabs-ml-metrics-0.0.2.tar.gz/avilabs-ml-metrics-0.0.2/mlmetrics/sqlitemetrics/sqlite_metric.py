import logging
import multiprocessing as mp
import signal
import sqlite3
import sys
from copy import copy
from datetime import datetime
from typing import Iterator, Tuple, List, Set

from mlmetrics.metric import Metric

logger = logging.getLogger(__name__)


def log_metric(db: str, q: mp.Queue):
    conn = sqlite3.connect(db)
    ins_sql, vals = q.get()
    while True:
        if ins_sql == 'QUIT':
            break
        cur = conn.cursor()
        cur.execute(ins_sql, vals)
        conn.commit()
        ins_sql, vals = q.get()


class SqliteMetric(Metric):
    def __init__(self, db: str, name: str, labels: Set[str]) -> None:
        self._conn = sqlite3.connect(db)
        self._conn.row_factory = sqlite3.Row
        self._table: str = ''
        self._labels: Set[str] = set()
        self._is_snapshot: bool = False
        self._snapshot_ts: float = -1.

        self._create_or_use(name, labels)

        self._q: mp.Queue = mp.Queue()
        self._proc = mp.Process(target=log_metric, args=(db, self._q))
        self._proc.start()
        logger.debug(f'Started writer process with pid {self._proc.pid}')
        signal.signal(signal.SIGTERM, self._terminate)
        signal.signal(signal.SIGINT, self._terminate)

    def _create_or_use(self, name: str, labels: Set[str]):
        cur = self._conn.execute(f'pragma table_info({name})')
        flds = cur.fetchall()
        if flds:
            # Table exists - check its schema
            for fld in flds:
                fldname = fld[1]
                fldtype = fld[2]
                if fldname == 'timestamp' or fldname == 'value':
                    continue
                if fldname in labels and fldtype == 'text':
                    continue
                else:
                    raise RuntimeError(f'Table {name} exists with a different schema!')
        else:
            # Create table
            sql = f'CREATE TABLE {name} (timestamp real, '
            for label in labels:
                sql += f'{label} text, '
            sql += 'value real)'
            cur.execute(sql)
            self._conn.commit()
        cur.close()
        self._labels = copy(labels)
        self._table = name

    def start_snapshot(self) -> None:
        self._is_snapshot = True
        self._snapshot_ts = datetime.now().timestamp()

    def stop_snapshot(self) -> None:
        self._is_snapshot = False
        self._snapshot_ts = -1.

    def _gen_filter(self, start=None, end=None, **filters) -> Tuple:
        flds = []
        vals = []
        for fld, val in filters.items():
            flds.append(f'{fld}=?')
            vals.append(val)
        if start:
            flds.append('timestamp>=?')
            vals.append(start)
        if end:
            flds.append('timestamp<=?')
            vals.append(end)
        return ' AND '.join(flds), vals

    def snapshots(self, start=None, end=None, **filters) -> Iterator[List[Tuple]]:
        # Get distinct snapshot timestamps from the rows of interest
        sel_sql_filters, vals = self._gen_filter(start, end, **filters)
        sel_sql = f'SELECT DISTINCT(timestamp) FROM {self._table} WHERE {sel_sql_filters}'
        logger.debug(sel_sql)
        cur = self._conn.cursor()
        cur.execute(sel_sql, vals)
        timestamps = []
        for row in cur:
            timestamps.append(row[0])

        # Get each timestamp at a time
        sel_sql_flds = ','.join(['timestamp'] + list(self._labels) + ['value'])
        sel_sql = f'SELECT {sel_sql_flds} FROM {self._table} WHERE timestamp=?'
        for timestamp in timestamps:
            cur.execute(sel_sql, [timestamp])
            rows = cur.fetchall()
            yield rows
        cur.close()

    def use_table(self, name: str) -> None:
        self._table = name

    def _terminate(self, signum, frame) -> None:
        self._proc.terminate()
        self._proc.join()
        self._proc.close()
        sys.exit(1)

    def close(self) -> None:
        self._q.put(('QUIT', ''))
        self._proc.join()
        self._proc.close()

    def log(self, **kwargs) -> None:
        if self._is_snapshot:
            ts = self._snapshot_ts
        else:
            ts = datetime.now().timestamp()
        ins_sql_flds = ','.join(['timestamp'] + list(self._labels) + ['value'])
        ins_sql_vals = ','.join(['?'] * (len(self._labels) + 2))
        ins_sql = f'INSERT INTO {self._table} ({ins_sql_flds}) VALUES ({ins_sql_vals})'
        vals = [ts] + [kwargs[label] for label in self._labels if label != 'value'] + [kwargs['value']]
        logger.debug(ins_sql)
        logger.debug(vals)
        self._q.put((ins_sql, vals))

    def logs(self, start=None, end=None, **filters) -> Iterator[Tuple]:
        sel_sql_flds = ','.join(['timestamp'] + list(self._labels) + ['value'])
        sel_sql_filters, vals = self._gen_filter(start, end, **filters)
        sel_sql = f'SELECT {sel_sql_flds} FROM {self._table} WHERE {sel_sql_filters}'
        logger.debug(sel_sql)
        logger.debug(vals)
        cur = self._conn.cursor()
        cur.execute(sel_sql, vals)
        for row in cur:
            yield row
        cur.close()

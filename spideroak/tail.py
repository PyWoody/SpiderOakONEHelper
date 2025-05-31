import os
import re
import time

from datetime import datetime

try:
    from rich import print
except ModuleNotFoundError:
    pass

from spideroak import utils


def tail():
    log_re = re.compile(r'_\d{14}\.log', re.IGNORECASE)
    log_path = utils.logdir()
    prev_log = None
    try:
        while True:
            try:
                log = max(
                    (
                        os.path.join(log_path, f)
                        for f in os.listdir(log_path)
                        if log_re.search(f)
                    ), key=to_datetime
                )
            except ValueError:
                raise Exception('No logs found on device')
            if prev_log is not None and prev_log != log:
                print(f'\n\tNow tailing {log}\n')
            _tail(log)
            prev_log = log
    except KeyboardInterrupt:
        return


def _tail(log, sleep=1, until=10):
    elapsed = 0
    with open(log, 'rb') as f:
        _ = f.seek(0, os.SEEK_END)
        while True:
            if line := f.readline():
                print(line.decode('utf8', errors='replace'), end='')
                elapsed = 0
            else:
                if elapsed >= until:  # aka, nothing for N seconds
                    return
                elapsed += sleep
                time.sleep(sleep)


def to_datetime(log_path):
    log = os.path.split(log_path)[1]
    *_, log = log.split('_', maxsplit=1)
    year = slice(0, 4)
    month = slice(4, 6)
    day = slice(6, 8)
    hour = slice(8, 10)
    minute = slice(10, 12)
    second = slice(12, 14)
    return datetime(
        int(log[year]),
        int(log[month]),
        int(log[day]),
        int(log[hour]),
        int(log[minute]),
        int(log[second]),
    )


if __name__ == '__main__':
    tail()

import io
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
    logs_pos = dict()
    datetime_key = setup_datetime()
    try:
        while True:
            try:
                log = max(
                    (
                        os.path.join(log_path, f)
                        for f in os.listdir(log_path)
                        if log_re.search(f)
                    ), key=datetime_key
                )
            except ValueError:
                raise Exception('No logs found on device')
            if prev_log is not None and prev_log != log:
                print(f'\n\tNow tailing {log}\n')
            last_read_pos = _tail(log, last_read_pos=logs_pos.get(log, 0))
            logs_pos[log] = last_read_pos
            prev_log = log
    except KeyboardInterrupt:
        return


def _tail(log, last_read_pos=0, sleep=.5, until=10):
    elapsed = 0
    with open(log, 'rb') as f:
        reader = io.BufferedReader(f)
        if last_read_pos == 0:
            _ = reader.seek(last_read_pos, os.SEEK_END)
        else:
            _ = reader.seek(last_read_pos)
        prev_data = b''
        while True:
            if data := reader.read(io.DEFAULT_BUFFER_SIZE):
                if prev_data:
                    data = prev_data + data
                    prev_data = b''
                head = 0
                while (tail := data.find(b'\n', head)) != -1:
                    print(data[head:tail].decode('utf8', errors='replace'))
                    head = tail + 1
                if head != len(data):
                    prev_data = data[head:]
                if elapsed > 0:
                    elapsed = 0
            else:
                if elapsed >= until:  # aka, nothing for N seconds
                    return f.tell()
                elapsed += sleep
                time.sleep(sleep)


def setup_datetime():
    year = slice(0, 4)
    month = slice(4, 6)
    day = slice(6, 8)
    hour = slice(8, 10)
    minute = slice(10, 12)
    second = slice(12, 14)

    def compute(log_path):
        log = os.path.split(log_path)[1]
        *_, log = log.split('_', maxsplit=1)
        return datetime(
            int(log[year]),
            int(log[month]),
            int(log[day]),
            int(log[hour]),
            int(log[minute]),
            int(log[second]),
        )

    return compute


if __name__ == '__main__':
    tail()

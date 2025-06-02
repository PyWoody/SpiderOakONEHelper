import subprocess
import tempfile

from threading import Thread

from spideroak import cli_path, tail


class TailThread(Thread):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stopped = False

    def run(self):
        if 'last_read_pos' not in self._kwargs:
            self._kwargs['last_read_pos'] = 0
        while not self.stopped:
            try:
                last_read_pos = self._target(*self._args, **self._kwargs)
            except FileNotFoundError:
                # Command interrupted, logfile already deleted
                return
            self._kwargs['last_read_pos'] = last_read_pos
        # Retry to read the last chunk of the file, just in case there was
        # more written. Prevents race condition
        self._kwargs['sleep'] = 0
        self._kwargs['until'] = 0
        try:
            _ = self._target(*self._args, **self._kwargs)
        except FileNotFoundError:
            # Command interrupted, logfile already deleted
            return

    def stop(self):
        self.stopped = True


def run(*args, verbose=False, **kwargs):
    if not verbose:
        return subprocess.run([cli_path, *args], **kwargs)
    with tempfile.NamedTemporaryFile(
        mode='w', encoding='utf8', suffix='.log'
    ) as tmp_file:
        tail_thread = TailThread(
            target=tail.log_tail,
            args=(tmp_file.name,),
            kwargs={'until': 2},
        )
        tail_thread.start()
        proc = subprocess.run(
            [cli_path, *args, f'--redirect={tmp_file.name}'], **kwargs
        )
        tail_thread.stop()
    return proc

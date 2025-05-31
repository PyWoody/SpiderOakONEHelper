import subprocess

from spideroak import cli_path
from spideroak.utils import Verbosity


def shutdown(verbose=Verbosity.NORMAL):
    proc = subprocess.run(
        [cli_path, '--shutdown'],
        capture_output=False if verbose is Verbosity.NONE else True
    )
    if proc.returncode != 0:
        raise Exception('Was not able to initiate shutdown')
    if proc.stderr:
        raise Exception(proc.stderr.decode('utf8', errors='replace'))
    print(proc.stdout.decode('utf8', errors='replace'))


if __name__ == '__main__':
    shutdown()

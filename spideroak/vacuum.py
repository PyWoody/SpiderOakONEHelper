import subprocess

from spideroak import cli_path
from spideroak.utils import Verbosity


def vacuum(verbose=Verbosity.NORMAL):
    proc = subprocess.run(
        [cli_path, '--vacuum'],
        capture_output=False if verbose is Verbosity.NONE else True
    )
    if proc.returncode != 0:
        raise Exception("Unable to run 'vacuum'")
    if verbose is not Verbosity.NONE:
        print(proc.stdout.decode('utf8', errors='replace'))


if __name__ == '__main__':
    vacuum()

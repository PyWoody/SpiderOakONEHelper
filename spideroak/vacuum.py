from spideroak import command
from spideroak.utils import Verbosity


def vacuum(*, verbose=Verbosity.NORMAL):
    proc = command.run(
        '--vacuum',
        capture_output=False if verbose is Verbosity.NONE else True
    )
    if proc.returncode != 0:
        raise Exception("Unable to run 'vacuum'")
    if verbose is not Verbosity.NONE and proc.stdout:
        print(proc.stdout.decode('utf8', errors='replace'))

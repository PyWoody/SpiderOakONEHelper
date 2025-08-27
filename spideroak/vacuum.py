from spideroak import command
from spideroak.utils import Verbosity


def vacuum(*, verbose=Verbosity.NORMAL):
    proc = command.run('--vacuum')
    if proc.returncode != 0:
        raise Exception("Unable to run 'vacuum'")
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if stdout == 'program is already running, taking no action':
        raise Exception(stdout)
    if verbose is not Verbosity.NONE and stdout:
        print(stdout)

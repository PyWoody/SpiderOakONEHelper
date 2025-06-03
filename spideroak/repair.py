from spideroak import command
from spideroak.utils import Verbosity


def repair(*, verbose=Verbosity.NORMAL):
    proc = command.run(
        '--repair',
        redirect_stdout=False if verbose is Verbosity.NONE else True
    )
    if proc.returncode != 0:
        raise Exception('Was not able to initiate repair')

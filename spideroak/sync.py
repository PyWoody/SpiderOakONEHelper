from spideroak import command
from spideroak.utils import Verbosity


def sync(verbose=Verbosity.NONE):
    proc = command.run(
        '--sync',
        verbose=False if verbose is Verbosity.NONE else True,
    )
    if proc.returncode != 0:
        raise Exception('Was not able to initiate sync')


if __name__ == '__main__':
    sync()

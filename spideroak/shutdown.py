from spideroak import command
from spideroak.utils import Verbosity


def shutdown(*, yes=False, verbose=Verbosity.NORMAL):
    if not yes:
        response = input(
            'Shutting down a running SpiderOakONE application may lead to '
            'lost data and incomplete syncs. Are you sure you wish to '
            'continue? (y/N) |> '
        )
        if response.lower().strip() != 'y':
            print('Aborting shutdown')
            return
    proc = command.run(
        '--shutdown',
        capture_output=False if verbose is Verbosity.NONE else True
    )
    if proc.returncode != 0:
        raise Exception('Was not able to initiate shutdown')
    if proc.stderr:
        raise Exception(proc.stderr.decode('utf8', errors='replace'))
    if proc.stdout:
        print(proc.stdout.decode('utf8', errors='replace'))

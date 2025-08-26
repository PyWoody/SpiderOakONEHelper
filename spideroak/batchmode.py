from spideroak import command, utils


def batchmode(*, verbose=utils.Verbosity.NONE):
    if verbose is not utils.Verbosity.NONE:
        proc = command.run('--batchmode', '--verbose', redirect_stdout=True)
    else:
        proc = command.run('--batchmode')
    if proc.returncode != 0:
        raise Exception('Batchmode failed')
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if stdout == 'program is already running, taking no action':
        raise Exception(stdout)
    return True

from spideroak import command, utils


def headless(*, verbose=utils.Verbosity.NONE):
    if verbose is not utils.Verbosity.NONE:
        proc = command.run('--headless', '--verbose', redirect_stdout=True)
    else:
        proc = command.run('--headless')
    if proc.returncode != 0:
        raise Exception('Headless failed')
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if stdout == 'program is already running, taking no action':
        raise Exception(stdout)

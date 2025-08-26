from spideroak import command, utils


def rebuild(*, verbose=utils.Verbosity.NONE):
    if verbose is not utils.Verbosity.NONE:
        proc = command.run(
            '--rebuild-reference-database', '--verbose', redirect_stdout=True
        )
    else:
        proc = command.run('--rebuild-reference-database')
    if proc.returncode != 0:
        raise Exception('rebuild failed')
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if stdout == 'program is already running, taking no action':
        raise Exception(stdout)

from spideroak import command, utils


def rebuild(verbose=utils.Verbosity.NONE):
    if verbose is not utils.Verbosity.NONE:
        proc = command.run(
            '--rebuild-reference-database', '--verbose', redirect_stdout=True
        )
    else:
        proc = command.run('--rebuild-reference-database')
    if proc.returncode != 0:
        raise Exception('rebuild failed')

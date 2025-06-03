from spideroak import command, utils


def build(verbose=utils.Verbosity.NONE):
    if verbose is not utils.Verbosity.NONE:
        proc = command.run('--build', '--verbose', redirect_stdout=True)
    else:
        proc = command.run('--build')
    if proc.returncode != 0:
        raise Exception('build failed')

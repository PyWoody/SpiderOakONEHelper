from spideroak import command, utils


def batchmode(*, verbose=utils.Verbosity.NONE):
    if verbose is not utils.Verbosity.NONE:
        proc = command.run('--batchmode', '--verbose', redirect_stdout=True)
    else:
        proc = command.run('--batchmode')
    if proc.returncode != 0:
        raise Exception('Batchmode failed')

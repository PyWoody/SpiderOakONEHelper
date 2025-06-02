from spideroak import command, utils


def headless(verbose=utils.Verbosity.NONE):
    if verbose is not utils.Verbosity.NONE:
        proc = command.run('--headless', '--verbose', redirect_stdout=True)
    else:
        proc = command.run('--headless')
    if proc.returncode != 0:
        raise Exception('Headless failed')

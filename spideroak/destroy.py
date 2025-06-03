from spideroak import command, utils


def destroy(*, yes=False, verbose=utils.Verbosity.NONE):
    if not yes:
        response = input(
            'Running this operation will destroy the upload shelf for the '
            'installation on this machine. Are you sure you want to '
            'continue? (y/N) |> '
        )
        if response.strip().lower() != 'y':
            print('Aborting destroying shelf')
            return
    if verbose is not utils.Verbosity.NONE:
        proc = command.run(
            '--destroy-shelved-x', '--verbose', redirect_stdout=True
        )
    else:
        proc = command.run('--destroy-shelved-x')
    if proc.returncode != 0:
        raise Exception('destroy failed')

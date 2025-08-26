import os

from spideroak import command
from spideroak.utils import Verbosity


# NOTE: Ratelimit this to 150 connections (attempts?) per hour
#       Filepaths are difficult cross OSes
#           Maybe use userinfo.txt to do normalization?
#           Also accept journal numbers

def restore(device, filepath, /, *, output=None, verbose=Verbosity.NONE):
    if output is None:
        output = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'restored',
        )
    os.makedirs(output, exist_ok=True)
    proc = command.run(
        f'--device={device}',
        f'--restore={filepath}',
        f'--output={output}',
        '--verbose' if verbose is Verbosity.HIGH else '',
        redirect_stdout=True if verbose is Verbosity.HIGH else False,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise Exception(f'Was not able to restore {filepath}')
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if stdout == 'program is already running, taking no action':
        raise Exception(stdout)
    if 'No journals for ' in stdout or 'does not exist ' in stdout:
        return False
    return True


def restore_paths(device, paths, /, *, output=None, verbose=Verbosity.NORMAL):
    for i, f in enumerate(paths, start=1):
        if verbose is not Verbosity.NONE:
            print(f'[] ({i}/{len(paths)}) Restoring {f}', end='\r', flush=True)
        success = restore(device, f, output=output, verbose=verbose)
        if verbose is not Verbosity.NONE:
            if success:
                print(f'[*] ({i}/{len(paths)}) Restored {f}')
            else:
                print(f'[!] ({i}/{len(paths)}) Not Restored {f}')


def restore_paths_from_file(
    device, filepath, /, *, output=None, verbose=Verbosity.NORMAL
):
    if os.path.splitext(filepath)[1].lower() != '.txt':
        raise Exception('Only .txt files are supported at the moment.')
    with open(filepath, 'r', encoding='utf8') as f:
        paths = [i.strip() for i in f if i.strip()]
    restore_paths(device, paths, output=output, verbose=verbose)

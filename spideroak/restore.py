import os

from spideroak import command
from spideroak.utils import Verbosity


# NOTE: Ratelimit this to 150 connections (attempts?) per hour
#       Filepaths are difficult cross OSes
#           Maybe use userinfo.txt to do normalization?
#           Also accept journal numbers

def restore(device, filepath, output=None, verbose=Verbosity.NONE):
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
        verbose=True if verbose is Verbosity.HIGH else False,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise Exception(f'Was not able to restore {filepath}')
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if 'No journals for ' in stdout or 'does not exist ' in stdout:
        return False
    return True


def restore_files(device, files, output=None, verbose=Verbosity.NORMAL):
    end = '\n' if verbose is Verbosity.HIGH else '\r'
    for i, f in enumerate(files, start=1):
        if verbose is not Verbosity.NONE:
            print(f'[] ({i}/{len(files)}) Restoring {f}', end=end, flush=True)
        if restore(device, f, output=output, verbose=verbose):
            if verbose is not Verbosity.NONE:
                print(f'[*] ({i}/{len(files)}) Restored {f}')
        else:
            if verbose is not Verbosity.NONE:
                print(f'[!] ({i}/{len(files)}) Not Restored {f}')


def restore_files_from_file(
    device, filepath, output=None, verbose=Verbosity.NORMAL
):
    if os.path.splitext(filepath)[1].lower() != '.txt':
        raise Exception('Only .txt files are supported at the moment.')
    with open(filepath, 'r', encoding='utf8') as f:
        files = [i.strip() for i in f if i.strip()]
    restore_files(device, files, output=output, verbose=verbose)

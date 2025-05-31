import os
import subprocess

from spideroak import cli_path
from spideroak.utils import Verbosity


# NOTE: Ratelimit this to 150 connections (attempts?) per hour
#       Filepaths are difficult cross OSes
#           Maybe use userinfo.txt to do normalization?
#           Also accept journal numbers

def restore(device, filepath, output=None):
    if output is None:
        output = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'restored',
        )
    os.makedirs(output, exist_ok=True)
    proc = subprocess.run(
        [
            cli_path,
            f'--device={device}',
            f'--restore={filepath}',
            f'--output={output}',
        ], capture_output=True
    )
    if proc.returncode != 0:
        raise Exception(f'Was not able to restore {filepath}')
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if stdout == (
        f"No journals for u'{filepath}' were found in the backup tree."
    ):
        return False
    return True


def restore_files(device, files, output=None, verbose=Verbosity.NORMAL):
    for i, f in enumerate(files, start=1):
        if verbose is not Verbosity.NONE:
            print(f'[] ({i}/{len(files)}) Restoring {f}', end='\r', flush=True)
        if restore(device, f, output=output):
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

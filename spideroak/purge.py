import os
import subprocess

from spideroak import cli_path
from spideroak.utils import Verbosity


def purge(device, filepath):
    proc = subprocess.run(
        [
            cli_path,
            f'--device={device}',
            f'--purge={filepath}',
        ], capture_output=True
    )
    if proc.returncode != 0:
        raise Exception(f'Was not able to purge {filepath}')
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if stdout == (
        f"No journals for u'{filepath}' were found in the backup tree."
    ):
        return False
    return True


def purge_files(device, files, verbose=Verbosity.NORMAL):
    for i, f in enumerate(files, start=1):
        if verbose is not Verbosity.NONE:
            print(f'[] ({i}/{len(files)}) Purging {f}', end='\r', flush=True)
        if purge(device, f):
            if verbose is not Verbosity.NONE:
                print(f'[*] ({i}/{len(files)}) Purged {f}')
        else:
            if verbose is not Verbosity.NONE:
                print(f'[!] ({i}/{len(files)}) Not Purged {f}')


def purge_files_from_file(device, filepath, verbose=Verbosity.NORMAL):
    if os.path.splitext(filepath)[1].lower() != '.txt':
        raise Exception('Only .txt files are supported at the moment.')
    with open(filepath, 'r', encoding='utf8') as f:
        files = [i.strip() for i in f if i.strip()]
    purge_files(device, files, verbose=verbose)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device', required=True, type=int)
    parser.add_argument('-f', '--files', nargs='+')
    parser.add_argument('--filepath')
    args = parser.parse_args()

    if args.files:
        purge_files(args.device, args.files)
    if args.filepath:
        purge_files_from_file(args.device, args.filepath)

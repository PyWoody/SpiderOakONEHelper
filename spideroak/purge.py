import os

from spideroak import command
from spideroak.utils import Verbosity


def purge(device, filepath, verbose=Verbosity.NONE):
    proc = command.run(
        f'--device={device}',
        f'--purge={filepath}',
        '--verbose' if verbose is Verbosity.HIGH else '',
        redirect_stdout=True if verbose is Verbosity.HIGH else False,
        capture_output=True,
    )
    if proc.returncode != 0:
        raise Exception(f'Was not able to purge {filepath}')
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if 'No journals for ' in stdout or 'does not exist ' in stdout:
        return False
    return True


def purge_files(device, files, verbose=Verbosity.NORMAL):
    end = '\n' if verbose is Verbosity.HIGH else '\r'
    for i, f in enumerate(files, start=1):
        if verbose is not Verbosity.NONE:
            print(f'[] ({i}/{len(files)}) Purging {f}', end=end, flush=True)
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

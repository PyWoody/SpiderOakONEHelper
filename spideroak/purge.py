import os

from spideroak import command
from spideroak.utils import Verbosity


YES_TO_ALL = False
QUIT = False


def purge(device, filepath, yes=False, verbose=Verbosity.NONE):
    global YES_TO_ALL, QUIT
    if not yes and not YES_TO_ALL:
        while True:
            response = input(
                'Running this operation will recursively and '
                f'permanently remove {filepath} and all files under '
                'its location.\nAre you sure you wish to continue?\n'
                '[y] Yes  [n] No  [A] Yes to All  [q] Quit |> '
            ).strip()
            if response == 'y':
                break
            elif response == 'n':
                return
            elif response == 'q':
                QUIT = True
                print('Aborting purge operation')
                return
            elif response == 'A':
                YES_TO_ALL = True
                break
            else:
                print(f'\n"{response}" is not an acceptable response\n')
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


def purge_files(device, files, yes=False, verbose=Verbosity.NORMAL):
    end = '\n' if verbose is Verbosity.HIGH else '\r'
    for i, f in enumerate(files, start=1):
        if QUIT:
            return
        if verbose is not Verbosity.NONE:
            print(f'[] ({i}/{len(files)}) Purging {f}', end=end, flush=True)
        success = purge(device, f, yes=yes)
        if verbose is not Verbosity.NONE:
            if success:
                print(f'[*] ({i}/{len(files)}) Purged {f}')
            else:
                print(f'[!] ({i}/{len(files)}) Not Purged {f}')


def purge_files_from_file(
    device, filepath, yes=False, verbose=Verbosity.NORMAL
):
    if os.path.splitext(filepath)[1].lower() != '.txt':
        raise Exception('Only .txt files are supported at the moment.')
    with open(filepath, 'r', encoding='utf8') as f:
        files = [i.strip() for i in f if i.strip()]
    purge_files(device, files, yes=yes, verbose=verbose)

import os

from spideroak import command
from spideroak.batchmode import batchmode as batchmode_cmd
from spideroak.utils import Verbosity


YES_TO_ALL = False
QUIT = False


def purge(device, filepath, /, *, yes=False, verbose=Verbosity.NONE):
    global YES_TO_ALL, QUIT
    if not yes and not YES_TO_ALL:
        while True:
            response = input(
                '\nRunning this operation will recursively and '
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
    )
    if proc.returncode != 0:
        raise Exception(f'Was not able to purge {filepath}')
    stdout = proc.stdout.decode('utf8', errors='replace').strip()
    if stdout == 'program is already running, taking no action':
        raise Exception(stdout)
    if 'No journals for ' in stdout or 'does not exist ' in stdout:
        return False
    return True


def purge_paths(
    device, paths, /, *, batchmode=False, yes=False, verbose=Verbosity.NORMAL
):
    for i, f in enumerate(paths, start=1):
        if QUIT:
            return
        if verbose is not Verbosity.NONE:
            print(f'[] ({i}/{len(paths)}) Purging {f}', end='\r', flush=True)
        success = purge(device, f, yes=yes)
        if verbose is not Verbosity.NONE:
            if success:
                print(f'[*] ({i}/{len(paths)}) Purged {f}')
            else:
                print(f'[!] ({i}/{len(paths)}) Not Purged {f}')
        if batchmode:
            try:
                batchmode_cmd()
            except Exception:
                print('Batchmode failed')


def purge_paths_from_file(
    device,
    filepath,
    /,
    *,
    batchmode=False,
    yes=False,
    verbose=Verbosity.NORMAL,
):
    if os.path.splitext(filepath)[1].lower() != '.txt':
        raise Exception('Only .txt files are supported at the moment.')
    with open(filepath, 'r', encoding='utf8') as f:
        paths = [i.strip() for i in f if i.strip()]
    purge_paths(device, paths, yes=yes, verbose=verbose, batchmode=batchmode)

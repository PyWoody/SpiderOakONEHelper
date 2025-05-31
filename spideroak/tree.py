import os
import re
import subprocess

from spideroak import cli_path
from spideroak.utils import Verbosity


def build(device, update=False, verbose=Verbosity.NORMAL):
    if verbose is not Verbosity.NONE:
        print(f'[] Generating TREE for {device}...', end='\r', flush=True)
    root = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'files'
    )
    output = os.path.join(root, f'{device}_tree.txt')
    if not update and os.path.isfile(output):
        if verbose is not Verbosity.NONE:
            print(f'[!] TREE exists for {device}.Skipping.')
        return
    os.makedirs(root, exist_ok=True)
    proc = subprocess.run(
        [
            cli_path,
            f'--device={device}',
            '--tree',
            f'--redirect={output}',
        ]
    )
    if proc.returncode != 0:
        raise Exception(f'Was not able to build a tree for {device}')
    if verbose is not Verbosity.NONE:
        print(f'[*] Generated TREE for {device}   ')


def clean(device, verbose=Verbosity.NORMAL):
    if verbose is not Verbosity.NONE:
        print(f'[] Cleaning TREE for {device}...', end='\r', flush=True)
    root = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'files'
    )
    output = os.path.join(root, f'{device}_tree.txt')

    trunk_re = re.compile(r'^trunk:\s+\d+:\s+(.*)\n$')
    delete_re = re.compile(r'^deleted_branch_\d+:\s+\d+:\s+(.*)\n$')
    deleted_branches = set()

    with open(output, 'r', encoding='utf8') as in_f:
        for line in in_f:
            if match := delete_re.search(line):
                deleted_branches.add(match.group(1))
        _ = in_f.seek(0)
        with open(f'{output}.tmp', 'w', encoding='utf8') as out_f:
            for line in in_f:
                if match := trunk_re.search(line):
                    trunk = match.group(1)
                    if trunk not in deleted_branches:
                        _ = out_f.write(trunk)
                        _ = out_f.write('\n')
    os.replace(f'{output}.tmp', output)
    if verbose is not Verbosity.NONE:
        print(f'[*] Cleaned TREE for {device}   ')

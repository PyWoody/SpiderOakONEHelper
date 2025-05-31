import os
import subprocess

from spideroak import cli_path, utils


def build(device, verbose=utils.Verbosity.NORMAL):
    if verbose is not utils.Verbosity.NONE:
        print(f'[] Generating FULLLIST for {device}...', end='\r', flush=True)
    root = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'files'
    )
    os.makedirs(root, exist_ok=True)
    output = os.path.join(root, f'{device}_full.txt')
    proc = subprocess.run(
        [
            cli_path,
            f'--device={device}',
            '--fulllist',
            f'--redirect={output}',
        ]
    )
    if proc.returncode != 0:
        raise Exception(f'Was not able to build a FULLLIST for {device}')
    if verbose is not utils.Verbosity.NONE:
        print(f'[*] Generated FULLLIST for {device}   ')
        print(f'[] Cleaning FULLLIST for {device}...', end='\r', flush=True)
    with open(f'{output}.tmp', 'w', encoding='utf8') as tmp:
        with open(output, 'r', encoding='utf8') as f:
            for line in f:
                if not line.startswith('deleted_branch'):
                    _ = tmp.write(line)
    os.replace(f'{output}.tmp', output)
    if verbose is not utils.Verbosity.NONE:
        print(f'[*] Cleaned FULLLIST for {device}   ')

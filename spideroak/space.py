import subprocess

from spideroak import cli_path


def space():
    proc = subprocess.run([cli_path, '--space'], capture_output=True)
    if proc.returncode != 0:
        raise Exception('Was not able to initiate space')
    print(proc.stdout.decode('utf8', errors='replace'))


if __name__ == '__main__':
    space()

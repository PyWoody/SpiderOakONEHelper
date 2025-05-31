import subprocess

from spideroak import cli_path


def sync():
    proc = subprocess.run([cli_path, '--sync'])
    if proc.returncode != 0:
        raise Exception('Was not able to initiate sync')


if __name__ == '__main__':
    sync()

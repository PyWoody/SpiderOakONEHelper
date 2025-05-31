import subprocess

from spideroak import cli_path


def headless():
    proc = subprocess.run([cli_path, '--headless'])
    if proc.returncode != 0:
        raise Exception('Was not able to initiate headless')


if __name__ == '__main__':
    headless()

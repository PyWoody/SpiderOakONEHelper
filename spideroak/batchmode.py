import subprocess

from spideroak import cli_path


def batchmode():
    proc = subprocess.run([cli_path, '--batchmode'])
    if proc.returncode != 0:
        raise Exception('Was not able to initiate batchmode')


if __name__ == '__main__':
    batchmode()

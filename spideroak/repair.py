import subprocess

from spideroak import cli_path


def repair():
    proc = subprocess.run([cli_path, '--repair'])
    if proc.returncode != 0:
        raise Exception('Was not able to initiate repair')


if __name__ == '__main__':
    repair()

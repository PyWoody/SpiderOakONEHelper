import subprocess

from spideroak import cli_path


def spideroak_help():
    proc = subprocess.run([cli_path, '--help'], capture_output=True)
    if proc.returncode != 0:
        raise Exception('Was not able to run help')
    print(proc.stdout.decode('utf8', errors='replace'))


if __name__ == '__main__':
    spideroak_help()

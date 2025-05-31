import subprocess

from spideroak import cli_path


def userinfo():
    proc = subprocess.run([cli_path, '--userinfo'], capture_output=True)
    if proc.returncode != 0:
        raise Exception(proc.stderr.decode('utf8', errors='replace').strip())
    print(proc.stdout.decode('utf8', errors='replace'))


if __name__ == '__main__':
    userinfo()

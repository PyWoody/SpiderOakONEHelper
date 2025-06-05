from spideroak import command


def version():
    proc = command.run('--version', capture_output=True)
    if proc.returncode != 0:
        raise Exception('Was not able to run --version for SpiderOakONE')
    print(proc.stdout.decode('utf8', errors='replace'))

from spideroak import command


def space():
    proc = command.run('--space')
    if proc.returncode != 0:
        raise Exception('Was not able to initiate space')
    print(proc.stdout.decode('utf8', errors='replace'))

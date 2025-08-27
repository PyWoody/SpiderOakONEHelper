from spideroak import command


def userinfo():
    proc = command.run('--userinfo')
    if proc.returncode != 0:
        raise Exception('Failed to generate userinfo')
    print(proc.stdout.decode('utf8', errors='replace'))

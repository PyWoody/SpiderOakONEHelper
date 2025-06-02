from spideroak import command


def userinfo():
    proc = command.run('--userinfo', capture_output=True)
    if proc.returncode != 0:
        raise Exception('Failed to generate userinfo')
    print(proc.stdout.decode('utf8', errors='replace'))


if __name__ == '__main__':
    userinfo()

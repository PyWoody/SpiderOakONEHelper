from spideroak import command


def spideroak_help():
    proc = command.run('--help', capture_output=True)
    if proc.returncode != 0:
        raise Exception('Was not able to run --help for SpiderOakONE')
    print(proc.stdout.decode('utf8', errors='replace'))

import os

from spideroak import command, utils, tail


def build(device, /, *, verbose=utils.Verbosity.NORMAL):
    if verbose is not utils.Verbosity.NONE:
        print(f'[] Generating FULLLIST for {device}...', end='\r', flush=True)
    root = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'files'
    )
    os.makedirs(root, exist_ok=True)
    output = os.path.join(root, f'{device}_full.txt')
    if verbose is utils.Verbosity.HIGH:
        tail_thread = tail.TailThread(
            target=tail.log_tail,
            args=(output,),
            kwargs={'sleep': .5, 'until': 2},
        )
        tail_thread.start()
    else:
        tail_thread = None
    try:
        proc = command.run(
            f'--device={device}', '--fulllist', f'--redirect={output}',
        )
    except Exception as e:
        if tail_thread is not None:
            tail_thread.stop()
            tail_thread.join()
        raise e from None
    if verbose is utils.Verbosity.HIGH:
        tail_thread.completed()
        tail_thread.join()  # Prevents re-reading updated version
    if proc.returncode != 0:
        raise Exception(f'Was not able to build a FULLLIST for {device}')
    if verbose is not utils.Verbosity.NONE:
        print(f'[*] Generated FULLLIST for {device}   ')
        print(f'[] Cleaning FULLLIST for {device}...', end='\r', flush=True)
    with open(f'{output}.tmp', 'w', encoding='utf8') as tmp:
        with open(output, 'r', encoding='utf8') as f:
            for line in f:
                if not line.startswith('deleted_branch'):
                    _ = tmp.write(line)
    os.replace(f'{output}.tmp', output)
    if verbose is not utils.Verbosity.NONE:
        print(f'[*] Cleaned FULLLIST for {device}   ')

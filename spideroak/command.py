import subprocess
import tempfile

from spideroak import cli_path, tail


def run(*args, verbose=False, **kwargs):
    if not verbose:
        return subprocess.run([cli_path, *args], **kwargs)
    with tempfile.NamedTemporaryFile(
        mode='w', encoding='utf8', suffix='.log'
    ) as tmp_file:
        tail_thread = tail.TailThread(
            target=tail.log_tail,
            args=(tmp_file.name,),
            kwargs={'until': 2},
        )
        tail_thread.start()
        try:
            proc = subprocess.run(
                [cli_path, *args, f'--redirect={tmp_file.name}'], **kwargs
            )
        except Exception as e:
            tail_thread.stop()
            raise e from None
        else:
            tail_thread.completed()
        finally:
            tail_thread.join()
        if kwargs.get('capture_output'):
            proc.stdout = open(tmp_file.name, 'rb').read()
    return proc

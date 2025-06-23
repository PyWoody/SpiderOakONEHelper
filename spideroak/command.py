import os
import subprocess
import tempfile

from spideroak import cli_path, tail


def run(*args, redirect_stdout=False, **kwargs):
    if not redirect_stdout:
        return subprocess.run([cli_path, *args], **kwargs)
    tmp_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode='w', encoding='utf8', suffix='.log', dir=tmp_dir,
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
        if kwargs.get('capture_output') and not proc.stdout:
            proc.stdout = open(tmp_file.name, 'rb').read()
    return proc

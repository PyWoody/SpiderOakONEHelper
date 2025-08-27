import os
import subprocess
import tempfile

from spideroak import cli_path, tail, _system


def run(*args, redirect_stdout=False, capture_output=True, **kwargs):
    if not redirect_stdout:
        return subprocess.run(
            [cli_path, *args], capture_output=capture_output, **kwargs
        )
    delete = False if _system == 'Windows' else True
    try:
        with tempfile.NamedTemporaryFile(
            mode='w', encoding='utf8', suffix='.log', delete=delete
        ) as tmp_file:
            try:
                tail_thread = tail.TailThread(
                    target=tail.log_tail,
                    args=(tmp_file.name,),
                    kwargs={'until': 2},
                )
                tail_thread.start()
                proc = subprocess.run(
                    [cli_path, *args, f'--redirect={tmp_file.name}'],
                    capture_output=capture_output,
                    **kwargs,
                )
            except (KeyboardInterrupt, Exception) as e:
                tail_thread.stop()
                raise e from None
            else:
                tail_thread.completed()
            finally:
                tail_thread.join()
            if kwargs.get('capture_output') and not proc.stdout:
                proc.stdout = open(tmp_file.name, 'rb').read()
    finally:
        try:
            os.remove(tmp_file.name)
        except (FileNotFoundError, PermissionError):
            pass
    return proc

import platform

_system = platform.system()

if _system == 'Windows':
    cli_path = r'C:\Program Files\SpiderOakONE\SpiderOakONE.exe'
elif _system == 'Darwin':
    cli_path = r'/Applications/SpiderOakONE.app/Contents/MacOS/SpiderOakONE'
else:
    import shutil
    cli_path = shutil.which('SpiderOakONE')
    if cli_path is None:
        raise Exception('Could not discern SpiderOakONE path.')

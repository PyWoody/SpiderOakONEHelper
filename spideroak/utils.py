import enum
import os


class Verbosity(enum.Enum):
    NONE = enum.auto()
    NORMAL = enum.auto()
    HIGH = enum.auto()


def logdir():
    possible_paths = [
        os.path.expanduser(r'~/Library/Application Support/SpiderOakONE'),
        os.path.expanduser(r'~/.config/SpiderOakONE/'),
        os.path.join(
            os.path.expandvars('%LOCALAPPDATA%'), 'SpiderOak', 'SpiderOakONE'
        ),
    ]
    if path := next((i for i in possible_paths if os.path.isdir(i)), None):
        return path
    raise Exception('Could not locate log directory')

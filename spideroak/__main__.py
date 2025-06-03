import argparse
import os

from spideroak import (
    batchmode,
    build,
    destroy,
    fulllist,
    headless,
    heap,
    purge,
    restore,
    tree,
    tail,
    userinfo,
    utils,
    rebuild,
    repair,
    shutdown,
    space,
    spideroak_help,
    sync,
    vacuum
)


parser = argparse.ArgumentParser(
    prog='spideroak',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
    A selection of SpiderOakONE command line utilities.

    Run `python3 -m spideroak spideroakhelp` for the official SpiderOakONE help.

    Run `python3 -m spideroak utils --cli-location` to find your locally
    installed SpiderOakONE executable location.
    '''  # noqa: E501
)

update_parser = argparse.ArgumentParser(add_help=False)
update_parser.add_argument(
    '--update',
    action='store_true',
    default=False,
    help='Flag for updating existing output files. Default is False'
)


output_parser = argparse.ArgumentParser(add_help=False)
output_parser.add_argument(
    '--output', help='Output location for saved, downloaded, or restored items.'
)

verbose_parser = argparse.ArgumentParser(add_help=False)
verbose_parser.add_argument(
    '-v',
    default=0,
    action='count',
    help='Flag for verbosity level. '
         'Setting multiple times increases verbosity, e.g, -vv. '
         'Default is Verbosity.NONE (0)'
)

yes_parser = argparse.ArgumentParser(add_help=False)
yes_parser.add_argument(
    '-y',
    '--yes',
    default=False,
    action='store_true',
    help='Flag for automatically approving any and all actions without prompt',
)


subparsers = parser.add_subparsers(
    dest='command',
    title='Commands',
    metavar='Enter {command} -h/--help for additional information'
)

batchmode_parser = subparsers.add_parser(
    'batchmode',
    help='Initiates batchmode',
    description='Like headless, but will exit when all '
                'available work is done.',
    parents=[verbose_parser],
)

build_parser = subparsers.add_parser(
    'build',
    help='Initiates build',
    description='Scans the filesystem and builds all possible file system '
                'changes as shelved upload transactions. Exits without '
                'uploading them',
    parents=[verbose_parser],
)

destroy_parser = subparsers.add_parser(
    'destroy',
    help='Clear the queue of all transactions',
    description='Clear the queue of all transactions, including file uploads. '
                'It is suggested to run --rebuild after this completes. '
                'You may then need to run --batchmode or --headless after '
                'completion to re-sync your local installation',
    parents=[verbose_parser, yes_parser],
)

fulllist_parser = subparsers.add_parser(
    'fulllist',
    help='Save all directories and files stored on device to file',
    description='Save all directories and files stored on device to file',
    parents=[verbose_parser, update_parser],
)
fulllist_parser.add_argument('device')

heap_parser = subparsers.add_parser(
    'heap',
    help='Utility to find files to remove',
    description='A helpful utility for finding large files, directories with '
                'a large number of files, or files with a high number of '
                'historical versions. This can be useful for finding files '
                'to purge.',
)
heap_parser.add_argument(
    'device_or_file',
    help='Device number or filepath for existing fulllist output',
)
heap_parser.add_argument(
    '--len',
    action='store_true',
    default=False,
    help='Sort by number of files in each directory',
)
heap_parser.add_argument(
    '--size',
    action='store_true',
    default=False,
    help='Sort by largest file size',
)
heap_parser.add_argument(
    '--history',
    action='store_true',
    default=False,
    help='Sort by number of historical versions',
)

headless_parser = subparsers.add_parser(
    'headless',
    help='Initiates headless',
    description='Run in headless mode (without the graphical interface).',
    parents=[verbose_parser],
)

purge_parser = subparsers.add_parser(
    'purge',
    help='Purge files, folders from backups',
    description='Purge files, folders from backups. Note, SpiderOakONE '
         'will need to start up and shut down per use. It is highly '
         'suggested to delete directories from their lowest root level '
         'instead of deleting individual files or folders',
    parents=[verbose_parser, yes_parser],
)
purge_parser.add_argument(
    '-d',
    '--device',
    required=True,
    type=int,
    help='Device number that uploaded the item'
)
purge_parser.add_argument(
    '-f',
    '--files',
    nargs='+',
    help='Item or items separated by whitespace to be purged. '
         'All paths should be wrapped in quotations.'
)
purge_parser.add_argument(
    '--filepath',
    help='Filepath to a .txt file containing a list files or '
         'folders separated by newline to be purged'
)

restore_parser = subparsers.add_parser(
    'restore',
    help='Download files, folders from backups to disk',
    description='Restore (download) files, folders from backups to disk',
    parents=[verbose_parser, output_parser],
)
restore_parser.add_argument(
    '-d',
    '--device',
    required=True,
    type=int,
    help='Device number that uploaded the item'
)
restore_parser.add_argument(
    '-f',
    '--files',
    nargs='+',
    help='Item or items separated by whitespace to be restored (downloaded)'
         'All paths should be wrapped in quotations.'
)
restore_parser.add_argument(
    '--filepath',
    help='Filepath to a .txt file containing a list files or '
         'folders separated by newline to be restored (downloaded)'
)

tree_parser = subparsers.add_parser(
    'tree',
    help='Save the hierarchy of stored backup directories to file',
    description='Save the hierarchy of stored backup directories to file',
    parents=[verbose_parser, update_parser],
)
tree_parser.add_argument('devices', nargs='+')
tree_parser.add_argument(
    '--no-clean',
    action='store_true',
    default=False,
    help='If set, the output file will not have already deleted folders/files '
         'purged from the output'
)

vacuum_parser = subparsers.add_parser(
    'vacuum',
    help='Vacuum local database',
    description='Vacuums the local file database. '
                'SpiderOak will automatically perform this under '
                'certain situations.',
    parents=[verbose_parser],
)
userinfo_parser = subparsers.add_parser(
    'userinfo',
    help='Show current userinfo',
    description='Shows to console the current userinfo.'
)
utils_parser = subparsers.add_parser(
    'utils',
    help='SpiderOak specific utilities like CLI path, log locations, etc.',
    description='SpiderOak utilities like CLI path, log locations, etc.',
)
utils_parser.add_argument(
    '--cli-location',
    help='Shows CLI path for local installation',
    action='store_true',
    default=False,
)
utils_parser.add_argument(
    '--logs-location',
    help='Shows log path for local installation',
    action='store_true',
    default=False,
)

rebuild_parser = subparsers.add_parser(
    'rebuild',
    help='Rebuild the SpiderOakONE reference database',
    description='Rebuild the SpiderOakONE reference database, '
                'which may take a long time to complete',
    parents=[verbose_parser],
)

repair_parser = subparsers.add_parser(
    'repair',
    help='Repair a local SpiderOakONE installation.',
    description='Repair a local SpiderOakONE installation.',
    parents=[verbose_parser],
)

spideroakhelp_parser = subparsers.add_parser(
    'shutdown',
    help='Connects to a running SpiderOakONE instance and shuts it down',
    description='Connects to a running SpiderOakONE '
                'instance and shuts it down',
    parents=[verbose_parser, yes_parser],
)
space_parser = subparsers.add_parser(
    'space',
    help='Show space usage information by device',
    description='Show space usage information by device',
)

spideroakhelp_parser = subparsers.add_parser(
    'spideroakhelp',
    help="Show the message returned by SpiderOak's --help",
    description="Show the message returned by SpiderOak's --help",
)

sync_parser = subparsers.add_parser(
    'sync',
    help='Initiates sync',
    description='Like batchmode, but only backup/update synced directories.',
    parents=[verbose_parser],
)

tail_parser = subparsers.add_parser(
    'tail',
    help='Tail most recently modified logs',
    description='Automatically tails the most recently modified logfile. '
                'Will use `rich.print` if available on the system.'
)

args = parser.parse_args()

if not hasattr(args, 'v') or args.v <= 0:
    verbosity = utils.Verbosity.NONE
elif args.v == 1:
    verbosity = utils.Verbosity.NORMAL
else:
    verbosity = utils.Verbosity.HIGH

if args.command is None:
    parser.print_help()
elif args.command == 'vacuum':
    vacuum.vacuum(verbose=verbosity)
elif args.command == 'batchmode':
    batchmode.batchmode(verbose=verbosity)
elif args.command == 'build':
    build.build(verbose=verbosity)
elif args.command == 'destroy':
    destroy.destroy(verbose=verbosity, yes=args.yes)
elif args.command == 'headless':
    headless.headless(verbose=verbosity)
elif args.command == 'tail':
    tail.tail()
elif args.command == 'userinfo':
    userinfo.userinfo()
elif args.command == 'utils':
    if args.cli_location:
        from spideroak import cli_path
        print(cli_path)
    if args.logs_location:
        print(utils.logdir())
elif args.command == 'rebuild':
    rebuild.rebuild(verbose=verbosity)
elif args.command == 'repair':
    repair.repair(verbose=verbosity)
elif args.command == 'shutdown':
    shutdown.shutdown(verbose=verbosity, yes=args.yes)
elif args.command == 'space':
    space.space()
elif args.command == 'spideroakhelp':
    spideroak_help.spideroak_help()
elif args.command == 'sync':
    sync.sync(verbose=verbosity)
elif args.command == 'tree':
    for device in args.devices:
        tree.build(device, update=args.update, verbose=verbosity)
        if not args.no_clean:
            tree.clean(device, verbose=verbosity)
elif args.command == 'purge':
    if args.files:
        purge.purge_files(
            args.device, args.files, yes=args.yes, verbose=verbosity
        )
    if args.filepath:
        purge.purge_files_from_file(
            args.device, args.filepath, yes=args.yes, verbose=verbosity
        )
elif args.command == 'restore':
    if args.files:
        restore.restore_files(
            args.device,
            args.files,
            output=args.output,
            verbose=verbosity,
        )
    if args.filepath:
        restore.restore_files_from_file(
            args.device,
            args.filepath,
            output=args.output,
            verbose=verbosity,
        )
elif args.command == 'fulllist':
    fpath = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'files',
        f'{args.device}_full.txt'
    )
    if not os.path.isfile(fpath) or args.update:
        fulllist.build(args.device, verbose=verbosity)
elif args.command == 'heap':
    if os.path.isfile(args.device_or_file):
        fpath = args.device_or_filee
    else:
        fpath = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'files',
            f'{args.device_or_file}_full.txt'
        )
    if not os.path.isfile(fpath):
        print(
            f'No full list for {args.device}. '
            'Run `python -m spideroak fulllist {device}` first.'
        )
    else:
        if args.len:
            heap.by_len(fpath)
        if args.size:
            heap.by_size(fpath)
        if args.history:
            heap.by_history(fpath)

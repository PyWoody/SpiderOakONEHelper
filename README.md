This is an unofficial SpiderOakONE helper library for personal use. It is not affiliated with SpiderOak.


```
usage: spideroak [-h] Enter {command} -h/--help for additional information ...

    A selection of SpiderOakONE command line utilities.

    Run `python3 -m spideroak spideroakhelp` for the official SpiderOakONE help.

    Run `python3 -m spideroak utils --cli-location` to find your locally installed SpiderOakONE executable location.
    

options:
  -h, --help            show this help message and exit

Commands:
  Enter {command} -h/--help for additional information
    batchmode           Initiates batchmode
    fulllist            Save all directories and files stored on device to file
    heap                Utility to find files to remove
    headless            Initiates headless
    purge               Purge files, folders from backups
    restore             Download files, folders from backups to disk
    tree                Save the hierarchy of stored backup directories to file
    vacuum              Vacuum local database
    userinfo            Show current userinfo
    utils               SpiderOak specific utilities like CLI path, log locations, etc.
    repair              Repair a local SpiderOakONE installation.
    shutdown            Connects to a running SpiderOakONE instance and shuts it down
    space               Show space usage information by device
    spideroakhelp       Show the message returned by SpiderOak's --help
    sync                Initiates sync
    tail                Tail most recently modified logs
```

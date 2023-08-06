#!/usr/bin/env python
# -*- coding: utf-8 -*-


# pylint: disable=superfluous-parens


# Version should be updated based on http://semver.org/spec/v2.0.0.html
__version__ = '0.2.0'


from logging import getLogger as _getLogger
_logger = _getLogger('yarbs')  # pylint: disable=invalid-name


DEFAULT_BACKUPS_KEPT = 30
DEFAULT_RSYNC_COMMAND = 'rsync'
DEFAULT_VERBOSE = False
DEFAULT_COMPRESSION = False


def _get_backup_basename(source_dir):
    """
    Get the base name used to name destination directories.
    """

    from os.path import basename, dirname

    name = basename(source_dir)  # If specified as some/path.
    if (not name):  # If specified as some/path/.
        name = basename(dirname(source_dir))
    return name


def _get_backup_name(basename):
    """
    Create a name for a current backup, including timestamp suffix.
    """

    from datetime import datetime

    return "{}_{}".format(
        basename,
        datetime.now().replace(microsecond=0).isoformat().replace(':', '-'))


def _is_matching_backup_name(name, basename):
    """
    Check if an item is a backup of a specified base name.
    """

    from re import match

    # Date component ranges are ignored. Seconds also might not be needed to be used.
    return (match(basename + r'_\d{4}-\d{2}-\d{2}T\d{2}-\d{2}', name) is not None)


def _list_existing_backups(destination_dir, backup_basename):
    """
    List the paths of existing backups in the destination directory.
    """

    from os import listdir
    from os.path import join, isdir

    backup_paths = []
    for item_name in listdir(destination_dir):
        item_path = join(destination_dir, item_name)
        if (isdir(item_path) and
                _is_matching_backup_name(item_name, backup_basename)):
            backup_paths.append(item_path)
    return sorted(backup_paths)


def _remove_old_backups(existing_backups, backups_kept):
    """
    Remove old backups above the limit and one more to make space for
    a new backup.
    """

    from shutil import rmtree

    while (len(existing_backups) >= backups_kept):
        backup_path = existing_backups.pop(0)
        _logger.info("Removing old backup: %s", backup_path)
        rmtree(backup_path)


def _get_backup_path(destination_dir, backup_name):
    """
    Get a path to the specific backup.
    """

    from os.path import join

    return join(destination_dir, backup_name)


def _normalize_dir_path(path):
    """
    Normalize directory path to include separator ("/") at the end.
    """

    from os import sep

    if (path[-1] not in ['/', '\\']):
        path += sep
    return path


def _create_backup(
        source_dir, backup_path, previous_backup_path,
        verbose=DEFAULT_VERBOSE, rsync_command=DEFAULT_RSYNC_COMMAND,
        compression=DEFAULT_COMPRESSION):
    """
    Create a source directory backup to the specified path, optionally
    linking to a previous backup.
    """

    from subprocess import check_call
    from os.path import abspath

    switches = ['-i', '-a', '--delete']
    if (verbose):
        switches.append('-v')
    if (compression):
        switches.append('-z')
    if (previous_backup_path is not None):
        previous_backup_path = _normalize_dir_path(abspath(previous_backup_path))
        switches.append("--link-dest={}".format(previous_backup_path))

    source_dir = _normalize_dir_path(source_dir)
    backup_path = _normalize_dir_path(backup_path)
    check_call([rsync_command] + switches + [source_dir, backup_path])


def _check_if_root():
    """
    Check if running as root (required by some rsync settings).
    """

    from subprocess import check_output

    user = check_output('whoami').decode().strip()
    if (user != 'root'):
        raise RuntimeError('Process must be executed as root.')


def prepare(
        source_dir, destination_dir,
        backups_kept=DEFAULT_BACKUPS_KEPT):
    """
    TODO
    """

    from os.path import exists, abspath

    if (not exists(destination_dir)):
        raise AttributeError('Destination directory does not exist.')
    if (backups_kept < 1):
        raise AttributeError('Must keep at least one backup.')

    backup_basename = _get_backup_basename(source_dir)
    _logger.info("Preparing \"%s\" backup.", backup_basename)
    _logger.debug("Source dir: %s", source_dir)
    _logger.debug("Destination dir: %s", destination_dir)

    existing_backups = _list_existing_backups(destination_dir, backup_basename)
    _logger.debug("Found %d existing backup(s).", len(existing_backups))
    _remove_old_backups(existing_backups, backups_kept)

    backup_name = _get_backup_name(backup_basename)
    backup_path = _get_backup_path(destination_dir, backup_name)
    _logger.info("Backup dir: %s", backup_path)
    return (
        abspath(backup_path),
        abspath(existing_backups[-1]) if (existing_backups) else None)


def sync(
        source_dir, backup_path, previous_backup_path,
        rsync_command=DEFAULT_RSYNC_COMMAND, verbose=DEFAULT_VERBOSE,
        compression=DEFAULT_COMPRESSION):
    """
    TODO
    """

    from os.path import exists
    from shutil import rmtree

    _check_if_root()
    if (not exists(source_dir)):
        raise AttributeError('Source directory does not exist.')

    backup_basename = _get_backup_basename(source_dir)
    _logger.info("Syncing \"%s\" backup.", backup_basename)

    try:
        _create_backup(
            source_dir, backup_path,
            previous_backup_path,
            rsync_command=rsync_command, verbose=verbose,
            compression=compression)
        _logger.info("Finished \"%s\" backup.", backup_basename)
    except:
        _logger.error(
            # pylint: disable=W1201
            'An error was encountered or the process was interrupted. ' +
            'The unfinished backup will be removed...')
        rmtree(backup_path)
        raise


def backup(
        source_dir, destination_dir,
        backups_kept=DEFAULT_BACKUPS_KEPT, rsync_command=DEFAULT_RSYNC_COMMAND,
        verbose=DEFAULT_VERBOSE, compression=DEFAULT_COMPRESSION):
    """
    Create an incremental backup of a source directory to a new
    directory created under destination directory.

    Existing backups in the destination directory that are above the
    limit of backup to be kept are removed. Last backup made is used
    as a target for unchanged files to link to. This avoids both copying
    the unchanged files and saves space in the destination directory.

    The syncing uses -a and --delete rsync arguments. See "man rsync"
    for more details.

    Needs to be ran as root (e.g. with "sudo").

    source_dir -- Path to the backed-up directory.
    destination_dir -- Path to the directory containing backups.
    backups_kept -- Maximum number of backups to be kept.
    rsync_command -- Custom rsync executable path.
    verbose -- Enables higher rsync verbosity.
    compression -- Enables rsync transport compression.
    """

    backup_path, previous_backup_path = prepare(
        source_dir, destination_dir, backups_kept=backups_kept)
    sync(
        source_dir, backup_path, previous_backup_path,
        rsync_command=rsync_command, verbose=verbose,
        compression=compression)


def setup_logging(verbose=False):
    from logging import basicConfig, INFO, DEBUG

    basicConfig(
        level=(INFO if (not verbose) else DEBUG),
        format='%(levelname)-5s: %(message)s')


def _print_backup_dirs(backup_path, previous_backup_path):
    from json import dumps

    print(dumps({
        'backup_path': backup_path,
        'previous_backup_path': previous_backup_path,
        }))


def _read_backup_dirs():
    from json import load
    from sys import stdin

    backup_dirs = load(stdin)
    return (backup_dirs['backup_path'], backup_dirs['previous_backup_path'])



SOURCE_DIR_DESCRIPTION = 'Path or name of the backed-up directory.'
DESTINATION_DIR_DESCRIPTION = 'Path to the directory containing backups.'
BACKUPS_KEPT_DESCRIPTION = 'Maximum number of backups to be kept.'
def _parse_args(args=None):
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description='Create incremental backups using Rsync.')
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose mode.')
    parser.add_argument(
        '--version',
        action='version',
        version=__version__)

    subparsers = parser.add_subparsers(
        help='Performed action (typically "backup").',
        dest='action')

    backup_parser = subparsers.add_parser(
        'backup',
        help=(
            'Make space, find the latest backup and create a new ' +
            'backup.'))
    backup_parser.add_argument(
        'source_dir',
        help=SOURCE_DIR_DESCRIPTION)
    backup_parser.add_argument(
        'destination_dir',
        help=DESTINATION_DIR_DESCRIPTION)
    backup_parser.add_argument(
        '--backups_kept',
        type=int,
        default=DEFAULT_BACKUPS_KEPT,
        help=BACKUPS_KEPT_DESCRIPTION)
    backup_parser.add_argument(
        '--rsync_command',
        default=DEFAULT_RSYNC_COMMAND,
        help='Custom rsync executable path.')
    backup_parser.add_argument(
        '-c', '--compression',
        action='store_true',
        help='Apply compression.')

    prepare_parser = subparsers.add_parser(
        'prepare',
        help=(
            'Make space, find the latest backup and print the paths ' +
            'to stdout as JSON (no changes are made).'))
    prepare_parser.add_argument(
        'source_dir',
        help=SOURCE_DIR_DESCRIPTION)
    prepare_parser.add_argument(
        'destination_dir',
        help=DESTINATION_DIR_DESCRIPTION)
    prepare_parser.add_argument(
        '--backups_kept',
        type=int,
        default=DEFAULT_BACKUPS_KEPT,
        help=BACKUPS_KEPT_DESCRIPTION)

    sync_parser = subparsers.add_parser(
        'sync',
        help=(
            'Create a new backup using the provided paths to ' +
            'previous and new backup dirs.'))
    sync_parser.add_argument(
        'source_dir',
        help=SOURCE_DIR_DESCRIPTION)
    sync_parser.add_argument(
        'backup_path',
        type=str,
        nargs='?',
        help=(
            'Specific path of the new backup directory (read as JSON ' +
            'from stdin if unspecified).'))
    sync_parser.add_argument(
        'previous_backup_path',
        type=str,
        nargs='?',
        help=(
            'Specific path of the latest previous backup directory ' +
            '(read as JSON from stdin if unspecified).'))

    return parser.parse_args(args)


def main(args=None):
    config = _parse_args(args)
    setup_logging(config.verbose)
    if (config.action == 'backup'):
        backup(
            config.source_dir,
            config.destination_dir,
            config.backups_kept,
            config.rsync_command,
            config.verbose,
            config.compression)
    elif (config.action == 'prepare'):
        _print_backup_dirs(*prepare(
            config.source_dir,
            config.destination_dir,
            config.backups_kept))
    elif (config.action == 'sync'):
        backup_path = config.backup_path
        previous_backup_path = config.previous_backup_path
        if (backup_path is None or
                previous_backup_path is None):
            backup_path, previous_backup_path = _read_backup_dirs()
        sync(
            config.source_dir,
            backup_path,
            previous_backup_path)
    else:
        raise ValueError('Bad action.')


if (__name__ == '__main__'):
    main()

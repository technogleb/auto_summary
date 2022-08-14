import argparse
from pathlib import Path

from auto_summary.generate_summary import main


def run_parser():
    parser = argparse.ArgumentParser(
        'Provides CLI interface for Auto Summary\n'
        'Syntax: python3 cli.py -r <markdown_root> [--wikilinks|watch_changes|h]\n'
        'options:\n'
        '-r                 Path to the root of you markdown filetree, auto_summary \n'
        '                   recursively looks for markdown files starting from the root\n'
        '--wikilinks        Whether to use wikilinks links format\n'
        '--watch_changes    Whether to automatically update table of contents files,\n'
        '                   when any file is moved/renamed/deleted/created.\n'
        '                   Requires watchdog to be installed'
    )

    parser.add_argument(
        '-r', '--root', type=str, required=True,
        help='Path to the root folder, where top level summary will be located'
    )
    parser.add_argument(
        '--wikilinks', action='store_true',
        help='Whether to use wikilinks format or not. Default False'
    )
    parser.add_argument(
        '--watch_changes', action='store_true',
        help='Whether to automatically watch root for changes and run summarizer on each'
    )

    args = vars(parser.parse_args())
    args['root'] = Path(args['root']).resolve()

    watch_changes = args.pop('watch_changes')
    if watch_changes:
        try:
            from auto_summary.change_watcher import watch
        except ImportError:
            raise ImportError('watchdog is not found')
        main(**args)  # initialize tables of content
        watch(**args, join=True)
    else:
        main(**args)


if __name__ == "__main__":
    run_parser()

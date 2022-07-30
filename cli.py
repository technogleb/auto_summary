import argparse
from pathlib import Path

from generate_summary import main


def run_parser():
    parser = argparse.ArgumentParser('Provides CLI interface for generate_summary script')

    parser.add_argument(
        '-r', '--root', type=str, required=True,
        help='Path to the root folder, where top level summary will be located'
    )
    parser.add_argument(
        '--wikilinks', action='store_true',
        help='Whether to use wikilinks format or not. Default False.'
    )

    args = vars(parser.parse_args())
    args['root'] = Path(args['root']).resolve()

    main(**args)


if __name__ == "__main__":
    run_parser()

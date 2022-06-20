from argparse import Namespace, ArgumentParser
import colorama as cma

from metaannote.utils import to_string


def main(arguments):
    pass


if __name__ == '__main__':
    options = [
        'health_care',
        'generate',
        'merge'
    ]

    all_formats = [
        'coco'
    ]
    parent_parser = ArgumentParser(add_help=False)
    parent_parser.add_argument(dest='options', choices=options)
    parent_parser.add_argument('--format', help=to_string(cma.Fore.RED, 'dataset format'), type=str,
                               choices=all_formats)

    # Health Care
    health_care_parser = ArgumentParser(parents=[parent_parser])

    # Generate
    generate_parser = ArgumentParser(parents=[parent_parser])

    # Merge
    merge_parser = ArgumentParser(parents=[parent_parser])

    args = parent_parser.parse_args()

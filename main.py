import argparse


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Extracts Kenshi game data and dump it in processable format."
    )
    parser.add_argument('input',
                        metavar='FILE',
                        type=str,
                        nargs='+',
                        help='list of files to be processed (order matters)'
                        )
    return parser.parse_args()


if __name__ == '__main__':
    args = get_arguments()

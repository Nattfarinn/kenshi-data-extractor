import argparse
import kenshi

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Merge Kenshi mods into one data file."
    )
    parser.add_argument('input',
                        metavar='FILE',
                        type=str,
                        nargs='+',
                        help='list of files to be merged (order matters)'
                        )
    parser.add_argument('--output',
                        type=str,
                        help='output file name (default:'
                             + ' output.mod)',
                        default='output.mod'
                        )
    parser.add_argument('--version',
                        type=int,
                        help='output mod version (default: 1)',
                        default=1
                        )
    parser.add_argument('--author',
                        type=str,
                        help='output mod author (default: "Merged")',
                        default="Merged"
                        )
    args = parser.parse_args()

    records = {}
    descriptions = []

    for path in args.input:
        mod_file = kenshi.ModFileReader(path)
        descriptions.append(mod_file.description)
        kenshi.merge_records(mod_file, records)

    output = kenshi.ModFileWriter(args.output, args.version, args.author,
                                  "\r\r".join(descriptions), "", "")
    output.records(records)

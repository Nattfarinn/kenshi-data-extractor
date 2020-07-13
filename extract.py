import argparse
import json
import kenshi

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Extracts Kenshi game data and dump"
                    + " it in processable format."
    )
    parser.add_argument('input',
                        metavar='FILE',
                        type=str,
                        nargs='+',
                        help='list of files to be processed'
                             + ' and merged (order matters)'
                        )
    parser.add_argument('--output',
                        type=str,
                        help='output file name (default:'
                             + ' output.json)',
                        default='output.json'
                        )
    parser.add_argument('--pretty',
                        action="store_true",
                        help='prettify JSON output',
                        default=False
                        )
    args = parser.parse_args()

    records = {}
    for path in args.input:
        kenshi.merge_records(kenshi.ModFileReader(path), records)

    with open(args.output, "w") as output:
        indent = 2 if args.pretty else None
        json_output = json.dumps(records, indent=indent)
        output.write(json_output)

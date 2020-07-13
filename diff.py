import argparse
import kenshi

ITEM_MISSING = '--'
ITEM_ADDED = '++'
ITEM_CHANGED = '<>'


def recursive_diff(dict_a, dict_b, path=None):
    for key_a in dict_a:
        value_a = dict_a[key_a]
        value_path = "[%s (%s)]" % (value_a["name"], value_a["type"]) if \
            not path else path + "->%s" % key_a
        if key_a not in dict_b and not path:
            print("(%s) B does not contain %s" % (ITEM_MISSING,
                                                  value_path))
        elif key_a not in dict_b:
            print("(%s) Value %s missing in B" % (
                ITEM_MISSING, value_path
            ))
        else:
            value_b = dict_b[key_a]
            if isinstance(value_a, dict) and isinstance(value_b, dict):
                recursive_diff(value_a, value_b, value_path)
            else:
                if value_a != value_b:
                    print("(%s) Value %s: %s => %s" % (
                        ITEM_CHANGED, value_path, value_a, value_b
                    ))
    for key_b in dict_b:
        value_b = dict_b[key_b]
        value_path = "[%s (%s)]" % (value_b["name"], value_b["type"]) if \
            not path else path + "->%s" % key_b
        if key_b not in dict_a and not path:
            print("(%s) Mod A does not contain %s" % (ITEM_ADDED,
                                                      value_path))
        elif key_b not in dict_a:
            print("(%s) Value %s added in B" % (
                ITEM_ADDED, value_path
            ))
    """
    err = ''
    key_err = ''
    value_err = ''
    old_path = path
    for k in dict_1.keys():
        path = old_path + "[%s]" % k
        if not dict_2.has_key(k):
            key_err += "Key %s%s not in %s\n" % (
            dict_2_name, path, dict_2_name)
        else:
            if isinstance(dict_1[k], dict) and isinstance(dict_2[k],
                                                          dict):
                err += compare_dictionaries(dict_1[k], dict_2[k], 'd1',
                                            'd2', path)
            else:
                if dict_1[k] != dict_2[k]:
                    value_err += "Value of %s%s (%s) not same as %s%s (%s)\n" \
                                 % (dict_1_name, path, dict_1[k],
                                    dict_2_name, path, dict_2[k])

    for k in dict_2.keys():
        path = old_path + "[%s]" % k
        if not dict_1.has_key(k):
            key_err += "Key %s%s not in %s\n" % (
            dict_2_name, path, dict_1_name)

    return key_err + value_err + err
    """


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Display difference between two mods or mod versions."
    )
    parser.add_argument('file_a',
                        metavar='FILE_A',
                        type=str,
                        help='First file path'
                        )
    parser.add_argument('file_b',
                        metavar='FILE_B',
                        type=str,
                        help='Second file path'
                        )
    args = parser.parse_args()

    first_file = kenshi.ModFileReader(args.file_a)
    second_file = kenshi.ModFileReader(args.file_b)

    print("Mod A: %s" % first_file.file_path)
    print("Mod B: %s" % second_file.file_path)

    recursive_diff(first_file.records, second_file.records)

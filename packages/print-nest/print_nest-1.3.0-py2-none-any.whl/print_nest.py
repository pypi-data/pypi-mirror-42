"""this is a little tool for printing all items of a nested(or not)list."""
import sys


def print_nest(a_list, indent=False, level=0, fh=sys.stdout):
    """by default, there is no indent added to items according to the nested situation.
    You can add \'Ture\' to turn indent mode on, and a int to modify how much indents you want to add.

    """

    for item in a_list:
        if isinstance(item, list):
            print_nest(item, indent, level + 1, fh)
        else:
            if indent:
                for item_indent in range(level):
                    print('\t', end='', file=fh)
            print(item, file=fh)



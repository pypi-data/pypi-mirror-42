
"""This is Print_Nested_List.py module, will help you printing nested list recursively.
Remember the limit of recursion in 1000."""

def print_nested_list(a_list, indent=False, tabs=0, file=None):
    """This is a method that will help to recursively go down the nested lists
    and then print each element of the list"""
    for x in a_list:
        if isinstance(x, list):
            tabs += 1
            print_nested_list(x, indent=indent, tabs=tabs, file=file)
        else:
            if indent:
                print("\t" * tabs, end='', file=file)
            print(x, file=file)


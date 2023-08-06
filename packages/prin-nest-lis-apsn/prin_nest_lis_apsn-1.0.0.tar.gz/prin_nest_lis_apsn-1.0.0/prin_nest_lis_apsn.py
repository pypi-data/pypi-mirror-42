
"""This is Print_Nested_List.py module, will help you printing nested list recursively.
Remember the limit of recursion in 1000."""


def print_nested_list(a_list):
    """This is a method that will help to recursively go down the nested lists
    and then print each element of the list"""
    for x in a_list:
        if isinstance(x, list):
            print_nested_list(x)
        else:
            print(x)

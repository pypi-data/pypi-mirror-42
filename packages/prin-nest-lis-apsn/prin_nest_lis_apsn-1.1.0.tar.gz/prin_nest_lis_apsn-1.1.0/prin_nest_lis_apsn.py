
"""This is Print_Nested_List.py module, will help you printing nested list recursively.
Remember the limit of recursion in 1000."""


def print_nested_list(a_list, tabs=0):
    """This is a method that will help to recursively go down the nested lists
    and then print each element of the list"""
    for x in a_list:
        if isinstance(x, list):
            tabs += 1
            print_nested_list(x, tabs)
        else:
            print("\t"*tabs+"{}".format(x))


if __name__ == '__main__':
        a_nested_list = [1, 2, 3, 4, 5, [6, 7, 8, 9, 10, [11, 12, 13, 14, 15, [16, 17, 18, 19, [20, 21, 22, 23], 24], 25], 26], 28]
        print_nested_list(a_nested_list)

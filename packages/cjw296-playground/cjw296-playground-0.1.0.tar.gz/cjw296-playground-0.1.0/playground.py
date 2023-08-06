"""
This is  module.
"""
from sys import version_info


def version_happiness():
    """
    This is version happiness...
    """
    if version_info.major == 2:
        return ':-('
    # elif version_info.major == 7:
    #     raise Exception('wut?')
    else:
        return ':-)'

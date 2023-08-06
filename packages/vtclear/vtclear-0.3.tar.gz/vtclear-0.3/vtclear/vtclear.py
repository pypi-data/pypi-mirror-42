#!/usr/bin/env python3


def clear_screen():
    """
    VT100 ASCII clear implemented in Python3.
    http://www.termsys.demon.co.uk/vtansi.htm#erase
    """
    print(f"{chr(27)}[2J{chr(27)}[H", end="")

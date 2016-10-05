import os
import sys
import time
import datetime


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
        print("\033c", end="")
    else:
        os.system("clear")
        print("\033c", end="")




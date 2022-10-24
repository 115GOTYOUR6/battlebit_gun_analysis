import sys
import os
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import utility


@utility.timer
def count_to(number):
    i = 0
    while i != number:
        i += 1


count_to(10**3)
count_to(10**6)
count_to(10**8)

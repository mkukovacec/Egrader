__words__ = {}

import os

for line in open("features/resources/common-english-words.txt"):
    __words__[line.rstrip()] = True

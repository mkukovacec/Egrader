__words__ = {}
import os
for line in open("./rulers/grammar/resources/english_stop_words.txt"):
    __words__[line.rstrip()] = True

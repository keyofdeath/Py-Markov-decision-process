#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Case(object):

    # constante pour définir le type de case que sa va être
    START = 0
    FIN = 1
    DANGER = 2
    VIDE = 3
    OBSTACLE = 4

    def __init__(self, type, recompense=None):

        self.type = type
        self.recompense = recompense
        self.shape = None
        self.text_shape = None


if __name__ == "__main__":
    pass
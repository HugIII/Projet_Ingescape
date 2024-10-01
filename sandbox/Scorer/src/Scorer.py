#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Scorer.py
#  Scorer version 1.0
#  Created by Ingenuity i/o on 2024/10/01
#
# "no description"
#
import ingescape as igs


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Scorer(metaclass=Singleton):
    def __init__(self):
        # inputs

        # outputs
        self._outO = None

    # outputs
    @property
    def outO(self):
        return self._outO

    @outO.setter
    def outO(self, value):
        self._outO = value
        if self._outO is not None:
            igs.output_set_string("out", self._outO)



#!/usr/bin/pyton
# -*- encoding: utf-8 -*-
__all__ = ["dbclasses"]

class WrongVersion(Exception):
    pass

from sys import version_info
if version_info.version_info < (3,6):
    raise WrongVersion("Minimal version of python is 3.6") 

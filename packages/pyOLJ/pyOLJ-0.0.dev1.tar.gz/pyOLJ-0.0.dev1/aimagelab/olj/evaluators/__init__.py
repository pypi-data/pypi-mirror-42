from .lab00 import *


def get_evaluator(fn):
    if fn.__name__ == 'dot':
        return DotEvaluator


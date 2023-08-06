from .lab00 import *


def get_evaluator(fn):
    if fn.__name__ == 'dot':
        return DotEvaluator
    elif fn.__name__ == 'linear_stretch':
        return LinearStretchEvaluator
    elif fn.__name__ == 'histogram':
        return HistogramEvaluator
    elif fn.__name__ == 'threshold':
        return ThresholdEvaluator


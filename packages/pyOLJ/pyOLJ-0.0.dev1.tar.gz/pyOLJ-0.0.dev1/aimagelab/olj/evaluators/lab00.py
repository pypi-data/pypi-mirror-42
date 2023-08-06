import numpy as np
import random
from .base import BaseEvaluator


class DotEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.Fn = np.dot
        self.tests = [self.numerical_correctness, self.numerical_correctness]
        super(DotEvaluator, self).__init__()

    def numerical_correctness(self):
        sha, shb, shc = random.randint(1, 4),  random.randint(1, 4), random.randint(1, 4)
        a = np.random.random((sha, shb))
        b = np.random.random((shb, shc))
        return self.assertAllClose(a, b)


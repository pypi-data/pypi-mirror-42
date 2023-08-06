import numpy as np
import random
import cv2
from .base import BaseEvaluator


class DotEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.Fn = np.dot
        self.tests = [self.assertAllClose, self.assertAllClose]
        super(DotEvaluator, self).__init__()

    def inputs(self):
        sha, shb, shc = random.randint(1, 4),  random.randint(1, 4), random.randint(1, 4)
        a = np.random.random((sha, shb))
        b = np.random.random((shb, shc))
        return a, b


class LinearStretchEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.tests = [self.assertType, self.assertAttribute('dtype'), self.assertAttribute('shape'), ]
        self.tests += [self.assertAllClose, ] * 100
        super(LinearStretchEvaluator, self).__init__()

    def Fn(self, im, alpha, beta):
        return np.rint(np.clip(alpha * im + beta, 0, 255)).astype(np.uint8)

    def inputs(self):
        sh = (random.choice([1,3]), random.randint(1, 10), random.randint(1, 10))
        if sh[0] == 0:
            sh = sh[1:]
        im = np.random.randint(0, 256, sh).astype(np.uint8)
        if random.randint(0, 1) == 0:
            alpha, beta = random.randint(0, 256),  random.randint(0, 256)
        else:
            alpha, beta = random.random()*256, random.random()*256
        return im, alpha, beta


class HistogramEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.tests = [self.assertType, self.assertAttribute('shape'), self.assertAllClose, self.assertAllClose]
        super(HistogramEvaluator, self).__init__()

    def Fn(self, im, n_bins):
        hists = []
        for c in range(3):
            hists.append(cv2.calcHist([im[c]], [0], None, [n_bins], [0, 256]).T[0])
        return np.concatenate(hists) / im.size

    def inputs(self):
        im = np.random.randint(0, 256, ((3, 256, 256))).astype(np.uint8)
        n_bins = np.random.randint(0, 256)
        return im, n_bins


class ThresholdEvaluator(BaseEvaluator):
    def __init__(self, fn):
        self.fn = fn
        self.tests = [self.assertType, self.assertAttribute('shape'), self.assertAllClose, self.assertAllClose]
        super(ThresholdEvaluator, self).__init__()

    def Fn(self, im, value):
        return cv2.threshold(im, value, 255, cv2.THRESH_BINARY)[1]

    def inputs(self):
        im = np.random.randint(0, 256, ((256, 256))).astype(np.uint8)
        value = np.random.randint(0, 256)
        return im, value

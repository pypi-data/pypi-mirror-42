import numpy as np


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class BaseEvaluator(object):
    def __init__(self):
        print('======================================================')
        print('AImageLab OLJ')
        print('======================================================')
        self.counter = 0
        self.run_tests()

    def run_tests(self):
        self.counter = 0
        counter_passed = 0
        for i, t in enumerate(self.tests):
            print('Test %i/%i (%s)...' % (i+1, len(self.tests), t.__name__), end='')
            try:
                passed, message = t()
            except:
                passed = False
                message = 'Exception thrown.'
            if passed:
                print(bcolors.OKGREEN, 'PASSED', bcolors.ENDC)
            else:
                print(bcolors.FAIL, 'NOT PASSED', bcolors.ENDC)
            if t.__doc__:
                print("Descrizione:", t.__doc__)
            if message:
                print(message)
            counter_passed += passed
            self.counter += 1
        print('======================================================')
        print('%i out of %i test passed.' % (counter_passed, len(self.tests)))
        print('======================================================')

    def assertAllClose(self, *inputs):
        expected = self.Fn(*inputs)
        actual = self.fn(*inputs)
        if not np.allclose(expected, actual):
            msg = "Using the following inputs:\n"
            #msg += str(*inputs) + "\n"
            msg += "function '%s' returned a wrong output\n" % self.fn.__name__
            msg += "Expected output:\n" + str(expected) + "\n"
            msg += "Returned output:\n" + str(actual) + "\n"
            return False, msg
        return True, None

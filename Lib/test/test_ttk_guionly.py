import os
import unittest
from test import support

# Skip this test if _tkinter wasn't built.
support.import_module('_tkinter')

from _tkinter import TclError
from tkinter import ttk
from tkinter.test import runtktests

try:
    ttk.Button()
except TclError as msg:
    # assuming ttk is not available
    raise unittest.SkipTest("ttk not available: %s" % msg)

def test_main(enable_gui=False):
    if enable_gui:
        if support.use_resources is None:
            support.use_resources = ['gui']
        elif 'gui' not in support.use_resources:
            support.use_resources.append('gui')

    support.run_unittest(
            *runtktests.get_tests(text=False, packages=['test_ttk']))

if __name__ == '__main__':
    test_main(enable_gui=True)

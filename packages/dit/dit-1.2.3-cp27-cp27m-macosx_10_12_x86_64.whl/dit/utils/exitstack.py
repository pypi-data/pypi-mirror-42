"""
Uniform access for ExitStack context manager.

"""
import sys

if sys.version_info[:2] >= (3,3):
    from contextlib import ExitStack
else:
    from contextlib2 import ExitStack

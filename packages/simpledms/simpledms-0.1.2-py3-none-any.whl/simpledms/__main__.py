import os
import sys


ROOT = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)

from main import start_gui  # NOQA


if __name__ == "__main__":
    start_gui()

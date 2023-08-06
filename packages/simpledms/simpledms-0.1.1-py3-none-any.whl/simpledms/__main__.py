import os
import sys

from main import start_gui

ROOT = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, ROOT)


if __name__ == "__main__":
    start_gui()

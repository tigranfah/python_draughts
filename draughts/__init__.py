import sys
import os

core_path = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, core_path)

from board import *
import engine
import preprocessing
import exceptions

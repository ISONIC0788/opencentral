from logmachine import LogMachine
from os import getenv
import sys

logger = LogMachine(debug_level=getenv('DEBUG_LEVEL', 0), verbose="--verbose" in sys.argv)

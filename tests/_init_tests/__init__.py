import os
import sys

# Add src to the current working directory so that
# the classes in there can be imported correctly.
cwd = os.getcwd()
sys.path.insert(0, os.path.join(cwd, 'src'))

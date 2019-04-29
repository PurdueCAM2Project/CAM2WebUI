import os
import sys
from pkg_resources import load_entry_point

# Insert code here to preprocess the data from anywhere else

# Generate hyde layouts
sys.argv = [sys.argv[0], 'gen']
load_entry_point('hyde', 'console_scripts', 'hyde')()

# Serve hyde site
sys.argv = [sys.argv[0], 'serve']
load_entry_point('hyde', 'console_scripts', 'hyde')()


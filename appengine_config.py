# appengine_config.py
import os
from google.appengine.ext import vendor

# Add any libraries install in this folder.
vendor.add(os.path.dirname(os.path.realpath(__file__)))
# Any changes to the distributions library should be reinstalled with
#  pip install --upgrade .

# For running unit tests, use
# /usr/bin/python -m unittest test

import unittest

from delimag import Delimag


# Create data for testing


class TestDelimagClass(unittest.TestCase):
    def
#!/usr/bin/env python
import os
import unittest


class Tests(unittest.TestCase):

    def test_chimit(self):
        os.system('chimit echo "hello there"')


if __name__ == '__main__':
    unittest.main()

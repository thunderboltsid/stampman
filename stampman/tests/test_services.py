import unittest

from stampman.services import pool


class PoolServiceTest(unittest.TestCase):
    def test_creation(self):
        pool.PooledService()

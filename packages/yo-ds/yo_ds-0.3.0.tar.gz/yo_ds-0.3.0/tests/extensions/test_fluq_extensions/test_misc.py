import unittest
from tests.extensions.common import *

class MiscMethodsTests(unittest.TestCase):
    def test_pairwise(self):
        result = Query.args(1,2,3).feed(fluq.pairwise()).to_list()
        self.assertListEqual([(1,2),(2,3)],result)

    def test_strjoin(self):
        result = Query.args(1,2,3).feed(fluq.strjoin(','))
        self.assertEqual("1,2,3",result)

    def test_countby(self):
        result = Query.args(1,1,1,2,2,3).feed(fluq.count_by(lambda z: z)).to_series()
        self.assertListEqual([1,2,3],list(result.index))
        self.assertListEqual([3,2,1],list(result))


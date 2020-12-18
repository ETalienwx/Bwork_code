import unittest
from My_Dict import Dict


class TestDict(unittest.TestCase):  # 编写一个测试类，从unittest.Testcase继承

    def test_init(self):
        d = Dict(a=1, b=2, c=3, d='test')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 2)
        self.assertEqual(d.c, 3)
        self.assertEqual(d.d, 'test')
        self.assertTrue(isinstance(d, dict))

    def test_keys(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertEqual(d.key, 'value')
        self.assertTrue('key' in d)

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')


if __name__ == '__main__':
    unittest.main()

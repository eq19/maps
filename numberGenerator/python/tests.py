from utilities import *
from decimal import *
import unittest


class testHexFunctions(unittest.TestCase):

    def setUp(self):
        #hnum of value 5, 2 powers, and precision 20
        self.prec = 15
        self.hnum = Hexnum(5, 2, self.prec)
        self.plist = open('prime_lists/5.txt')

    def test_power_list(self):
        self.assertEqual(power_list(2,1, self.prec), [2.00000])
        self.assertEqual(power_list(2.5,2, self.prec), [Decimal('2.5'), Decimal('6.25')])
        self.assertEqual(power_list(3.14159265358979, 2, self.prec),
                         [Decimal('3.14159265358979'),
                          Decimal('9.86960440108934')])

    def test_add_color(self):
        self.hnum.add_color("blue")
        self.assertEqual(self.hnum.colors, ["blue"])

    def test_did_roll_double(self):
        self.hnum.add_color("blue")
        self.hnum.add_color("blue")
        self.assertTrue(self.hnum.did_roll_double())

    def test_find_plist(self):
        self.assertEqual(find_plist(10), 4)
        self.assertEqual(find_plist(10000000), 4)
        self.assertEqual(find_plist(20000000), 0)
        self.assertEqual(find_plist(60000000), None)

    def test_get_spin_nums(self):
        self.assertEqual(get_spin_nums(1,     self.plist), (1, 1))
        self.plist.seek(0)
        self.assertEqual(get_spin_nums(9,     self.plist), (3, 1))
        self.plist.seek(0)
        self.assertEqual(get_spin_nums(10000, self.plist), (5,-1))

if __name__ == '__main__':
    unittest.main(exit=False)

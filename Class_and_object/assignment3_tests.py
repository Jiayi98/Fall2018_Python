# -*- coding: utf-8 -*-
"""A few basic tests for CS109 Python Assignment 3.

This does not test for all the requirements of the assignment! So make
sure you test it yourself.

Run this script using:
  python3.5 assignment3_tests.py
It should work if you are in the same directory as your assignment3.py
file. If this does not work you may want to try:
  PYTHONPATH=[directory containing assignment3.py] python3.5 assignment3_tests.py

"""

# DO NOT CHANGE THIS FILE. Grading will be done with an official
# version, so make sure your code works with this exact version.

import unittest
import sys

import assignment3

class Assignment3Tests(unittest.TestCase):

    def check_constructor(self, cls, *args, **kws):
        self.assertIsInstance(cls, type)
        self.assertIsInstance(cls(*args, **kws), cls)

    def test_menu_init(self):
        self.check_constructor(assignment3.Menu)

    def test_order_init(self):
        self.check_constructor(assignment3.Order)

    def test_grouporder_init(self):
        self.check_constructor(assignment3.GroupOrder)

    def test_food_init(self):
        self.check_constructor(assignment3.Food, "Lasagna", 9.50)

    def test_drink_init(self):
        self.check_constructor(assignment3.Drink, "Lemonade", 1.50)

    def test_drink_attr(self):
        d = assignment3.Drink("Lemonade", 1.50)
        self.assertAlmostEqual(d.price, 1.50)

    def test_drink_prop(self):
        m = assignment3.Menu()
        d = assignment3.Drink("Lemonade", 1.50)
        m.add_item(d)
        self.assertAlmostEqual(d.price_plus_tax(), 1.50 * 1.18)
        self.assertEqual(d.menu, m)
        
    def test_menu_items(self):
        m = assignment3.Menu()
        d = assignment3.Drink("Lemonade", 1.50)
        m.add_item(d)
        self.assertIs(d.menu, m)
        self.assertEqual(list(m.items), [d])
        with self.assertRaises(AttributeError):
            m.items = [None]
        self.assertEqual(list(m.items), [d])
        
    def test_menu_items_copy(self):
        m = assignment3.Menu()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m.add_item(d)
        self.assertIsNot(m.items, m.items)
        it = m.items
        if hasattr(it, "add"):
            it.add(f)
        if hasattr(it, "append"):
            it.append(f)
        self.assertEqual(list(m.items), [d])
        
    def test_menu_add_items(self):
        m1 = assignment3.Menu()
        m2 = assignment3.Menu()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        self.assertTrue(m1.add_item(d))
        self.assertTrue(m2.add_item(f))
        self.assertFalse(m2.add_item(d))
        self.assertFalse(m1.add_item(f))

    def test_menu_add_items2(self):
        m1 = assignment3.Menu()
        m2 = assignment3.Menu()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m1.add_item(d)
        m2.add_item(f)
        m2.add_item(d)
        m1.add_item(f)
        self.assertNotIn(d, m2.items)
        self.assertNotIn(f, m1.items)

    def test_item_menu(self):
        m = assignment3.Menu()
        d = assignment3.Drink("Lemonade", 1.50)
        d.menu = m
        try:
            d.menu = assignment3.Menu()
        except:
            pass
        self.assertIs(d.menu, m)

    def test_order_items(self):
        m1 = assignment3.Menu()
        m2 = assignment3.Menu()
        o = assignment3.Order()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m1.add_item(d)
        m2.add_item(f)
        self.assertTrue(o.add_item(d))
        self.assertFalse(o.add_item(f))

    def test_order_price(self):
        m = assignment3.Menu()
        o = assignment3.Order()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m.add_item(d)
        m.add_item(f)
        o.add_item(d)
        o.add_item(f)
        self.assertAlmostEqual(o.price_plus_tax(), 1.50 * 1.18 + 0.75 * 1.10)
        self.assertAlmostEqual(o.price_plus_tax_and_tip(0.18), (1.50 * 1.18 + 0.75 * 1.10) * 1.18)

    def test_order_small(self):
        m = assignment3.Menu()
        o = assignment3.Order() 
        f = assignment3.Food("Toast", 0.75)
        m.add_item(f)
        self.assertAlmostEqual(o.price_plus_tax(), 0)
        o.add_item(f)
        self.assertAlmostEqual(o.price_plus_tax(), 0.75 * 1.10)

    def test_order_large(self):
        m = assignment3.Menu()
        o = assignment3.Order()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        a = assignment3.Food("A", 10.00)
        b = assignment3.Food("B", 9.50)
        m.add_item(d)
        m.add_item(f)
        m.add_item(a)
        m.add_item(b)
        o.add_item(d)
        o.add_item(f) 
        o.add_item(a)
        o.add_item(b)
        self.assertAlmostEqual(o.price_plus_tax(), 1.50 * 1.18 + (0.75 + 10 + 9.5) * 1.10)

    def test_tax_attributes_class(self):
        self.assertAlmostEqual(assignment3.Menu.food_tax, 0.1)
        self.assertAlmostEqual(assignment3.Menu.drink_tax, 0.18)

    def test_tax_attributes(self):
        m = assignment3.Menu()
        self.assertAlmostEqual(m.food_tax, 0.1)
        self.assertAlmostEqual(m.drink_tax, 0.18)

    def test_food_attr(self):
        d = assignment3.Food("Lemonade", 1.50)
        self.assertAlmostEqual(d.price, 1.50)

    def test_food_prop(self):
        m = assignment3.Menu()
        d = assignment3.Food("Lemonade", 1.50)
        m.add_item(d)
        self.assertAlmostEqual(d.price_plus_tax(), 1.50 * 1.10)
        self.assertEqual(d.menu, m)

    def test_grouporder_items(self):
        m1 = assignment3.Menu()
        m2 = assignment3.Menu()
        o = assignment3.GroupOrder()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m1.add_item(d)
        m2.add_item(f)
        self.assertTrue(o.add_item(d))
        self.assertFalse(o.add_item(f))

    def test_grouporder_price_under(self):
        m = assignment3.Menu()
        o = assignment3.GroupOrder()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m.add_item(d)
        m.add_item(f)
        o.add_item(d)
        o.add_item(f)
        self.assertAlmostEqual(o.price_plus_tax(), 1.50 * 1.18 + 0.75 * 1.10)
        self.assertAlmostEqual(o.price_plus_tax_and_tip(0.18), (1.50 * 1.18 + 0.75 * 1.10) * 1.20)

    def test_grouporder_super_use(self):
        class DeliveredOrder(assignment3.Order):
            def price_plus_tax_and_tip(self, amount):
                return super().price_plus_tax_and_tip(amount) + 1.0

        class GroupDeliveredOrder(assignment3.GroupOrder, DeliveredOrder):
            pass

        m = assignment3.Menu()
        o = GroupDeliveredOrder()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m.add_item(d)
        m.add_item(f)
        o.add_item(d)
        o.add_item(f)
        self.assertAlmostEqual(o.price_plus_tax_and_tip(0.20), (1.50 * 1.18 + 0.75 * 1.10) * 1.20 + 1.0)

    def test_grouporder_price_over(self):
        m = assignment3.Menu()
        o = assignment3.GroupOrder()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m.add_item(d)
        m.add_item(f)
        o.add_item(d)
        o.add_item(f)
        self.assertAlmostEqual(o.price_plus_tax(), 1.50 * 1.18 + 0.75 * 1.10)
        self.assertAlmostEqual(o.price_plus_tax_and_tip(0.32), (1.50 * 1.18 + 0.75 * 1.10) * 1.32)

    def test_applicable_tax(self):
        m = assignment3.Menu()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m.add_item(d)
        m.add_item(f)
        self.assertAlmostEqual(f._applicable_tax(), 0.10)
        self.assertAlmostEqual(d._applicable_tax(), 0.18)

    def test_alternate_tax(self):
        class MyMenu(assignment3.Menu):
            food_tax = 0.12
            drink_tax = 0.16
        
        m = MyMenu()
        d = assignment3.Drink("Lemonade", 1.50)
        f = assignment3.Food("Toast", 0.75)
        m.add_item(d)
        m.add_item(f)
        self.assertAlmostEqual(f.price_plus_tax(), 0.75 * 1.12)
        self.assertAlmostEqual(d.price_plus_tax(), 1.50 * 1.16)
        self.assertAlmostEqual(f._applicable_tax(), 0.12)
        self.assertAlmostEqual(d._applicable_tax(), 0.16)


    def test_additional_item_type(self):
        class MyMenu(assignment3.Menu):
            dessert_tax = 0.05
        
        m = MyMenu()
        f = assignment3.Food("Toast", 0.75)
        m.add_item(f)
        
        class Dessert(assignment3.Item):
            def _applicable_tax(self):
                return self.menu.dessert_tax

        d = Dessert("PI", 1.50)
        m.add_item(d)
            
        self.assertAlmostEqual(f.price_plus_tax(), 0.75 * 1.10)
        self.assertAlmostEqual(d.price_plus_tax(), 1.50 * 1.05)
        self.assertAlmostEqual(f._applicable_tax(), 0.10)
        self.assertAlmostEqual(d._applicable_tax(), 0.05)

if __name__ == "__main__":
    unittest.main()

from unittest import TestCase

from src.deal import AccessoryDeal, BundleDeal, DiscountDeal
from src.item import Item

class TestDiscountDeal(TestCase):
    # the brand new Super iPad will have a bulk discounted applied, 
    # where the price will drop to $499.99 each, if someone buys more than 4
    def setUp(self) -> None:
        self.item = Item('ipd', 'Super Ipad', 549.99)
        self.deal = DiscountDeal(
            associated_item=self.item, 
            discount_quantity=5, 
            discount_price=499.99
        )

    def test_less_than_discount_quantity(self):
        # Supply a cart with 4 ipads.
        # Price should remain untouched.
        cart = [self.item] * 4
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])
        
        self.assertEqual(len(discounts), 0)
        self.assertAlmostEqual(total, self.item.price * 4)

    def test_exact_discount_quantity(self):
        # Supply a cart with 5 ipads.
        # Price should drop to 499.99 per unit.
        cart = [self.item] * 5
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])
        
        self.assertEqual(len(discounts), 5)
        self.assertAlmostEqual(total, self.deal.discount_price * 5)

    def test_more_than_discount_quantity(self):
        # Supply a cart with 6 ipads.
        # Price should drop to 499.99 per unit.
        cart = [self.item] * 6
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])

        self.assertEqual(len(discounts), 6)
        self.assertAlmostEqual(total, self.deal.discount_price * 6)

class TestBundleDeal(TestCase):
    # we're going to have a 3 for 2 deal on Apple TVs. 
    # For example, if you buy 3 Apple TVs, you will pay the price of 2 only
    def setUp(self) -> None:
        self.item = Item('atv', 'Apple TV', 109.50)
        self.deal = BundleDeal(
            associated_item=self.item,
            bundle_quantity=3,
            discount_quantity=2
        )

    def test_less_than_bundle_quantity(self):
        # Supply cart with 2 apple tvs.
        # No discount should be included.
        cart = [self.item] * 2
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])

        self.assertEqual(len(discounts), 0)
        self.assertAlmostEqual(total, self.item.price * 2, 2)

    def test_exact_bundle_quantity(self):
        # Supply cart with 3 apple tvs.
        # Discount should be applied once.
        cart = [self.item] * 3
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])

        self.assertEqual(len(discounts), 1)
        self.assertAlmostEqual(total, self.item.price * 2, 2)

    def test_more_than_but_not_double_bundle_quantity(self):
        # Supply cart with 5 apple tvs.
        # Discount should be applied only once.
        cart = [self.item] * 5
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])

        self.assertEqual(len(discounts), 1)
        self.assertAlmostEqual(total, self.item.price * 4, 2)

    def test_double_bundle_quantity(self):
        # Supply cart with 6 apple tvs.
        # Discount should be applied twice.
        cart = [self.item] * 6
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])

        self.assertEqual(len(discounts), 2)
        self.assertAlmostEqual(total, self.item.price * 4, 2)

class TestAccessoryDeal(TestCase):
    # we will bundle in a free VGA adapter free of charge with every MacBook Pro sold
    def setUp(self) -> None:
        self.item = Item('mbp', 'MacBook Pro', 1399.99)
        self.bonus = Item('vga', 'VGA adapter', 30.00)
        self.deal = AccessoryDeal(
            associated_item=self.item,
            bonus_item=self.bonus
        )

    def test_bonus_item_not_applied(self):
        # Supply a cart with no macbooks.
        # Bonus item should not be added.
        cart = [self.bonus] * 2
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])
        
        self.assertEqual(len(discounts), 0)
        self.assertAlmostEqual(total, self.bonus.price * 2, 2)

    def test_bonus_item_applied(self):
        # Supply a cart with 3 macbooks.
        # Bonus item should be added 3 times.
        cart = [self.item, self.bonus] * 3
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])
        
        self.assertEqual(len(discounts), 3)
        self.assertAlmostEqual(total, self.item.price * 3, 2)

    def test_bonus_item_applied_with_more_bonus_items_than_deal_items(self):
        cart = [self.bonus] * 4 + [self.item] * 2
        discounts = self.deal.apply(cart)
        total = sum([item.price for item in [*cart, *discounts]])
        
        self.assertEqual(len(discounts), 2)
        self.assertAlmostEqual(total, self.bonus.price * 2 + self.item.price * 2, 2)
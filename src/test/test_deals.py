from unittest import TestCase

from src.deal import AccessoryDeal, BundleDeal, DiscountDeal
from src.item import Item

class TestDiscountDeal(TestCase):
    # the brand new Super iPad will have a bulk discounted applied, 
    # where the price will drop to $499.99 each, if someone buys more than 4
    def setUp(self) -> None:
        item = Item('ipd', 'Super Ipad', 549.99)
        self.deal = DiscountDeal(
            associated_item=item, 
            discount_quantity=5, 
            discount_price=499.99
        )


class TestBundleDeal(TestCase):
    # we're going to have a 3 for 2 deal on Apple TVs. 
    # For example, if you buy 3 Apple TVs, you will pay the price of 2 only
    def setUp(self) -> None:
        item = Item('atv', 'Apple TV', 109.50)
        self.deal = BundleDeal(
            associated_item=item,
            bundle_quantity=3,
            discount_quantity=2
        )

class TestAccessoryDeal(TestCase):
    # we will bundle in a free VGA adapter free of charge with every MacBook Pro sold
    def setUp(self) -> None:
        item = Item('mbp', 'MacBook Pro', 1399.99)
        bonus = Item('vga', 'VGA adapter', 30.00)
        self.deal = AccessoryDeal(
            associated_item=item,
            bonus_item=bonus
        )
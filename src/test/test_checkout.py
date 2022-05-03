from unittest import TestCase
from src.checkout import Checkout

from src.utils import load_deals, load_items

class TestExpectedOutput(TestCase):
    items = load_items('items.yaml')
    deals = load_deals('deals.yaml', items)

    def setUp(self) -> None:
        self.checkout = Checkout(self.deals)

    # SKUs Scanned: atv, atv, atv, vga Total expected: $249.00
    def test_case_one(self):
        self.checkout.scan(self.items['atv'])
        self.checkout.scan(self.items['atv'])
        self.checkout.scan(self.items['atv'])
        self.checkout.scan(self.items['vga'])
        self.checkout.display_cart

        self.assertEqual(self.checkout.total, 249.00)

    # SKUs Scanned: atv, ipd, ipd, atv, ipd, ipd, ipd Total expected: $2718.95
    def test_case_two(self):
        self.checkout.scan(self.items['atv'])
        self.checkout.scan(self.items['ipd'])
        self.checkout.scan(self.items['ipd'])
        self.checkout.scan(self.items['atv'])
        self.checkout.scan(self.items['ipd'])
        self.checkout.scan(self.items['ipd'])
        self.checkout.scan(self.items['ipd'])
        self.checkout.display_cart

        self.assertEqual(self.checkout.total, 2718.95)

    # SKUs Scanned: mbp, vga, ipd Total expected: $1949.98
    def test_case_three(self):
        self.checkout.scan(self.items['mbp'])
        self.checkout.scan(self.items['ipd'])
        self.checkout.scan(self.items['vga'])
        self.checkout.display_cart

        self.assertEqual(self.checkout.total, 1949.98)

from cmd import Cmd

from src.checkout import Checkout
from src.utils import load_deals, load_items


items = load_items('items.yaml')
deals = load_deals('deals.yaml', items)

checkout = Checkout(deals)

class ShoppingCLI(Cmd):
    checkout: Checkout

    def do_add(self, args):
        pass

    def do_total(self, args):
        pass

    def do_exit(self, args):
        pass


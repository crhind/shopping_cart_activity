from cmd import Cmd

from src.checkout import Checkout
from src.utils import load_deals, load_items


items = load_items('items.yaml')
deals = load_deals('deals.yaml', items)

checkout = Checkout(deals)

class ShoppingCLI(Cmd):

    def do_add(self, args):
        '''Adds an item to the checkou. Requires an item sku to be provided.'''
        if len(args) > 0:
            try:
                item = items[args]
                checkout.scan(item)
            except KeyError:
                print(f'Unknown item sku "{args}"')
        else:
            print("Missing item sku.")

    def do_list_items(self, args):
        '''Lists the available items.'''
        list_items()

    def do_display_cart(self, args):
        '''Displays the current items in the checkout cart.'''
        checkout.display_cart

    def do_total(self, args):
        '''Calculate and display the cart total. Includes any discounts.'''
        total = checkout.total
        print(f'Current total is {total}')

    def do_exit(self, args):
        '''Exits the command prompt.'''
        print('Exiting...')
        raise SystemExit

def list_items() -> None:
    print('Items:')
    for item_sku, item in items.items():
        print(f'  {item}')

if __name__ == '__main__':
    prompt = ShoppingCLI()
    prompt.prompt = '> '
    prompt.cmdloop(f'Starting shopping cart.')
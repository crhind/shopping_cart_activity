
from typing import List, Set

from src.deal import Deal
from src.item import Item


class Checkout:
    '''
    General checkout class.
    Maintains the current shopping cart and all current deals.
    '''
    def __init__(self, deals: Set[Deal]) -> None:
        self._cart = list()
        self.deals = deals

    @property
    def cart(self) -> List[Item]:
        '''Returns a readonly copy of the cart.'''
        return self._cart.copy()

    @property
    def display_cart(self) -> None:
        '''Displays all items currently in the cart.'''
        print("Cart: \n")
        for item in self._cart:
            print(f'  {item}')

    @property
    def total(self) -> None:
        '''Calculates and displays the total of the cart, including all applicable deals.'''
        cart_total = sum([item.price for item in self._cart])
        discount_total = sum([item.price for item in self._apply_deals()])
        
        print(f'Cart total: {cart_total}')
        print(f'Discount total: {discount_total}')
        
        return cart_total + discount_total

    def scan(self, line_item: Item) -> None:
        '''Adds an item to the cart.'''
        print(f'Adding item "{line_item.sku}"')
        self._cart.append(line_item) 
     
    def _apply_deals(self) -> List[Item]:
        '''
        Cycles through all avaiable deals to checkif the conditions have been met.
        Returns all associated deal items.
        '''
        applied_deals = list()
        for deal in self.deals:
            deals = deal.apply(self.cart)
            print(f'{type(deal).__name__} deals - {deals}')
            applied_deals.extend(deals)
        return applied_deals    


from typing import List, Set

from src.deal import Deal
from src.item import Item


class Checkout:
    def __init__(self, deals: Set[Deal]) -> None:
        self._cart = list()
        self.deals = deals

    @property
    def cart(self) -> List[Item]:
        return self._cart.copy()

    @property
    def display_cart(self) -> None:
        print("Cart: \n")
        for item in self._cart:
            print(f'  {item}')

    @property
    def total(self) -> None:
        cart_total = sum([item.price for item in self._cart])
        discount_total = sum([item.price for item in self._apply_deals()])
        
        print(f'Cart total: {cart_total}')
        print(f'Discount total: {discount_total}')
        
        return cart_total + discount_total

    def scan(self, line_item: Item) -> None:
        print(f'Adding item "{line_item.sku}"')
        self._cart.append(line_item) 
     
    def _apply_deals(self) -> List[Item]:
        applied_deals = list()
        for deal in self.deals:
            deals = deal.apply(self.cart)
            print(f'{type(deal).__name__} deals - {deals}')
            applied_deals.extend(deals)
        return applied_deals    

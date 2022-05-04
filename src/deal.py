
from logging import getLogger
from copy import deepcopy
from typing import List

from src.item import Item

logger = getLogger(__name__)


class Deal:
    '''
    Base class for deals. Could implement as abstract with ABC if needed.
    Every deal has an item that the deal is associated with.
    '''
    associated_item: Item

    def apply(self, cart: List[Item]) -> List[Item]:
        '''Applies the deal(s) if the deal condition is met.'''
        pass


class DiscountDeal(Deal):
    '''
    Discount type deal.
    Example: "the brand new Super iPad will have a bulk discounted applied, where the price will drop to $499.99 each, if someone buys more than 4"
    '''
    def __init__(self, associated_item: Item, discount_quantity: int, discount_price: float) -> None:
        self.associated_item = associated_item
        self.discount_quantity = discount_quantity
        self.discount_price = discount_price

    @property
    def description(self) -> str:
        return f'{self.discount_price} for {self.discount_quantity}+ {self.associated_item.name}.'
    
    @property
    def discount(self) -> float:
        return self.associated_item.price - self.discount_price

    def apply(self, cart: List[Item]) -> List[Item]:
        logger.info(f'Applying all discount deals.')
        # Find the quantity of associated items in the supplied cart.
        item_quantity = len(list(filter(lambda item, key=self.associated_item.sku: item.sku == key, cart)))
        # If the quantity condition is met apply the discount and return the deal items otherwise an empty list.
        if item_quantity >= self.discount_quantity:
            return [Item(sku='DSC', name=self.description, price=-self.discount)] * item_quantity
        return list()


class BundleDeal(Deal):
    '''
    Bundle type deal.
    Example: "we're going to have a 3 for 2 deal on Apple TVs. For example, if you buy 3 Apple TVs, you will pay the price of 2 only"
    '''
    def __init__(self, associated_item: Item, bundle_quantity: int, discount_quantity: int) -> None:
        self.associated_item = associated_item
        self.bundle_quantity = bundle_quantity
        self.discount_quantity = discount_quantity

    @property
    def description(self) -> str:
        return f'{self.bundle_quantity} for {self.discount_quantity} on {self.associated_item.name}.'
    
    @property
    def discount(self) -> float:
        return (self.bundle_quantity-self.discount_quantity) * self.associated_item.price

    def apply(self, cart: List[Item]) -> List[Item]:
        logger.info(f'Applying all bundle deals.')
        # Find all instances of the associated item in the supplied cart.
        matching_items = filter(lambda item, key=self.associated_item.sku: item.sku == key, cart)
        # Return a bundle deal discount item for every bundle_quanitity'th associated deal item. 
        return [Item(sku='DSC', name=self.description, price=-self.discount)] * (len(list(matching_items)) // self.bundle_quantity)


class AccessoryDeal(Deal):
    '''
    Accessory type deal.
    Example: "we will bundle in a free VGA adapter free of charge with every MacBook Pro sold"
    '''
    def __init__(self, associated_item: Item, bonus_item: Item) -> None:
        self.associated_item = associated_item
        self.bonus_item = deepcopy(bonus_item)
        self.bonus_item.price *= -1
    
    def apply(self, cart: List[Item]) -> List[Item]:
        logger.info(f'Applying all accessory deals.')

        # Do we need to check if the vga is in cart already to apply the discount? 
        # Find all instances of the associated item in the supplied cart.
        item_quantity = len(list(filter(lambda item, key=self.associated_item.sku: item.sku == key, cart)))
        # Find all instances of the bonus item in the supplied cart.
        bonus_item_quantity = len(list(filter(lambda item, key=self.bonus_item.sku: item.sku == key, cart)))
        
        # Should only discount the bonus item if it is present in the cart. i.e. has been scanned.
        applied_discount_quantity = min(item_quantity, bonus_item_quantity)

        # Return discount deal items.
        return [self.bonus_item] * applied_discount_quantity
                
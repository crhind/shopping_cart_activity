
from logging import getLogger
from copy import deepcopy
from typing import List

from src.item import Item

logger = getLogger(__name__)


class Deal:
    associated_item: Item

    def apply(self, cart: List[Item]) -> List[Item]:
        pass

class DiscountDeal(Deal):
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
        item_quantity = len(list(filter(lambda item, key=self.associated_item.sku: item.sku == key, cart)))
        if item_quantity >= self.discount_quantity:
            return [Item(sku='DSC', name=self.description, price=-self.discount)] * item_quantity
        return list()
class BundleDeal(Deal):
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
        matching_items = filter(lambda item, key=self.associated_item.sku: item.sku == key, cart)
        return [Item(sku='DSC', name=self.description, price=-self.discount)] * (len(list(matching_items)) // self.bundle_quantity)
            
class AccessoryDeal(Deal):
    def __init__(self, associated_item: Item, bonus_item: Item) -> None:
        self.associated_item = associated_item
        self.bonus_item = deepcopy(bonus_item)
        self.bonus_item.price *= -1
    
    def apply(self, cart: List[Item]) -> List[Item]:
        logger.info(f'Applying all accessory deals.')
        # Do we need to check if the vga is in cart already to apply the discount? 
        item_quantity = len(list(filter(lambda item, key=self.associated_item.sku: item.sku == key, cart)))
        bonus_item_quantity = len(list(filter(lambda item, key=self.bonus_item.sku: item.sku == key, cart)))
        
        applied_discount_quantity = min(item_quantity, bonus_item_quantity)

        return [self.bonus_item] * applied_discount_quantity
                
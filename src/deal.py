
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
        return [Item(sku='DSC', name=self.description, price=-self.discount) for item in cart if self.associated_item is item]

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
        return [Item(sku='DSC', name=self.description, price=-self.discount) for x in list(matching_items)[::self.bundle_quantity]]
            
class AccessoryDeal(Deal):
    def __init__(self, associated_item: Item, bonus_item: Item) -> None:
        self.associated_item = associated_item
        self.bonus_item = deepcopy(bonus_item)
        self.bonus_item.price = 0.0
    
    def apply(self, cart: List[Item]) -> List[Item]:
        logger.info(f'Applying all accessory deals.')
        return [self.bonus_item for item in cart if item is self.associated_item]
                
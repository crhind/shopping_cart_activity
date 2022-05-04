
from typing import Dict, List, Set
import yaml 

from src.deal import AccessoryDeal, BundleDeal, Deal, DiscountDeal
from src.item import Item


def load_items(filename: str) -> Dict[str, Item]:
    '''
    Reads the items yaml file and returns the corresponding dictionary.
    Dictionary mapping is item_sku: Item instance
    '''
    items = dict()
    with open(filename, 'r') as f:
        for k, v in yaml.safe_load(f).items():
            items[k] = Item(sku=k, name=v['name'], price=float(v['price']))
    return items


def load_deals(filename: str, items: Dict[str, Item]) -> Set[Deal]:
    '''Reads the deals yaml file and return the set of currently deals.'''
    deals = list()
    with open(filename, 'r') as f:
        for k, v in yaml.safe_load(f).items():
            associated_item = items[v.pop('item_sku')]
            # The below functionality could be shifted out to a factory.
            if k == 'bundle':
                deal = BundleDeal(
                    associated_item=associated_item,
                    bundle_quantity=int(v['bundle_quantity']),
                    discount_quantity=int(v['discount_quantity'])
                )
            elif k == 'discount':
                deal = DiscountDeal(
                    associated_item=associated_item,
                    discount_quantity=int(v['discount_quantity']),
                    discount_price=float(v['discount_price'])
                )
            elif k == 'accessory':
                bonus_item = items[v['bonus_item_sku']]
                deal = AccessoryDeal(
                    associated_item=associated_item,
                    bonus_item=bonus_item
                )
            else: 
                raise ValueError(f'Invalid deal keyword - {k}')
            deals.append(deal)
    return set(deals)

        
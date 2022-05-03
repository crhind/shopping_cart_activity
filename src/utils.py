
from typing import Dict, List, Set
import yaml 

from src.deal import AccessoryDeal, BundleDeal, Deal, DiscountDeal
from src.item import Item


def load_items(filename: str) -> List[Item]:
    items = dict()
    with open(filename, 'r') as f:
        for k,v in yaml.safe_load(f).items():
            print(f'k: {k}, v: {v}')
            items[k] = Item(sku=k, name=v['name'], price=float(v['price']))
    print(items)
    return items


def load_deals(filename: str, items: Dict[str, Item]) -> Set[Deal]:
    deals = list()
    with open(filename, 'r') as f:
        for k, v in yaml.safe_load(f).items():
            print(f'k: {k}, v: {v}')
            associated_item = items[v.pop('item_sku')]
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
    print(deals)
    return set(deals)

        
# DiUS Shopping Example. 
Simple shopping cart application that allows configuration of specials/deals that get applied at checkout time. Users interact with the application through a CLI.

Tested with Python3.8 (but should work in Python3.7+).
Wont work with Python2.x as f-strings are used everywhere.

## Usage
To use simply navigate to the top level directory and run
```bash
python3.8 run.py
``` 
This will open a command prompt for the application and allow users to begin interacting with the checkout. 

All the commands can be found by running the `help` command.
For individual command usage run `help <command>`. 
```
> help

Documented commands (type help <topic>):
========================================
add  display_cart  exit  help  list_items  total

> help add

Adds an item to the checkou. Requires an item sku to be provided.
```

To exit the command prompt simply run the  `exit` command.
```
> exit

Exiting...
```

## Adding Items.
All of the items are imported to the system from a top level yaml file, [items.yaml](items.yaml).

This yaml file can be extended as needed to include other items. The expected schema is simple:
```yaml
<sku>:
    name: <item_name>
    price: <item_price>
```

__Note:__ Item sku's are treated as unique within the system. Do not reuse item sku's

## Adding Deals. 
Similarly to items, the deals are imported to the system from a top level file, [deals.yaml](deals.yaml).

The currently available deal types are:
* BundleDeal. Template is buy X for the price of Y.
    Example: _"we're going to have a 3 for 2 deal on Apple TVs. For example, if you buy 3 Apple TVs, you will pay the price of 2 only"_

* DiscountDeal. Template is buy X or more items, get them at a bulk discount price
    Example: _"the brand new Super iPad will have a bulk discounted applied, where the price will drop to $499.99 each, if someone buys more than 4"_
* AccessoryDeal. Template is by one item get another as a bonus.
    Example: _"we will bundle in a free VGA adapter free of charge with every MacBook Pro sold"_

The yaml schema for deals is simple and just follows the deal class fields:
```yaml
<deal-type>:
    item_sku: <associated_item_sku>
    <deal-fields>

bundle:
    item_sku: <associated_item_sku>
    bundle_quantity: <quantity of items for deal condition>
    discount_quantity: <effective quantity of items paid for.>

discount:
    item_sku: <associated_item_sku>
    discount_quantity: <quantity of items for deal condition>
    discount_price: <discounted price per unit.>

accessory:
    item_sku: <associated_item_sku>
    bonus_item_sku: <bonus_item_sku>
```


## Run Tests
Testing is done using the builtin testing framework [unittest](https://docs.python.org/3/library/unittest.html)

To run all tests, from the top level project directoy run
```bash
python3 -m unittest
```
unittest ships with an autodiscover feature for finding test cases.
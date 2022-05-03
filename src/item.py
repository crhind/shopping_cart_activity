
from dataclasses import dataclass

@dataclass
class Item:
    sku: str
    name: str
    price: float

    def __str__(self) -> str:
        return f'{self.sku} | {self.price:.2f} | {self.name}'

    @property
    def line_description(self) -> str:
        return f'Code: {self.sku}\n\t{self.name}\n\t{"="*10} {self.price}'
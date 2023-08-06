import inspect
from dataclasses import dataclass

import jsons

@dataclass
class Parent:
    parent_attr: str
    # def __init__(self, parent_attr):
    #     self.parent_attr = parent_attr


class Child(Parent):
    def __init__(self, parent_attr, child_attr):
        super().__init__(parent_attr)
        self.child_attr = child_attr

child = Child('p', 'c')

members = inspect.getmembers(child)

dumped = jsons.dump(child, cls=Parent)

# inspect.classify_class_attrs(cls)

print(dumped)
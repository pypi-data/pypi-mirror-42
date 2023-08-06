from typing import Union

from jsons import set_deserializer, default_union_deserializer

set_deserializer(default_union_deserializer, Union)


import typing
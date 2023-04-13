import dataclasses
import json
from abc import abstractmethod
from typing import List

from conf import log


def jsonify(obj: dataclasses.dataclass, unwanted_keys: List[str] = []) -> str:
    if hasattr(obj, 'json'):
        log.debug(f"implemented json attribute {obj.json}")
        return obj.json

    obj_dict = dataclasses.asdict(obj)
    for key in unwanted_keys:
        del obj_dict[key]

    json_str = json.dumps(obj_dict)

    return json_str


@dataclasses.dataclass
class DataClassJson:

    @staticmethod
    @abstractmethod
    def Loads(json_str: str) -> object:
        pass

    @property
    def json(self) -> str:
        return jsonify(self)

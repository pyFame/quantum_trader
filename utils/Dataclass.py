import dataclasses
import json
from abc import abstractmethod


def jsonify(obj: dataclasses.dataclass) -> str:
    obj_dict = dataclasses.asdict(obj)
    json_str = json.dumps(obj_dict)

    return json_str


class DataClassJson:

    @staticmethod
    @abstractmethod
    def Loads(json_str: str) -> object:
        pass

    @property
    def json(self) -> str:
        return jsonify(self)

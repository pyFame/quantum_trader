import dataclasses
import json


def jsonify(obj: dataclasses.dataclass) -> str:
    obj_dict = dataclasses.asdict(obj)
    json_str = json.dumps(obj_dict)

    return json_str


class DataClassJson:
    @property
    def json(self) -> str:
        return jsonify(self)

import json
from dataclasses import is_dataclass, asdict


def dumps(payload) -> str:
    if is_dataclass(payload):
        return json.dumps(asdict(payload), ensure_ascii=False)
    if isinstance(payload, list):
        return json.dumps([dumps(i) for i in payload])
    if isinstance(payload, dict):
        return json.dumps({k: dumps(v) for k, v in payload.items()})
    return json.dumps(payload, ensure_ascii=False)

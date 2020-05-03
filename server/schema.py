import logging as l
from dataclasses import dataclass, fields, is_dataclass

# noinspection Mypy,PyUnresolvedReferences
from typing import List, _GenericAlias, get_origin, get_args

LOGGER = l.getLogger(__name__)


class SchemaError:
    pass


@dataclass
class CommonError(SchemaError):
    message: str

    def __str__(self):
        return self.message

    def __repr__(self):
        return f"SchemaError: {self.message}"


@dataclass
class NotFoundKeyError(SchemaError):
    key: str

    def __str__(self):
        return f"not found key {self.key}"

    # def __repr__(self):
    #     return f"NotFoundKeyError: {self.key}"


@dataclass
class WrongTypeError(SchemaError):
    key: str
    expect_type: type
    actual_type: type

    # def __repr__(self):
    #     return f"{self.__class__.__name__}: " \
    #            f"{self.key} {self.expect_type} {self.actual_type}"


@dataclass
class ElementWrongType(WrongTypeError):
    index: int


def validate(model, payload: dict, path: str = "") -> List[SchemaError]:
    if not isinstance(payload, dict):
        return [SchemaError()]
    model_fields = fields(model)
    errors: List[SchemaError] = []
    for field in model_fields:
        key = field.name
        if path:
            key = f"{path}.{field.name}"

        LOGGER.debug(f"check key '{key}'")

        if field.name not in payload.keys():
            errors.append(NotFoundKeyError(key=key))
        else:
            actualtype = type(payload[field.name])
            LOGGER.debug(f"'{key}' value exists")
            if is_dataclass(field.type):
                if actualtype != dict:
                    errors.append(
                        WrongTypeError(
                            key=key, expect_type=field.type, actual_type=actualtype
                        )
                    )
                else:
                    errors += validate(field.type, payload[field.name], path=key)

            elif isinstance(field.type, _GenericAlias):
                # it is typing module - we need to get origin and check with
                LOGGER.debug("check typing types")
                # noinspection Mypy
                origin_type: type = get_origin(field.type)
                if actualtype != origin_type:
                    errors.append(
                        WrongTypeError(
                            key=key,
                            expect_type=origin_type,
                            actual_type=actualtype,
                        )
                    )
                # TODO: check subtypes of field.type
                args = get_args(field.type)
                LOGGER.debug(
                    f"check field {field.name} type {field.type} arguments", args
                )
                if len(args) > 0:
                    arg = args[0]
                    if origin_type == actualtype == list:
                        for i, e in enumerate(payload[field.name]):
                            current_path = f"{key}.[{i}]"
                            LOGGER.debug("validate array", current_path)
                            errors += validate(arg, e, path=current_path)

            else:
                if actualtype != field.type:
                    errors.append(
                        WrongTypeError(
                            key=key, expect_type=field.type, actual_type=actualtype
                        )
                    )

    return errors

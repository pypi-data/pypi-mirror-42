import re
import typing
from math import isfinite

from typesystem import formats
from typesystem.base import ErrorMessage, ErrorMessages, ValidationResult

NO_DEFAULT = object()

FORMATS = {
    "date": formats.DateFormat(),
    "time": formats.TimeFormat(),
    "datetime": formats.DateTimeFormat(),
}


class Validator:
    errors = {}
    _creation_counter = 0

    def __init__(
        self,
        title="",
        description="",
        default=NO_DEFAULT,
        allow_null=False,
        definitions=None,
        def_name=None,
    ):
        definitions = {} if (definitions is None) else dict(definitions)

        assert isinstance(title, str)
        assert isinstance(description, str)
        assert isinstance(definitions, dict)
        assert all(isinstance(k, str) for k in definitions.keys())
        assert all(isinstance(v, Validator) for v in definitions.values())

        if allow_null and default is NO_DEFAULT:
            default = None

        if default is not NO_DEFAULT:
            self.default = default

        self.title = title
        self.description = description
        self.allow_null = allow_null
        self.definitions = definitions
        self.def_name = def_name

        # We need this global counter to determine what order fields have
        # been declared in when used with `Type`.
        self._creation_counter = Validator._creation_counter
        Validator._creation_counter += 1

    def validate(self, value, strict=False):
        result = self.validate_value(value, strict=strict)

        if isinstance(result, ErrorMessage):
            errors = ErrorMessages([result])
        elif isinstance(result, ErrorMessages):
            errors = result
        else:
            value = result
            errors = None

        return ValidationResult(value, errors=errors)

    def validate_value(self, value):
        raise NotImplementedError()  # pragma: no cover

    def serialize(self, obj):
        return obj

    def has_default(self):
        return hasattr(self, "default")

    def error(self, code, context=None, index=None):
        context = {} if context is None else context
        text = self.errors[code].format(**self.__dict__, **context)
        return ErrorMessage(text=text, code=code, index=index)


class String(Validator):
    errors = {
        "type": "Must be a string.",
        "null": "May not be null.",
        "blank": "Must not be blank.",
        "max_length": "Must have no more than {max_length} characters.",
        "min_length": "Must have at least {min_length} characters.",
        "pattern": "Must match the pattern /{pattern}/.",
        "format": "Must be a valid {format}.",
        "enum": "Must be one of {enum}.",
        "exact": "Must be {exact}.",
    }

    def __init__(
        self,
        max_length=None,
        min_length=None,
        pattern=None,
        enum=None,
        format=None,
        allow_blank=True,
        exact=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        assert max_length is None or isinstance(max_length, int)
        assert min_length is None or isinstance(min_length, int)
        assert pattern is None or isinstance(pattern, str)
        assert (
            enum is None
            or isinstance(enum, list)
            and all([isinstance(i, str) for i in enum])
        )
        assert format is None or isinstance(format, str)

        if not allow_blank:
            assert min_length is None
            min_length = 1

        if exact is not None:
            assert enum is None
            enum = [exact]

        self.max_length = max_length
        self.min_length = min_length
        self.pattern = pattern
        self.enum = enum
        self.format = format

    def validate_value(self, value, strict=False):
        if value is None and self.allow_null:
            return None
        elif value is None:
            return self.error("null")
        elif self.format in FORMATS and FORMATS[self.format].is_native_type(value):
            return value
        elif not isinstance(value, str):
            return self.error("type")

        if self.enum is not None:
            if value not in self.enum:
                if len(self.enum) == 1:
                    return self.error("exact", context={"exact": self.enum[0]})
                return self.error("enum")

        if self.min_length is not None:
            if len(value) < self.min_length:
                if self.min_length == 1:
                    return self.error("blank")
                else:
                    return self.error("min_length")

        if self.max_length is not None:
            if len(value) > self.max_length:
                return self.error("max_length")

        if self.pattern is not None:
            if not re.search(self.pattern, value):
                return self.error("pattern")

        if self.format in FORMATS:
            return FORMATS[self.format].validate(value)

        return value

    def serialize(self, obj):
        if self.format in FORMATS:
            return FORMATS[self.format].serialize(obj)
        return obj


class NumericType(Validator):
    """
    Base class for both `Number` and `Integer`.
    """

    numeric_type = None  # type: type
    errors = {
        "type": "Must be a number.",
        "null": "May not be null.",
        "integer": "Must be an integer.",
        "finite": "Must be finite.",
        "minimum": "Must be greater than or equal to {minimum}.",
        "exclusive_minimum": "Must be greater than {minimum}.",
        "maximum": "Must be less than or equal to {maximum}.",
        "exclusive_maximum": "Must be less than {maximum}.",
        "multiple_of": "Must be a multiple of {multiple_of}.",
        "enum": "Must be one of {enum}.",
        "exact": "Must be {exact}.",
    }

    def __init__(
        self,
        minimum=None,
        maximum=None,
        exclusive_minimum=None,
        exclusive_maximum=None,
        multiple_of=None,
        enum=None,
        format=None,
        exact=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        assert minimum is None or isinstance(minimum, self.numeric_type)
        assert maximum is None or isinstance(maximum, self.numeric_type)
        assert exclusive_minimum is None or isinstance(
            exclusive_minimum, self.numeric_type
        )
        assert exclusive_maximum is None or isinstance(
            exclusive_maximum, self.numeric_type
        )
        assert (
            multiple_of is None
            or isinstance(multiple_of, int)
            or multiple_of.is_integer()
        )
        assert (
            enum is None
            or isinstance(enum, list)
            and all([isinstance(i, self.numeric_type) for i in enum])
        )
        assert format is None or isinstance(format, str)

        if exact is not None:
            assert enum is None
            enum = [exact]

        self.minimum = minimum
        self.maximum = maximum
        self.exclusive_minimum = exclusive_minimum
        self.exclusive_maximum = exclusive_maximum
        self.multiple_of = multiple_of
        self.enum = enum
        self.format = format

    def validate_value(self, value, strict=False):
        if value is None and self.allow_null:
            return None
        elif value is None:
            return self.error("null")
        elif isinstance(value, bool):
            return self.error("type")
        elif (
            self.numeric_type is int
            and isinstance(value, float)
            and not value.is_integer()
        ):
            return self.error("integer")
        elif not isinstance(value, (int, float)) and strict:
            return self.error("type")
        elif isinstance(value, float) and not isfinite(value):
            return self.error("finite")

        try:
            value = self.numeric_type(value)
        except (TypeError, ValueError):
            return self.error("type")

        if self.enum is not None:
            if value not in self.enum:
                if len(self.enum) == 1:
                    return self.error("exact", context={"exact": self.enum[0]})
                return self.error("enum")

        if self.minimum is not None and value < self.minimum:
            return self.error("minimum")

        if self.exclusive_minimum is not None and value <= self.exclusive_minimum:
            return self.error("exclusive_minimum")

        if self.maximum is not None and value > self.maximum:
            return self.error("maximum")

        if self.exclusive_maximum is not None and value >= self.exclusive_maximum:
            return self.error("exclusive_maximum")

        if self.multiple_of is not None:
            if value % self.multiple_of:
                return self.error("multiple_of")

        return value


class Integer(NumericType):
    numeric_type = int


class Float(NumericType):
    numeric_type = float


class Boolean(Validator):
    errors = {"type": "Must be a valid boolean.", "null": "May not be null."}
    coerce_values = {
        "true": True,
        "false": False,
        "on": True,
        "off": False,
        "1": True,
        "0": False,
        "": False,
        1: True,
        0: False,
    }
    coerce_null_values = {"": None, "null": None, "none": None}

    def validate_value(self, value, strict=False):
        if value is None and self.allow_null:
            return None

        elif value is None:
            return self.error("null")

        elif not isinstance(value, bool):
            if strict:
                return self.error("type")

            if self.allow_null:
                values = dict(self.coerce_values)
                values.update(self.coerce_null_values)
            else:
                values = self.coerce_values
            try:
                if isinstance(value, str):
                    value = values[value.lower()]
                else:
                    value = values[value]
            except KeyError:
                return self.error("type")

        return value


class Object(Validator):
    errors = {
        "type": "Must be an object.",
        "null": "May not be null.",
        "invalid_key": "All object keys must be strings.",
        "required": 'The "{field_name}" field is required.',
        "invalid_property": "Invalid property name.",
        "empty": "Must not be empty.",
        "max_properties": "Must have no more than {max_properties} properties.",
        "min_properties": "Must have at least {min_properties} properties.",
    }

    def __init__(
        self,
        properties=None,
        pattern_properties=None,
        additional_properties=True,
        min_properties=None,
        max_properties=None,
        required=None,
        coerce=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        properties = {} if (properties is None) else dict(properties)
        pattern_properties = (
            {} if (pattern_properties is None) else dict(pattern_properties)
        )
        required = list(required) if isinstance(required, (list, tuple)) else required
        required = [] if (required is None) else required

        assert all(isinstance(k, str) for k in properties.keys())
        assert all(hasattr(v, "validate") for v in properties.values())
        assert all(isinstance(k, str) for k in pattern_properties.keys())
        assert all(hasattr(v, "validate") for v in pattern_properties.values())
        assert additional_properties in (None, True, False) or hasattr(
            additional_properties, "validate"
        )
        assert min_properties is None or isinstance(min_properties, int)
        assert max_properties is None or isinstance(max_properties, int)
        assert all(isinstance(i, str) for i in required)

        self.properties = properties
        self.pattern_properties = pattern_properties
        self.additional_properties = additional_properties
        self.min_properties = min_properties
        self.max_properties = max_properties
        self.required = required
        self.coerce = coerce

    def validate_value(self, value, strict=False):
        if value is None and self.allow_null:
            return None
        elif value is None:
            return self.error("null")
        elif not isinstance(value, (dict, typing.Mapping)):
            return self.error("type")

        validated = {}
        errors = []

        # Ensure all property keys are strings.
        for key in value.keys():
            if not isinstance(key, str):
                return self.error("invalid_key")

        # Min/Max properties
        if self.min_properties is not None:
            if len(value) < self.min_properties:
                if self.min_properties == 1:
                    return self.error("empty")
                else:
                    return self.error("min_properties")
        if self.max_properties is not None:
            if len(value) > self.max_properties:
                return self.error("max_properties")

        # Required properties
        for key in self.required:
            if key not in value:
                error = self.error("required", context={"field_name": key}, index=[key])
                errors.append(error)

        # Properties
        for key, child_schema in self.properties.items():
            if key not in value:
                if child_schema.has_default():
                    validated[key] = child_schema.default
                continue
            item = value[key]
            child = child_schema.validate(item, strict=strict)
            if child.is_valid:
                validated[key] = child.value
            else:
                for error in child.errors:
                    error = error.with_index_prefix(prefix=key)
                    errors.append(error)

        # Pattern properties
        if self.pattern_properties:
            for key in list(value.keys()):
                for pattern, child_schema in self.pattern_properties.items():
                    if isinstance(key, str) and re.search(pattern, key):
                        item = value[key]
                        child = child_schema.validate(item, strict=strict)
                        if child.is_valid:
                            validated[key] = child.value
                        else:
                            for error in child.errors:
                                errors.append(error.with_index_prefix(prefix=key))

        # Additional properties
        validated_keys = set(validated.keys())
        error_keys = set([error.index[0] for error in errors if error.index])

        remaining = [
            key for key in value.keys() if key not in validated_keys | error_keys
        ]

        if self.additional_properties is True:
            for key in remaining:
                validated[key] = value[key]
        elif self.additional_properties is False:
            for key in remaining:
                error = self.error("invalid_property", index=[key])
                errors.append(error)
        elif self.additional_properties is not None:
            child_schema = self.additional_properties
            for key in remaining:
                item = value[key]
                child = child_schema.validate(item, strict=strict)
                if child.is_valid:
                    validated[key] = child.value
                else:
                    for error in child.errors:
                        error = error.with_index_prefix(prefix=key)
                        errors.append(error)

        if errors:
            return ErrorMessages(errors)

        if self.coerce is not None:
            return self.coerce(validated)

        return validated


# class Array(Validator):
#     errors = {
#         'type': 'Must be an array.',
#         'null': 'May not be null.',
#         'empty': 'Must not be empty.',
#         'exact_items': 'Must have {min_items} items.',
#         'min_items': 'Must have at least {min_items} items.',
#         'max_items': 'Must have no more than {max_items} items.',
#         'additional_items': 'May not contain additional items.',
#         'unique_items': 'This item is not unique.',
#     }
#
#     def __init__(self, items=None, additional_items=None, min_items=None,
#                  max_items=None, unique_items=False, **kwargs):
#         super().__init__(**kwargs)
#
#         items = list(items) if isinstance(items, (list, tuple)) else items
#
#         assert items is None or hasattr(items, 'validate') or (
#             isinstance(items, list) and
#             all(hasattr(i, 'validate') for i in items)
#         )
#         assert additional_items in (None, True, False) or hasattr(additional_items, 'validate')
#         assert min_items is None or isinstance(min_items, int)
#         assert max_items is None or isinstance(max_items, int)
#         assert isinstance(unique_items, bool)
#
#         self.items = items
#         self.additional_items = additional_items
#         self.min_items = min_items
#         self.max_items = max_items
#         self.unique_items = unique_items
#
#     def validate(self, value, definitions=None, allow_coerce=False):
#         if value is None and self.allow_null:
#             return None
#         elif value is None:
#             self.error('null')
#         elif not isinstance(value, list):
#             self.error('type')
#
#         definitions = self.get_definitions(definitions)
#         validated = []
#
#         if self.min_items is not None and self.min_items == self.max_items and len(value) != self.min_items:
#             self.error('exact_items')
#         if self.min_items is not None and len(value) < self.min_items:
#             if self.min_items == 1:
#                 self.error('empty')
#             self.error('min_items')
#         elif self.max_items is not None and len(value) > self.max_items:
#             self.error('max_items')
#         elif isinstance(self.items, list) and (self.additional_items is False) and len(value) > len(self.items):
#             self.error('additional_items')
#
#         # Ensure all items are of the right type.
#         errors = {}
#         if self.unique_items:
#             seen_items = Uniqueness()
#
#         for pos, item in enumerate(value):
#             try:
#                 if isinstance(self.items, list):
#                     if pos < len(self.items):
#                         item = self.items[pos].validate(
#                             item,
#                             definitions=definitions,
#                             allow_coerce=allow_coerce
#                         )
#                     elif isinstance(self.additional_items, Validator):
#                         item = self.additional_items.validate(
#                             item,
#                             definitions=definitions,
#                             allow_coerce=allow_coerce
#                         )
#                 elif self.items is not None:
#                     item = self.items.validate(
#                         item,
#                         definitions=definitions,
#                         allow_coerce=allow_coerce
#                     )
#
#                 if self.unique_items:
#                     if item in seen_items:
#                         self.error('unique_items')
#                     else:
#                         seen_items.add(item)
#
#                 validated.append(item)
#             except ValidationError as exc:
#                 errors[pos] = exc.messages
#
#         if errors:
#             error_messages = []
#             for key, messages in errors.items():
#                 for message in messages:
#                     index = [key] if message.index is None else [key] + message.index
#                     error_message = ErrorMessage(message.text, message.code, index)
#                     error_messages.append(error_message)
#             raise ValidationError(error_messages)
#
#         return validated


class Text(String):
    def __init__(self, **kwargs):
        super().__init__(format="text", **kwargs)


class Date(String):
    def __init__(self, **kwargs):
        super().__init__(format="date", **kwargs)


class Time(String):
    def __init__(self, **kwargs):
        super().__init__(format="time", **kwargs)


class DateTime(String):
    def __init__(self, **kwargs):
        super().__init__(format="datetime", **kwargs)


# class Any(Validator):
#     def validate(self, value, definitions=None, allow_coerce=False):
#         # TODO: Validate value matches primitive types
#         return value
#
#
# class Union(Validator):
#     errors = {
#         'null': 'Must not be null.',
#         'union': 'Must match one of the union types.'
#     }
#
#     def __init__(self, items, **kwargs):
#         super().__init__(**kwargs)
#         assert isinstance(items, list) and all(isinstance(i, Validator) for i in items)
#         self.items = list(items)
#
#     def validate(self, value, definitions=None, allow_coerce=False):
#         if value is None and self.allow_null:
#             return None
#         elif value is None:
#             self.error('null')
#
#         for item in self.items:
#             try:
#                 return item.validate(
#                     value,
#                     definitions=definitions,
#                     allow_coerce=allow_coerce
#                 )
#             except ValidationError:
#                 pass
#         self.error('union')
#
#
# class Ref(Validator):
#     def __init__(self, ref, **kwargs):
#         super().__init__(**kwargs)
#         assert isinstance(ref, str)
#         self.ref = ref
#
#     def validate(self, value, definitions=None, allow_coerce=False):
#         assert definitions is not None, 'Ref.validate() requires definitions'
#         assert self.ref in definitions, 'Ref "%s" not in definitions' % self.ref
#
#         child_schema = definitions[self.ref]
#         return child_schema.validate(
#             value,
#             definitions=definitions,
#             allow_coerce=allow_coerce
#         )
#
#
# class Uniqueness():
#     """
#     A set-like class that tests for uniqueness of primitive types.
#     Ensures the `True` and `False` are treated as distinct from `1` and `0`,
#     and coerces non-hashable instances that cannot be added to sets,
#     into hashable representations that can.
#     """
#     TRUE = object()
#     FALSE = object()
#
#     def __init__(self):
#         self._set = set()
#
#     def __contains__(self, item):
#         item = self.make_hashable(item)
#         return item in self._set
#
#     def add(self, item):
#         item = self.make_hashable(item)
#         self._set.add(item)
#
#     def make_hashable(self, element):
#         """
#         Coerce a primitive into a uniquely hashable type, for uniqueness checks.
#         """
#
#         # Only primitive types can be handled.
#         assert (element is None) or isinstance(element, (bool, int, float, str, list, dict))
#
#         if element is True:
#             # Need to make `True` distinct from `1`.
#             return self.TRUE
#         elif element is False:
#             # Need to make `False` distinct from `0`.
#             return self.FALSE
#         elif isinstance(element, list):
#             # Represent lists using a two-tuple of ('list', (item, item, ...))
#             return ('list', tuple([
#                 self.make_hashable(item) for item in element
#             ]))
#         elif isinstance(element, dict):
#             # Represent dicts using a two-tuple of ('dict', ((key, val), (key, val), ...))
#             return ('dict', tuple([
#                 (self.make_hashable(key), self.make_hashable(value)) for key, value in element.items()
#             ]))
#
#         return element

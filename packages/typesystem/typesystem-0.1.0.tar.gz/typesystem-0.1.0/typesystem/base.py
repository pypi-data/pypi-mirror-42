import typing
from collections.abc import Mapping


class ErrorMessage:
    def __init__(self, *, text: str, code: str, index: list = None):
        self.text = text
        self.code = code
        self.index = [] if index is None else index

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, ErrorMessage) and (
            self.text == other.text
            and self.code == other.code
            and self.index == other.index
        )


class ValidationError(Mapping):
    def __init__(
        self,
        *,
        text: str = None,
        code: str = None,
        messages: typing.List[ErrorMessage] = None
    ):
        if messages is None:
            # Instantiated as a ValidationError with a single error message.
            assert text is not None
            assert code is not None
            messages = [ErrorMessage(text=text, code=code)]
        else:
            # Instantiated as a ValidationError with multiple error messages.
            assert text is None
            assert code is None

        self._messages = messages
        self._message_dict = (
            {}
        )  # type: typing.Dict[typing.Any, typing.Union[str, dict]]

        # Populate 'self._message_dict'
        for message in messages:
            insert_into = self._message_dict
            for key in message.index[:-1]:
                insert_into = insert_into.setdefault(key, {})  # type: ignore
            insert_key = message.index[-1] if message.index else ""
            insert_into[insert_key] = message.text

    def messages(
        self, *, add_prefix: typing.Union[str, int] = None
    ) -> typing.List[ErrorMessage]:
        if add_prefix is not None:
            return [
                ErrorMessage(
                    text=message.text,
                    code=message.code,
                    index=[add_prefix] + message.index,
                )
                for message in self._messages
            ]
        return list(self._messages)

    def __iter__(self) -> typing.Iterator:
        return iter(self._message_dict)

    def __len__(self) -> int:
        return len(self._message_dict)

    def __getitem__(self, key: typing.Any) -> typing.Union[str, dict]:
        return self._message_dict[key]

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, ValidationError) and self._messages == other._messages


class ValidationResult:
    def __init__(
        self, *, value: typing.Any = None, error: ValidationError = None
    ) -> None:
        self.value = value
        self.error = error

    def __iter__(self) -> typing.Iterator:
        yield self.value
        yield self.error

    def __bool__(self) -> bool:
        return self.error is None

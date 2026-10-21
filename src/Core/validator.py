from src.exceptions import (
    AbstractException,
    LengthException,
    TypeException,
    ValueException,
)

operation_exception = AbstractException

class validator:
    """
    Набор статических методов для проверки значений.
    Все методы бросают исключения из src.exceptions.
    """

    @staticmethod
    def validate_type(value, expected_type, field_name: str = "value") -> None:
        if not isinstance(value, expected_type):
            raise TypeException(
                field_name,
                expected_type.__name__ if isinstance(expected_type, type)
                else str(expected_type),
                type(value).__name__,
            )

    @staticmethod
    def validate_not_empty(value: str, field_name: str = "value") -> None:
        if not isinstance(value, str):
            raise TypeException(field_name, "str", type(value).__name__)
        if not value or not value.strip():
            raise ValueException(field_name, f"поле '{field_name}' не может быть пустым")

    @staticmethod
    def validate_length(value: str, max_length: int, field_name: str = "value") -> None:
        if not isinstance(value, str):
            raise TypeException(field_name, "str", type(value).__name__)
        if len(value) > max_length:
            raise LengthException(field_name, max_length, len(value))

    @staticmethod
    def validate_digits(value: str, length: int, field_name: str = "value") -> None:
        if not isinstance(value, str):
            raise TypeException(field_name, "str", type(value).__name__)
        if not value.isdigit() or len(value) != length:
            raise ValueException(
                field_name,
                f"поле '{field_name}' должно состоять из {length} цифр",
            )

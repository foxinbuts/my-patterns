"""Тесты ядра: validator, abstract_manager. 3 теста."""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.Core.abstract_manager import abstract_manager
from src.Core.validator import validator
from src.exceptions import LengthException, TypeException, ValueException


class TestCore(unittest.TestCase):

    def test_validator_type_and_empty(self):
        """Валидатор: тип и пустота."""
        validator.validate_type("abc", str, "f")
        with self.assertRaises(TypeException):
            validator.validate_type(123, str, "f")
        with self.assertRaises(ValueException):
            validator.validate_not_empty("   ", "f")

    def test_validator_length_and_digits(self):
        """Валидатор: длина и цифры."""
        with self.assertRaises(LengthException):
            validator.validate_length("abcdef", 5, "f")
        with self.assertRaises(ValueException):
            validator.validate_digits("12a45", 5, "f")

    def test_abstract_manager_not_instantiable(self):
        """abstract_manager — ABC."""
        with self.assertRaises(TypeError):
            abstract_manager()


if __name__ == "__main__":
    unittest.main()

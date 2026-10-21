"""Тесты моделей: 5 тестов."""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.abstract import abstract_model
from src.exceptions import ValueException
from src.models.group_model import group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.organization_model import organization_model
from src.models.range_model import range_model
from src.models.warehouse_model import warehouse_model


class TestModels(unittest.TestCase):

    def test_range_convert(self):
        """Тонна → кг → грамм."""
        gram = range_model("грамм", 1)
        kg = range_model("кг", 1000, gram)
        ton = range_model("тонна", 1000, kg)
        self.assertEqual(ton.convert_to_base(1), 1_000_000.0)

    def test_group_strip_and_validate(self):
        """Группа: strip + запрет пустого."""
        self.assertEqual(group_model("  Молочные  ").name, "Молочные")
        with self.assertRaises(ValueException):
            group_model("")

    def test_nomenclature_links(self):
        """Номенклатура хранит ссылки на группу и единицу."""
        g = group_model("Овощи")
        u = range_model("кг", 1000, range_model("грамм", 1))
        n = nomenclature_model("Картофель", "Картофель свежий", g, u)
        self.assertIs(n.group, g)
        self.assertIs(n.range_unit, u)

    def test_organization_fields(self):
        """Организация: ИНН/БИК/счёт/форма."""
        org = organization_model(
            "ООО Ромашка", "1234567890", "044525225",
            "40702810123456789012", "ООО",
        )
        self.assertEqual(org.inn, "1234567890")
        self.assertEqual(org.account, "40702810123456789012")
        with self.assertRaises(ValueException):
            organization_model("Орг", "123", "044525225", "40702810123456789012", "ООО")

    def test_warehouse_default_and_inherit(self):
        """Склад: адрес по умолчанию + наследование."""
        w = warehouse_model("Склад")
        self.assertEqual(w.address, "")
        self.assertIsInstance(w, abstract_model)
        self.assertIsNotNone(w.id)


if __name__ == "__main__":
    unittest.main()

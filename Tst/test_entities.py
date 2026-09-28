"""
Автотесты моделей данных.
Покрывают корректное создание всех моделей со всеми вариантами параметров
и работу с моделью единицы измерения.
"""
import unittest
import sys
import os

# Добавляем корень проекта в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.abstract import abstract_model
from src.models.range_model import range_model
from src.models.group_model import group_model
from src.models.nomenclature_model import nomenclature_model
from src.models.organization_model import organization_model
from src.models.warehouse_model import warehouse_model
from src.exceptions import (
    ArgumentException,
    LengthException,
    TypeException,
    ValueException,
)


class TestRangeModel(unittest.TestCase):
    """Тесты модели единицы измерения (range_model)."""

    def test_create_base_unit(self):
        """Базовая единица: грамм с коэффициентом 1."""
        gram = range_model("грамм", 1)
        self.assertEqual(gram.name, "грамм")
        self.assertEqual(gram.coefficient, 1.0)
        self.assertIsNone(gram.base)
        self.assertIsInstance(gram, abstract_model)
        self.assertIsNotNone(gram.id)

    def test_create_derived_unit(self):
        """Производная единица: кг на основе грамма."""
        gram = range_model("грамм", 1)
        kg = range_model("кг", 1000, gram)
        self.assertEqual(kg.name, "кг")
        self.assertEqual(kg.coefficient, 1000.0)
        self.assertIs(kg.base, gram)

    def test_create_with_default_coefficient(self):
        """Создание только с именем (коэффициент по умолчанию = 1)."""
        unit = range_model("штука")
        self.assertEqual(unit.coefficient, 1.0)
        self.assertIsNone(unit.base)

    def test_convert_to_base_simple(self):
        """Пересчёт в базовую единицу (сама базовая)."""
        gram = range_model("грамм", 1)
        self.assertEqual(gram.convert_to_base(5), 5.0)

    def test_convert_to_base_derived(self):
        """Пересчёт кг → граммы."""
        gram = range_model("грамм", 1)
        kg = range_model("кг", 1000, gram)
        self.assertEqual(kg.convert_to_base(2), 2000.0)

    def test_convert_to_base_nested(self):
        """Вложенный пересчёт: тонна → кг → грамм."""
        gram = range_model("грамм", 1)
        kg = range_model("кг", 1000, gram)
        ton = range_model("тонна", 1000, kg)
        self.assertEqual(ton.convert_to_base(1), 1_000_000.0)

    def test_invalid_name_empty(self):
        with self.assertRaises(ValueException):
            range_model("")

    def test_invalid_name_type(self):
        with self.assertRaises(TypeException):
            range_model(123)

    def test_invalid_name_too_long(self):
        with self.assertRaises(LengthException):
            range_model("а" * 51)

    def test_invalid_coefficient_zero(self):
        with self.assertRaises(ValueException):
            range_model("кг", 0)

    def test_invalid_coefficient_negative(self):
        with self.assertRaises(ValueException):
            range_model("кг", -10)

    def test_invalid_coefficient_type(self):
        with self.assertRaises(TypeException):
            range_model("кг", "1000")

    def test_invalid_base_type(self):
        with self.assertRaises(TypeException):
            range_model("кг", 1000, base="not_a_range")

    def test_example_from_task(self):
        """Пример из ТЗ: base_range = range_model('грамм', 1); new_range = range_model('кг', 1000, base_range)"""
        base_range = range_model("грамм", 1)
        new_range = range_model("кг", 1000, base_range)
        self.assertEqual(base_range.name, "грамм")
        self.assertEqual(base_range.coefficient, 1)
        self.assertIsNone(base_range.base)
        self.assertEqual(new_range.name, "кг")
        self.assertEqual(new_range.coefficient, 1000)
        self.assertIs(new_range.base, base_range)


class TestGroupModel(unittest.TestCase):
    """Тесты модели группы номенклатуры."""

    def test_create_ok(self):
        g = group_model("Мясные продукты")
        self.assertEqual(g.name, "Мясные продукты")
        self.assertIsInstance(g, abstract_model)
        self.assertIsNotNone(g.id)

    def test_create_with_strip(self):
        g = group_model("  Молочные  ")
        self.assertEqual(g.name, "Молочные")

    def test_empty_name(self):
        with self.assertRaises(ValueException):
            group_model("")

    def test_name_too_long(self):
        with self.assertRaises(LengthException):
            group_model("а" * 51)

    def test_name_wrong_type(self):
        with self.assertRaises(TypeException):
            group_model(None)


class TestNomenclatureModel(unittest.TestCase):
    """Тесты модели номенклатуры."""

    def setUp(self):
        self.group = group_model("Овощи")
        self.unit = range_model("кг", 1000, range_model("грамм", 1))

    def test_create_ok(self):
        n = nomenclature_model(
            name="Картофель",
            full_name="Картофель свежий мытый",
            group=self.group,
            range_unit=self.unit,
        )
        self.assertEqual(n.name, "Картофель")
        self.assertEqual(n.full_name, "Картофель свежий мытый")
        self.assertIs(n.group, self.group)
        self.assertIs(n.range_unit, self.unit)
        self.assertIsInstance(n, abstract_model)

    def test_name_max_50(self):
        name_50 = "а" * 50
        n = nomenclature_model(name_50, "полное", self.group, self.unit)
        self.assertEqual(len(n.name), 50)

    def test_name_too_long(self):
        with self.assertRaises(LengthException):
            nomenclature_model("а" * 51, "полное", self.group, self.unit)

    def test_full_name_max_255(self):
        full_255 = "б" * 255
        n = nomenclature_model("Имя", full_255, self.group, self.unit)
        self.assertEqual(len(n.full_name), 255)

    def test_full_name_too_long(self):
        with self.assertRaises(LengthException):
            nomenclature_model("Имя", "б" * 256, self.group, self.unit)

    def test_empty_name(self):
        with self.assertRaises(ValueException):
            nomenclature_model("", "полное", self.group, self.unit)

    def test_empty_full_name(self):
        with self.assertRaises(ValueException):
            nomenclature_model("Имя", "", self.group, self.unit)

    def test_wrong_group_type(self):
        with self.assertRaises(TypeException):
            nomenclature_model("Имя", "полное", "not_group", self.unit)

    def test_wrong_unit_type(self):
        with self.assertRaises(TypeException):
            nomenclature_model("Имя", "полное", self.group, "not_unit")

    def test_includes_group_and_unit(self):
        """П.8: номенклатура включает группу и единицу измерения."""
        n = nomenclature_model("Морковь", "Морковь столовая", self.group, self.unit)
        self.assertIsInstance(n.group, group_model)
        self.assertIsInstance(n.range_unit, range_model)


class TestOrganizationModel(unittest.TestCase):
    """Тесты модели организации."""

    def test_create_ok_ul(self):
        """Юридическое лицо (ИНН 10 цифр)."""
        org = organization_model(
            name="ООО Ромашка",
            inn="1234567890",
            bik="044525225",
            account="40702810123456789012",
            ownership_form="ООО",
        )
        self.assertEqual(org.name, "ООО Ромашка")
        self.assertEqual(org.inn, "1234567890")
        self.assertEqual(org.bik, "044525225")
        self.assertEqual(org.account, "40702810123456789012")
        self.assertEqual(org.ownership_form, "ООО")
        self.assertIsInstance(org, abstract_model)

    def test_create_ok_ip(self):
        """ИП (ИНН 12 цифр)."""
        org = organization_model(
            name="ИП Иванов",
            inn="123456789012",
            bik="044525225",
            account="40802810123456789012",
            ownership_form="ИП",
        )
        self.assertEqual(org.inn, "123456789012")

    def test_invalid_inn_length(self):
        with self.assertRaises(ValueException):
            organization_model("Орг", "123", "044525225", "40702810123456789012", "ООО")

    def test_invalid_inn_letters(self):
        with self.assertRaises(ValueException):
            organization_model(
                "Орг", "123456789a", "044525225", "40702810123456789012", "ООО"
            )

    def test_invalid_bik(self):
        with self.assertRaises(ValueException):
            organization_model(
                "Орг", "1234567890", "123", "40702810123456789012", "ООО"
            )

    def test_invalid_account(self):
        with self.assertRaises(ValueException):
            organization_model(
                "Орг", "1234567890", "044525225", "12345", "ООО"
            )

    def test_empty_ownership(self):
        with self.assertRaises(ValueException):
            organization_model(
                "Орг", "1234567890", "044525225", "40702810123456789012", ""
            )

    def test_name_too_long(self):
        with self.assertRaises(LengthException):
            organization_model(
                "а" * 51, "1234567890", "044525225", "40702810123456789012", "ООО"
            )


class TestWarehouseModel(unittest.TestCase):
    """Тесты модели склада."""

    def test_create_ok(self):
        w = warehouse_model("Основной склад", "Производственный цех, холодильник №1")
        self.assertEqual(w.name, "Основной склад")
        self.assertEqual(w.address, "Производственный цех, холодильник №1")
        self.assertIsInstance(w, abstract_model)

    def test_create_without_address(self):
        w = warehouse_model("Склад доставки")
        self.assertEqual(w.name, "Склад доставки")
        self.assertEqual(w.address, "")

    def test_empty_name(self):
        with self.assertRaises(ValueException):
            warehouse_model("")

    def test_name_too_long(self):
        with self.assertRaises(LengthException):
            warehouse_model("а" * 51)

    def test_address_too_long(self):
        with self.assertRaises(LengthException):
            warehouse_model("Склад", "б" * 256)


class TestAllModelsInheritance(unittest.TestCase):
    """Проверка, что все модели наследуются от abstract_model."""

    def test_all_inherit(self):
        models = [
            range_model("г", 1),
            group_model("Группа"),
            nomenclature_model(
                "Товар",
                "Полное имя товара",
                group_model("Группа"),
                range_model("шт", 1),
            ),
            organization_model(
                "ООО Тест",
                "1234567890",
                "044525225",
                "40702810123456789012",
                "ООО",
            ),
            warehouse_model("Склад"),
        ]
        for m in models:
            self.assertIsInstance(m, abstract_model)
            self.assertIsNotNone(m.id)
            self.assertTrue(hasattr(m, "name"))


class TestExceptions(unittest.TestCase):
    """Проверка, что ошибки выбрасываются через внутренние классы исключений."""

    def test_exceptions_hierarchy(self):
        self.assertTrue(issubclass(LengthException, ArgumentException))
        self.assertTrue(issubclass(TypeException, ArgumentException))
        self.assertTrue(issubclass(ValueException, ArgumentException))
        self.assertTrue(issubclass(ArgumentException, Exception))


if __name__ == "__main__":
    unittest.main()

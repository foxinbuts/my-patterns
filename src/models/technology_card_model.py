from typing import Dict, List, Optional, Set

from src.abstract import abstract_model
from src.exceptions import LengthException, TypeException, ValueException
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model
from src.models.technology_card_item import technology_card_item


class technology_card_model(abstract_model):
    """
    Технологическая карта (рецептура).
    Паттерн Composite (Компоновщик): карта может включать как листовые ингредиенты
    (номенклатуру), так и другие технологические карты (полуфабрикаты).
    """

    MAX_NAME_LENGTH = 100

    def __init__(
        self,
        name: str,
        target: nomenclature_model,
        quantity: float = 1.0,
        range_unit: Optional[range_model] = None,
        items: Optional[List[technology_card_item]] = None,
    ):
        super().__init__()

        if not isinstance(name, str):
            raise TypeException("name", "str", type(name).__name__)
        if not name or not name.strip():
            raise ValueException("name", "наименование не может быть пустым")
        if len(name.strip()) > self.MAX_NAME_LENGTH:
            raise LengthException("name", self.MAX_NAME_LENGTH, len(name.strip()))
        self.name = name.strip()

        if not isinstance(target, nomenclature_model):
            raise TypeException("target", "nomenclature_model", type(target).__name__)
        self.__target = target

        if not isinstance(quantity, (int, float)):
            raise TypeException("quantity", "int | float", type(quantity).__name__)
        if quantity <= 0:
            raise ValueException("quantity", "выход продукции должен быть > 0")
        self.__quantity = float(quantity)

        unit = range_unit if range_unit is not None else target.range_unit
        if not isinstance(unit, range_model):
            raise TypeException("range_unit", "range_model", type(unit).__name__)
        self.__range_unit = unit

        self.__items: List[technology_card_item] = []
        if items is not None:
            if not isinstance(items, list):
                raise TypeException("items", "list", type(items).__name__)
            for item in items:
                self.add_item(item)

    @property
    def target(self) -> nomenclature_model:
        """Целевая номенклатура (блюдо или полуфабрикат)."""
        return self.__target

    @target.setter
    def target(self, value: nomenclature_model):
        if not isinstance(value, nomenclature_model):
            raise TypeException("target", "nomenclature_model", type(value).__name__)
        self.__target = value

    @property
    def quantity(self) -> float:
        """Выход готовой продукции по рецептуре."""
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeException("quantity", "int | float", type(value).__name__)
        if value <= 0:
            raise ValueException("quantity", "выход продукции должен быть > 0")
        self.__quantity = float(value)

    @property
    def range_unit(self) -> range_model:
        """Единица измерения выхода продукции."""
        return self.__range_unit

    @range_unit.setter
    def range_unit(self, value: range_model):
        if not isinstance(value, range_model):
            raise TypeException("range_unit", "range_model", type(value).__name__)
        self.__range_unit = value

    @property
    def items(self) -> List[technology_card_item]:
        """Список позиций/ингредиентов рецептуры."""
        return self.__items

    def add_item(self, item: technology_card_item) -> None:
        """Добавить ингредиент или вложенную техкарту."""
        if not isinstance(item, technology_card_item):
            raise TypeException("item", "technology_card_item", type(item).__name__)
        # Проверка на прямое добавление самой себя
        if item.item == self:
            raise ValueException("item", "технологическая карта не может включать саму себя")
        self.__items.append(item)

    def remove_item(self, item: technology_card_item) -> None:
        """Удалить позицию из рецептуры."""
        if item in self.__items:
            self.__items.remove(item)

    def calculate_gross_requirements(
        self,
        output_quantity: float = 1.0,
        visited_cards: Optional[Set[str]] = None,
    ) -> Dict[nomenclature_model, float]:
        """
        Рекурсивно разворачивает составную технологическую карту (Composite)
        и возвращает суммарную потребность во всех базовых листовых номенклатурах.

        :param output_quantity: требуемое количество выхода целевой номенклатуры
        :param visited_cards: множество ID посещенных карт (защита от циклов)
        :return: словарь {номенклатура: количество_в_единицах_номенклатуры}
        """
        if not isinstance(output_quantity, (int, float)):
            raise TypeException("output_quantity", "int | float", type(output_quantity).__name__)
        if output_quantity <= 0:
            raise ValueException("output_quantity", "требуемое количество должно быть > 0")

        if visited_cards is None:
            visited_cards = set()

        card_id_str = str(self.id)
        if card_id_str in visited_cards:
            raise ValueException(
                "items",
                f"Обнаружена циклическая зависимость в технологической карте '{self.name}'",
            )
        visited_cards.add(card_id_str)

        # Масштаб выпуска по отношению к базовому выходу карты
        scale = float(output_quantity) / self.__quantity
        requirements: Dict[nomenclature_model, float] = {}

        for row in self.__items:
            needed_quantity = row.quantity * scale

            if row.is_composite():
                subcard: technology_card_model = row.item  # type: ignore
                # Рекурсивно вычисляем ингредиенты вложенной карты
                sub_requirements = subcard.calculate_gross_requirements(
                    output_quantity=needed_quantity,
                    visited_cards=set(visited_cards),
                )
                for nom, req_qty in sub_requirements.items():
                    requirements[nom] = requirements.get(nom, 0.0) + req_qty
            else:
                nom: nomenclature_model = row.item  # type: ignore
                converted_qty = self._convert_units(needed_quantity, row.range_unit, nom.range_unit)
                requirements[nom] = requirements.get(nom, 0.0) + converted_qty

        return requirements

    @staticmethod
    def _convert_units(amount: float, source_unit: range_model, target_unit: range_model) -> float:
        """Переводит количество из source_unit в target_unit с учетом коэффициентов."""
        if source_unit == target_unit or source_unit.name == target_unit.name:
            return float(amount)

        # Пытаемся привести к общей базе
        try:
            source_in_base = source_unit.convert_to_base(amount)
            target_base_factor = target_unit.convert_to_base(1.0)
            if target_base_factor > 0:
                return float(source_in_base) / float(target_base_factor)
        except Exception:
            pass

        return float(amount)

    def __str__(self) -> str:
        return (
            f"technology_card_model(name={self.name!r}, target={self.__target.name!r}, "
            f"quantity={self.__quantity}, range={self.__range_unit.name!r}, "
            f"items_count={len(self.__items)})"
        )

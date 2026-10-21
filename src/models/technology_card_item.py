from typing import TYPE_CHECKING, Union

from src.abstract import abstract_model
from src.exceptions import TypeException, ValueException
from src.models.nomenclature_model import nomenclature_model
from src.models.range_model import range_model

if TYPE_CHECKING:
    from src.models.technology_card_model import technology_card_model


class technology_card_item:
    """
    Строка технологической карты.
    Может содержать конкретную номенклатуру (ингредиент)
    или вложенную технологическую карту (составная техкарта / паттерн Composite).
    """

    def __init__(
        self,
        item: Union[nomenclature_model, "technology_card_model"],
        quantity: float,
        range_unit: range_model,
    ):
        from src.models.technology_card_model import technology_card_model

        if not isinstance(item, (nomenclature_model, technology_card_model)):
            raise TypeException(
                "item",
                "nomenclature_model | technology_card_model",
                type(item).__name__,
            )
        self.__item = item

        if not isinstance(quantity, (int, float)):
            raise TypeException("quantity", "int | float", type(quantity).__name__)
        if quantity <= 0:
            raise ValueException("quantity", "количество должно быть > 0")
        self.__quantity = float(quantity)

        if not isinstance(range_unit, range_model):
            raise TypeException("range_unit", "range_model", type(range_unit).__name__)
        self.__range_unit = range_unit

    @property
    def item(self) -> Union[nomenclature_model, "technology_card_model"]:
        return self.__item

    @item.setter
    def item(self, value: Union[nomenclature_model, "technology_card_model"]):
        from src.models.technology_card_model import technology_card_model

        if not isinstance(value, (nomenclature_model, technology_card_model)):
            raise TypeException(
                "item",
                "nomenclature_model | technology_card_model",
                type(value).__name__,
            )
        self.__item = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value: float):
        if not isinstance(value, (int, float)):
            raise TypeException("quantity", "int | float", type(value).__name__)
        if value <= 0:
            raise ValueException("quantity", "количество должно быть > 0")
        self.__quantity = float(value)

    @property
    def range_unit(self) -> range_model:
        return self.__range_unit

    @range_unit.setter
    def range_unit(self, value: range_model):
        if not isinstance(value, range_model):
            raise TypeException("range_unit", "range_model", type(value).__name__)
        self.__range_unit = value

    def is_composite(self) -> bool:
        """Проверяет, является ли позиция вложенной техкартой."""
        from src.models.technology_card_model import technology_card_model

        return isinstance(self.__item, technology_card_model)

    def __str__(self) -> str:
        item_name = getattr(self.__item, "name", str(self.__item))
        return (
            f"technology_card_item(item={item_name!r}, "
            f"quantity={self.__quantity}, range_unit={self.__range_unit.name!r})"
        )

    def __repr__(self) -> str:
        return self.__str__()

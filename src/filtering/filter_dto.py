from dataclasses import dataclass, field
from typing import Any, List, Optional
from src.filtering.filter_types import FilterType


@dataclass
class FilterCondition:
    """Условие фильтрации для одного поля"""
    field_name: str     #Имя поля (поддерживается вложенность через точку: "group.name")
    filter_type: FilterType
    value: Any

    def __post_init__(self):
        if not isinstance(self.field_name, str) or not self.field_name.strip():
            raise ValueError("field_name должен быть непустой строкой")
        if not isinstance(self.filter_type, FilterType):
            raise ValueError("filter_type должен быть экзампляром FilterType")


@dataclass
class FilterDTO:
    """
    Универсальный DTO для фильтрации данных
    Поддерживается множественные условия фильтрации (логическое И)
    """
    conditions: List[FilterCondition] = field(default_factory=list)

    def add_condition(self, field_name: str, filter_type: FilterType, value: Any) -> None:
        """Добавить условие фильтрации"""
        condition = FilterCondition(field_name, filter_type, value)
        self.conditions.append(condition)

    def is_empty(self) -> bool:
        """Проверяет есть ли условия фильтрации"""
        return len(self.conditions) == 0

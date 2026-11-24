from enum import Enum


class FilterType(Enum):
    """Типы фильтрации"""
    EQUALS = "EQUALS"                       # Пролное совпадние
    LIKE = "LIKE"                           # Вхождение строки (частичное совпадение)
    LESS_THAN = "LESS_THAN"                 # Меньше
    LESS_OR_EQUAL = "LESS_OR_EQUAL"         # Меньше или равно
    GREATER_THAN = "GREATER_THAN"           # Больше
    GREATER_OR_EQUAL = "GRATER_OR_EQUAL"    # Больше или равно

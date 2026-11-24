from enum import Enum


class FilterType(Enum):
    """Типы фильтрации"""
    EQUALS = "EQUALS"   #Пролное совпадние
    LIKE = "LIKE"       # Вхождение строки (частичное совпадение)

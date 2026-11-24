from datetime import datetime
from typing import Any, Dict, List
from uuid import UUID

from src.abstract import abstract_model


def serialize_value(value: Any) -> Any:
    """Рекурсивно сериализует значение в JSON-совместимый формат"""
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, abstract_model):
        return serialize_model(value)
    if isinstance(value, list):
        return [serialize_value(item) for item in value]
    if isinstance(value, dict):
        return {str(k): serialize_value(v) for k, v in value.items()}
    return str(value)


def serialize_model(model: abstract_model) -> Dict[str, Any]:
    """
    Сериализует модель в словарь, извлекая все публичные properties.
    """
    if not isinstance(model, abstract_model):
        return {"value": serialize_value(model)}

    result = {}

    # Извлекаем все properties из класса
    for attr_name in dir(model.__class__):
        if attr_name.startswith('_'):
            continue

        attr = getattr(model.__class__, attr_name, None)
        if isinstance(attr, property):
            try:
                value = getattr(model, attr_name)
                result[attr_name] = serialize_value(value)
            except Exception:
                continue

    return result


def serialize_models(models: List[abstract_model]) -> List[Dict[str, Any]]:
    """Сериализует список моделей"""
    return [serialize_model(m) for m in models]

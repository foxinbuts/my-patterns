from datetime import datetime
from typing import Any, Dict, List

from flask import Flask, jsonify, request

from src.Core.warehouse_operation_manager import warehouse_operation_manager
from src.Logics.osv_service import osv_service
from src.api.model_registry import ModelRegistry
from src.api.serializers import serialize_model, serialize_models
from src.filtering import FilterDTO, FilterPrototype, FilterType
from src.models.nomenclature_model import nomenclature_model
from src.models.warehouse_model import warehouse_model
from src.models.warehouse_operation_model import warehouse_operation_model


app = Flask(__name__)


def parse_filter_dto(data: Dict[str, Any]) -> FilterDTO:
    """
    Парсит DTO фильтрации из JSON.
    Ожидает формат:
    {
        "conditions": [
            {"field_name": "name", "filter_type": "LIKE", "value": "мяс"},
            {"field_name": "group.name", "filter_type": "EQUALS", "value": "Мясо"}
        ]
    }
    """
    dto = FilterDTO()

    conditions = data.get("conditions", [])
    if not isinstance(conditions, list):
        raise ValueError("conditions должен быть списком")

    for cond in conditions:
        field_name = cond.get("field_name")
        filter_type_str = cond.get("filter_type")
        value = cond.get("value")

        if not field_name or not filter_type_str:
            raise ValueError("Каждое условие должно содержать field_name и filter_type")

        try:
            filter_type = FilterType(filter_type_str)
        except ValueError:
            raise ValueError(
                f"Неизвестный тип фильтра: {filter_type_str}. "
                f"Доступные: {[ft.value for ft in FilterType]}"
            )

        dto.add_condition(field_name, filter_type, value)

    return dto


# ============================================================
# Пункт 5: POST /api/filter/<model_type>
# Фильтрация DOMAIN моделей
# ============================================================
@app.route("/api/filter/<model_type>", methods=["POST"])
def filter_models(model_type: str):
    """
    Фильтрует DOMAIN модели по заданным условиям.

    Body:
    {
        "conditions": [
            {"field_name": "name", "filter_type": "LIKE", "value": "мяс"}
        ]
    }
    """
    try:
        # Проверяем, что тип модели существует
        ModelRegistry.get_model_class(model_type)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # Парсим DTO из запроса
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Тело запроса должно быть JSON"}), 400
        filter_dto = parse_filter_dto(data)
    except ValueError as e:
        return jsonify({"error": f"Ошибка в DTO: {str(e)}"}), 400

    # Получаем данные для модели
    data_store = ModelRegistry.get_data_store(model_type)

    # Применяем фильтр через Прототип
    prototype = FilterPrototype()
    for condition in filter_dto.conditions:
        prototype.add_condition(
            condition.field_name,
            condition.filter_type,
            condition.value,
        )

    filtered_data = prototype.apply(data_store)

    return jsonify({
        "model_type": model_type,
        "total_count": len(data_store),
        "filtered_count": len(filtered_data),
        "items": serialize_models(filtered_data),
    })


# ============================================================
# Пункт 6: POST /api/osv
# Формирование ОСВ с учетом фильтрации
# ============================================================
@app.route("/api/osv", methods=["POST"])
def get_osv():
    """
    Формирует оборотно-сальдовую ведомость с учетом фильтрации.

    Body:
    {
        "period_start": "2024-01-01T00:00:00",
        "period_end": "2024-01-31T23:59:59",
        "filter": {
            "conditions": [
                {"field_name": "nomenclature.name", "filter_type": "LIKE", "value": "Мука"},
                {"field_name": "warehouse.name", "filter_type": "EQUALS", "value": "Склад №1"}
            ]
        }
    }
    """
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Тело запроса должно быть JSON"}), 400

        # Парсим период
        period_start_str = data.get("period_start")
        period_end_str = data.get("period_end")

        if not period_start_str or not period_end_str:
            return jsonify({"error": "Необходимо указать period_start и period_end"}), 400

        try:
            period_start = datetime.fromisoformat(period_start_str)
            period_end = datetime.fromisoformat(period_end_str)
        except ValueError:
            return jsonify({"error": "Неверный формат даты. Используйте ISO формат"}), 400

        # Получаем операции (в реальном приложении - из менеджера)
        operations = ModelRegistry.get_data_store("warehouse_operation")

        # Применяем фильтр к операциям через Прототип
        filter_data = data.get("filter", {})
        filter_dto = parse_filter_dto(filter_data)

        prototype = FilterPrototype()
        for condition in filter_dto.conditions:
            prototype.add_condition(
                condition.field_name,
                condition.filter_type,
                condition.value,
            )

        # Фильтруем операции
        filtered_operations = prototype.apply(operations)

        # Формируем ОСВ через сервис
        service = osv_service(filtered_operations)
        report = service.generate_report(period_start, period_end)

        # Сериализуем результат
        items_data = []
        for item in report.items:
            items_data.append({
                "warehouse": serialize_model(item.warehouse),
                "nomenclature": serialize_model(item.nomenclature),
                "opening_balance": item.opening_balance,
                "deposit_turnover": item.deposit_turnover,
                "withdraw_turnover": item.withdraw_turnover,
                "closing_balance": item.closing_balance,
            })

        return jsonify({
            "period_start": report.period_start,
            "period_end": report.period_end,
            "total_opening_balance": report.get_total_opening_balance(),
            "total_deposit_turnover": report.get_total_deposit_turnover(),
            "total_withdraw_turnover": report.get_total_withdraw_turnover(),
            "total_closing_balance": report.get_total_closing_balance(),
            "items_count": len(items_data),
            "items": items_data,
        })

    except Exception as e:
        return jsonify({"error": f"Внутренняя ошибка: {str(e)}"}), 500


# ============================================================
# Вспомогательные endpoints для тестирования
# ============================================================
@app.route("/api/models", methods=["GET"])
def list_models():
    """Возвращает список доступных типов моделей"""
    return jsonify({
        "available_types": ModelRegistry.get_available_types()
    })


@app.route("/api/seed", methods=["POST"])
def seed_data():
    """
    Заполняет хранилища тестовыми данными.
    Используется для демонстрации работы API.
    """
    from src.models.group_model import group_model
    from src.models.range_model import range_model

    # Очищаем хранилища
    for model_type in ModelRegistry.get_available_types():
        ModelRegistry.set_data_store(model_type, [])

    # Создаем тестовые данные
    kg = range_model("кг", coefficient=1.0)
    g = range_model("г", coefficient=0.001, base=kg)

    meat_group = group_model("Мясо")
    meat_group.code = "GRP-001"
    veg_group = group_model("Овощи")
    veg_group.code = "GRP-002"

    beef = nomenclature_model("Говядина", "Говядина охлажденная", meat_group, kg)
    beef.code = "NOM-001"
    pork = nomenclature_model("Свинина", "Свинина охлажденная", meat_group, kg)
    pork.code = "NOM-002"
    potato = nomenclature_model("Картофель", "Картофель свежий", veg_group, kg)
    potato.code = "NOM-003"

    # Заполняем хранилища
    ModelRegistry.set_data_store("group", [meat_group, veg_group])
    ModelRegistry.set_data_store("range", [kg, g])
    ModelRegistry.set_data_store("nomenclature", [beef, pork, potato])

    return jsonify({
        "message": "Тестовые данные загружены",
        "counts": {
            "group": 2,
            "range": 2,
            "nomenclature": 3,
        }
    })


def create_app() -> Flask:
    """Фабрика приложения"""
    return app


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

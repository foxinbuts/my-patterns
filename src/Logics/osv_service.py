from datetime import datetime
from typing import Dict, List, Tuple

from src.exceptions import TypeException, ValueException
from src.filtering import FilterPrototype, FilterType
from src.models.nomenclature_model import nomenclature_model
from src.models.osv_report_model import osv_report, osv_report_item
from src.models.warehouse_model import warehouse_model
from src.models.warehouse_operation_model import (
    OperationType,
    warehouse_operation_model,
)


class osv_service:
    """
    Сервис для формирования оборотно-сальдовой ведомости (ОСВ).
    Использует паттерн Прототип для фильтрации складских операций.

    Алгоритм:
    1. Получить исходные данные из менеджера
    2. Наложить фильтр по дате начала <= (для начальных остатков)
    3. Рассчитать начальные остатки
    4. Опять взять исходные данные и наложить фильтр по датам (ОТ и ДО)
    5. Рассчитать обороты (приход/расход)
    6. Объединить записи и рассчитать конечные остатки
    """

    def __init__(self, operations: List[warehouse_operation_model]):
        if not isinstance(operations, list):
            raise TypeException("operations", "list", type(operations).__name__)

        for op in operations:
            if not isinstance(op, warehouse_operation_model):
                raise TypeException("operation", "warehouse_operation_model", type(op).__name__)

        self.__operations = operations

    def generate_report(
        self,
        period_start: datetime,
        period_end: datetime,
    ) -> osv_report:
        """
        Формирует оборотно-сальдовую ведомость за период.

        :param period_start: начало периода
        :param period_end: конец периода
        :return: оборотно-сальдовая ведомость
        """
        if not isinstance(period_start, datetime):
            raise TypeException("period_start", "datetime", type(period_start).__name__)
        if not isinstance(period_end, datetime):
            raise TypeException("period_end", "datetime", type(period_end).__name__)
        if period_start > period_end:
            raise ValueException("period", "начало периода должно быть <= конца периода")

        # Шаг 1: Рассчитываем начальные остатки (операции до начала периода)
        opening_balances = self._calculate_opening_balances(period_start)

        # Шаг 2: Рассчитываем обороты за период
        turnovers = self._calculate_turnovers(period_start, period_end)

        # Шаг 3: Объединяем результаты и рассчитываем конечные остатки
        report_items = self._build_report_items(opening_balances, turnovers)

        return osv_report(
            items=report_items,
            period_start=period_start.strftime("%Y-%m-%d"),
            period_end=period_end.strftime("%Y-%m-%d"),
        )

    def _calculate_opening_balances(
        self,
        period_start: datetime,
    ) -> Dict[Tuple[object, object], float]:
        """
        Рассчитывает начальные остатки на начало периода.
        Использует прототип фильтрации для отбора операций до начала периода.
        """
        # Создаем прототип фильтра: операции с датой < period_start
        filter_proto = FilterPrototype()
        filter_proto.add_condition("date", FilterType.LESS_THAN, period_start)

        # Применяем фильтр
        filtered_operations = filter_proto.apply(self.__operations)

        # Рассчитываем остатки
        balances: Dict[Tuple[object, object], float] = {}
        for op in filtered_operations:
            key = (op.warehouse.id, op.nomenclature.id)
            if op.is_deposit():
                balances[key] = balances.get(key, 0.0) + op.quantity
            elif op.is_withdraw():
                balances[key] = balances.get(key, 0.0) - op.quantity

        return balances

    def _calculate_turnovers(
        self,
        period_start: datetime,
        period_end: datetime,
    ) -> Dict[Tuple[object, object], Dict[str, float]]:
        """
        Рассчитывает обороты за период.
        Использует прототип фильтрации для отбора операций в диапазоне дат.
        """
        # Создаем прототип фильтра: операции с датой >= period_start И <= period_end
        filter_proto = FilterPrototype()
        filter_proto.add_condition("date", FilterType.GREATER_OR_EQUAL, period_start)
        filter_proto.add_condition("date", FilterType.LESS_OR_EQUAL, period_end)

        # Применяем фильтр
        filtered_operations = filter_proto.apply(self.__operations)

        # Рассчитываем обороты
        turnovers: Dict[Tuple[object, object], Dict[str, float]] = {}
        for op in filtered_operations:
            key = (op.warehouse.id, op.nomenclature.id)
            if key not in turnovers:
                turnovers[key] = {"deposit": 0.0, "withdraw": 0.0}

            if op.is_deposit():
                turnovers[key]["deposit"] += op.quantity
            elif op.is_withdraw():
                turnovers[key]["withdraw"] += op.quantity

        return turnovers

    def _build_report_items(
        self,
        opening_balances: Dict[Tuple[object, object], float],
        turnovers: Dict[Tuple[object, object], Dict[str, float]],
    ) -> List[osv_report_item]:
        """
        Объединяет начальные остатки и обороты в строки ОСВ.
        """
        # Собираем все уникальные ключи (склад + номенклатура)
        all_keys = set(opening_balances.keys()) | set(turnovers.keys())

        # Создаем словари для быстрого доступа к объектам
        warehouse_map = {op.warehouse.id: op.warehouse for op in self.__operations}
        nomenclature_map = {op.nomenclature.id: op.nomenclature for op in self.__operations}

        report_items = []
        for key in all_keys:
            warehouse_id, nomenclature_id = key
            warehouse = warehouse_map.get(warehouse_id)
            nomenclature = nomenclature_map.get(nomenclature_id)

            if warehouse is None or nomenclature is None:
                continue

            opening_balance = opening_balances.get(key, 0.0)
            turnover_data = turnovers.get(key, {"deposit": 0.0, "withdraw": 0.0})

            item = osv_report_item(
                warehouse=warehouse,
                nomenclature=nomenclature,
                opening_balance=opening_balance,
                deposit_turnover=turnover_data["deposit"],
                withdraw_turnover=turnover_data["withdraw"],
            )
            item.calculate_closing_balance()
            report_items.append(item)

        return report_items

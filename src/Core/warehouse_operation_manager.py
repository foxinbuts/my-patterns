import json
import os
from datetime import datetime
from typing import List

from src.Core.abstract_manager import abstract_manager
from src.exceptions import TypeException, ValueException
from src.models.nomenclature_model import nomenclature_model
from src.models.warehouse_model import warehouse_model
from src.models.warehouse_operation_model import OperationType, warehouse_operation_model


class warehouse_operation_manager(abstract_manager):
    """
    Менеджер для загрузки складских операций из JSON-файла.
    """

    DEFAULT_FILE = "warehouse_operations.json"

    def __init__(self, warehouses: List[warehouse_model], nomenclatures: List[nomenclature_model]):
        super().__init__()

        if not isinstance(warehouses, list):
            raise TypeException("warehouses", "list", type(warehouses).__name__)
        if not isinstance(nomenclatures, list):
            raise TypeException("nomenclatures", "list", type(nomenclatures).__name__)

        self.__warehouses = {w.id: w for w in warehouses}
        self.__nomenclatures = {n.id: n for n in nomenclatures}
        self.file_name = self.DEFAULT_FILE

    def load(self, file_name: str = "") -> None:
        """Загрузить операции из JSON-файла"""
        if file_name:
            self.file_name = file_name

        if not self.file_name:
            raise ValueError("Не задан путь к файлу операций")

        if not os.path.isfile(self.file_name):
            raise FileNotFoundError(f"Файл операций не найден: {self.file_name}")

        with open(self.file_name, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        if not isinstance(raw_data, list):
            raise ValueException("data", "list", type(raw_data).__name__)

        self.data = raw_data
        self.is_loaded = True

    def convert(self) -> bool:
        """Преобразовать загруженные данные в список warehouse_operation_model"""
        if not self.is_loaded:
            return False

        try:
            operations = []
            for item in self.data:
                operation = self._convert_operation(item)
                operations.append(operation)

            self.data = operations
            return True
        except Exception as e:
            print(f"Ошибка конвертации: {e}")
            return False

    def _convert_operation(self, item: dict) -> warehouse_operation_model:
        """Конвертирует одну операцию из словаря"""
        if not isinstance(item, dict):
            raise TypeException("item", "dict", type(item).__name__)

        # Извлекаем обязательные поля
        operation_type_str = item.get("operation_type")
        if operation_type_str not in ["DEPOSIT", "WITHDRAW"]:
            raise ValueException("operation_type", "DEPOSIT or WITHDRAW", operation_type_str)

        operation_type = OperationType.DEPOSIT if operation_type_str == "DEPOSIT" else OperationType.WITHDRAW

        quantity = item.get("quantity")
        if not isinstance(quantity, (int, float)):
            raise TypeException("quantity", "int | float", type(quantity).__name__)

        warehouse_id = item.get("warehouse_id")
        if warehouse_id not in self.__warehouses:
            raise ValueException("warehouse_id", "valid warehouse ID", warehouse_id)
        warehouse = self.__warehouses[warehouse_id]

        nomenclature_id = item.get("nomenclature_id")
        if nomenclature_id not in self.__nomenclatures:
            raise ValueException("nomenclature_id", "valid nomenclature ID", nomenclature_id)
        nomenclature = self.__nomenclatures[nomenclature_id]

        # Парсим дату
        date_str = item.get("date")
        if date_str:
            date = datetime.fromisoformat(date_str)
        else:
            date = datetime.now()

        description = item.get("description", "")

        return warehouse_operation_model(
            operation_type=operation_type,
            quantity=quantity,
            warehouse=warehouse,
            nomenclature=nomenclature,
            date=date,
            description=description,
        )

    def get_operations(self) -> List[warehouse_operation_model]:
        """Возвращает список операций после конвертации"""
        if not self.is_loaded:
            return []
        return [op for op in self.data if isinstance(op, warehouse_operation_model)]

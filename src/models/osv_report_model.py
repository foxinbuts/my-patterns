from dataclasses import dataclass
from typing import List

from src.models.nomenclature_model import nomenclature_model
from src.models.warehouse_model import warehouse_model


@dataclass
class osv_report_item:
    """
    Строка оборотно-сальдовой ведомости.
    Содержит начальный остаток, обороты и конечный остаток для пары (склад, номенклатура).
    """
    warehouse: warehouse_model
    nomenclature: nomenclature_model
    opening_balance: float = 0.0      # Начальный остаток
    deposit_turnover: float = 0.0     # Оборот по дебету (приход)
    withdraw_turnover: float = 0.0    # Оборот по кредиту (расход)
    closing_balance: float = 0.0      # Конечный остаток

    def calculate_closing_balance(self) -> None:
        """Рассчитывает конечный остаток"""
        self.closing_balance = (
            self.opening_balance
            + self.deposit_turnover
            - self.withdraw_turnover
        )

    def __str__(self):
        return (
            f"OSV(warehouse={self.warehouse.name!r}, "
            f"nomenclature={self.nomenclature.name!r}, "
            f"opening={self.opening_balance:.2f}, "
            f"deposit={self.deposit_turnover:.2f}, "
            f"withdraw={self.withdraw_turnover:.2f}, "
            f"closing={self.closing_balance:.2f})"
        )


@dataclass
class osv_report:
    """
    Оборотно-сальдовая ведомость.
    Содержит список строк с остатками и оборотами.
    """
    items: List[osv_report_item]
    period_start: str
    period_end: str

    def get_total_opening_balance(self) -> float:
        """Сумма начальных остатков"""
        return sum(item.opening_balance for item in self.items)

    def get_total_deposit_turnover(self) -> float:
        """Сумма оборотов по приходу"""
        return sum(item.deposit_turnover for item in self.items)

    def get_total_withdraw_turnover(self) -> float:
        """Сумма оборотов по расходу"""
        return sum(item.withdraw_turnover for item in self.items)

    def get_total_closing_balance(self) -> float:
        """Сумма конечных остатков"""
        return sum(item.closing_balance for item in self.items)

    def __str__(self):
        return (
            f"OSV Report (period: {self.period_start} - {self.period_end})\n"
            f"Items: {len(self.items)}\n"
            f"Total opening: {self.get_total_opening_balance():.2f}\n"
            f"Total deposit: {self.get_total_deposit_turnover():.2f}\n"
            f"Total withdraw: {self.get_total_withdraw_turnover():.2f}\n"
            f"Total closing: {self.get_total_closing_balance():.2f}"
        )

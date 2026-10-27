from Src.Core.report_result_model import report_result_model
from abc import ABC, abstractmethod
from Src.Core.abstract_model import abstact_model

"""
Абстрактный класс для формирования отчета
"""

class abstract_report(ABC):
    """
    Сформировать отчет
    """

    @abstractmethod
    def build(self, source: abstact_model) -> report_result_model:
        pass


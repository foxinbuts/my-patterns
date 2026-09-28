from src.abstract import abstract_model
from src.exceptions import ArgumentException, TypeException, ValueException, LengthException

class range_model(abstract_model):

	MAX_NAME_LENGTH = 50

	def __init__(
		self,
		name: str,
		coefficient: float | int = 1,
		base: "range_model | None" = None,
	):

		super().__init__()

		if not isinstance(name, str):
			raise TypeException("name", "str", type(name).__name__)
		if not name or not name.strip():
			raise ValueException("name", "наименование не может быть пустым")
		if len(name) > self.MAX_NAME_LENGTH:
			raise LengthException("name", self.MAX_NAME_LENGTH, len(name))
		self.name = name.strip()

		if not isinstance(coefficient, (int, float)):
			raise TypeException("coefficient", "int | float", type(base).__name__)
		if coefficient <= 0:
			raise ValueException("coefficient", "коеффициент не может быть > 0")
		self.__coefficient = float(coefficient)

		if base is not None and not isinstance(base, range_model):
			raise TypeException("base", "range_model | None", type(base).__name__)
		self.__base = base

	@property
	def coefficient(self) -> float:
		return self.__coefficient

	@coefficient.setter
	def coefficient(self, value: float | int):
		if not isinstance(value, (int, float)):
			raise TypeException("coefficient", "int | float", type(value).__name__)
		if value <= 0:
			raise ValueException("coefficient", "коеффициент должен быть > 0")
		self.__coefficient = float(value)

	@property
	def base(self) -> "range_model | None":
		return self.__base

	@base.setter
	def base(self, value: "range_model | None"):
		if value is not None and not isinstance(value, range_model):
			raise TypeException("base", "range_model | None", type(value).__name__)
		self.__base = value

	def convert_to_base(self, amount: float | int) -> float:
		if not isinstance(amount, (int, float)):
			raise TypeException("amount", "int | float", type(amount).__name__)
		if self.__base is None:
			return float(amount) * self.__coefficient
		return float(amount) * self.__coefficient * self.__base.convert_to_base(1)

	def __str__(self):
		base_name = self.__base.name if self.__base else "None"
		return (
			f"range_model(name={self.name!r}, coefficient={self.__coefficient}, "
			f"base={base_name})"
		)

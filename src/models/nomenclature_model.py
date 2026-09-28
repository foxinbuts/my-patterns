from src.abstract import abstract_model
from src.models.group_model import group_model
from src.models.range_model import range_model
from src.exceptions import TypeException, ValueException, LengthException

class nomenclature_model(abstract_model):
	MAX_NAME_LENGTH = 50
	MAX_FULL_NAME_LENGTH = 255

	def __init__(
		self,
		name: str,
		full_name: str,
		group: group_model,
		range_unit: range_model,
	):

		super().__init__()
		if not isinstance(name, str):
			raise TypeException("name", "str", type(name).__name__)
		if not name or not name.strip():
			raise ValueException("name", "наименование не может быть пустым")
		if len(name) > self.MAX_NAME_LENGTH:
			raise LengthException("name", self.MAX_NAME_LENGTH, len(name))
		self.name = name.strip()

		if not isinstance(full_name, str):
			raise TypeException("full_name", "str", type(full_name).__name__)
		if not full_name or not full_name.strip():
			raise ValueException("full_name", "полное наименование не может быть пустым")
		if len(full_name) > self.MAX_FULL_NAME_LENGTH:
			raise LengthException("full_name", self.MAX_FULL_NAME_LENGTH, len(full_name))
		self.__full_name = full_name.strip()

		if not isinstance(group, group_model):
			raise TypeException("group", "group_model", type(group).__name__)
		self.__group = group

		if not isinstance(range_unit, range_model):
			raise TypeException("range_unit", "range_model", type(range_unit).__name__)
		self.__range_unit = range_unit

	@property
	def full_name(self) -> str:
		return self.__full_name

	@full_name.setter
	def full_name(self, value: str):
		if not isinstance(value, str):
			raise TypeException("full_name", "str", type(value).__name__)
		if not value or not value.strip():
			raise ValueException("full_name", "полное наименование не может быть пустым")
		if len(value) > self.MAX_FULL_NAME_LENGTH:
			raise LengthException("full_name", self.MAX_FULL_NAME_LENGTH, len(value))
		self.__full_name = value.strip()

	@property
	def group(self) -> group_model:
		return self.__group

	@group.setter
	def group(self, value: group_model):
		if not isinstance(value, group_model):
			raise TypeException("group", "group_model", type(value).__name__)
		self.__group = value

	@property
	def range_unit(self) -> range_model:
		return self.__range_unit

	@range_unit.setter
	def range_unit(self, value: range_model):
		if not isinstance(value, range_model):
			raise TypeException("range_unit", "range_model", type(value).__name__)
		self.__range_unit = value

	def __str__(self):
		return (
			f"nomenclature_model(name={self.name!r}, full_name={self.__full_name!r}, "
			f"group={self.__group.name!r}, unit={self.__range_unit.name!r})"
		)

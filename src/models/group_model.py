from src.abstract import abstract_model
from src.exceptions import TypeException, ValueException, LengthException

class group_model(abstract_model):

	MAX_NAME_LENGTH = 50

	def __init__(self, name: str):
		super().__init__()

		if not isinstance(name, str):
			raise TypeException("name", "str", type(name).__name__)
		if not name or not name.strip():
			raise ValueException("name", "наименование группы не может быть пустым")
		if len(name) > self.MAX_NAME_LENGTH:
			raise LengthException("name", self.MAX_NAME_LENGTH, len(name))

		self.name = name.strip()

	def __str__(self):
		return f"group_model(id={self.id}, name={self.name!r})"

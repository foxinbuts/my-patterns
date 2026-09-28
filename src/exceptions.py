class AbstractException(Exception):
	def __init__(self, message: str = ""):
		self.message = message
		super().__init__(self.message)

class ArgumentException(AbstractException):
	def __init__(self, message: str = "Некорректный аргумент"):
		super().__init__(message)

class LengthException(ArgumentException):
	def __init__(self, field_name: str, max_length: int, actual_length: int = None):
		msg = f"Поле '{field_name}' превышает максимальную длину {max_length}"
		if actual_length is not None:
			msg += f"(получено: {actual_length})"
		super().__init__(msg)

class TypeException(ArgumentException):
	def __init__(self, field_name: str, expected_type: str, actual_type: str = None):
		msg = f"Поле {field_name} должно иметь тип {expected_type}"
		if actual_type is not None:
			msg += f"(получено: {actual_type})"
		super().__init__(msg)

class ValueException(ArgumentException):
	def __init__(self, field_name: str, message: str = ""):
		msg = f"Недопустимое значение поля '{field_name}'"
		if message:
			msg += f": {message}"
		super().__init__(msg)

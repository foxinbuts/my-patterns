from src.abstract import abstract_model
from src.exceptions import TypeException, ValueException, LengthException

class organization_model(abstract_model):
	MAX_NAME_LENGTH = 50
	INN_LENGTHS = (10, 12)
	BIK_LENGTH = 9
	ACCOUNT_LENGTH = 20

	def __init__(
		self,
		name: str,
		inn: str,
		bik: str,
		account: str,
		ownership_form: str,
	):
		super().__init__()

		if not isinstance(name, str):
			raise TypeException("name", "str", type(name).__name__)
		if not name or not name.strip():
			raise ValueException("name", "наименование не может быть пустым")
		if len(name) > self.MAX_NAME_LENGTH:
			raise LengthException("name", self.MAX_NAME_LENGTH, len(name))
		self.name = name.strip()

		if not isinstance(inn, str):
			raise TypeException("inn", "str", type(inn).__name__)
		inn_clean = inn.strip()
		if not inn_clean.isdigit():
			raise ValueException("inn", "ИНН должен содержать только цифры")
		if len(inn_clean) not in self.INN_LENGTHS:
			raise ValueException(
				"inn",
				f"ИНН должен иметь длину {self.INN_LENGTHS[0]} или {self.INN_LENGTHS[1]} цифр",
			)
		self.__inn = inn_clean

		if not isinstance(bik, str):
			raise TypeException("bik", "str", type(bik).__name__)
		bik_clean = bik.strip()
		if not bik_clean.isdigit() or len(bik_clean) != self.BIK_LENGTH:
			raise ValueException("bik", f"БИК должен состоять из {self.BIK_LENGTH} цифр")
		self.__bik = bik_clean

		if not isinstance(account, str):
			raise TypeException("account", "str", type(account).__name__)
		account_clean = account.strip()
		if not account_clean.isdigit() or len(account_clean) != self.ACCOUNT_LENGTH:
			raise ValueException(
				"account",
				f"Расчетный счет должен состоять из {self.ACCOUNT_LENGTH} цифр",
			)
		self.__account = account_clean

		if not isinstance(ownership_form, str):
			raise TypeException("ownership_form", "str", type(ownership_form).__name__)
		if not ownership_form or not ownership_form.strip():
			raise ValueException("ownership_form", "форма собственности не может быть пустой")
		self.__ownership_form = ownership_form.strip()

	@property
	def inn(self) -> str:
		return self.__inn

	@inn.setter
	def inn(self, value: str):
		if not isinstance(value, str):
			raise TypeException("inn", "str", type(value).__name__)
		clean = value.strip()
		if not clean.isdigit() or len(clean) not in self.INN_LENGTHS:
			raise ValueException(
				"inn",
				f"ИНН должен иметь длину {self.INN_LENGTHS[0]} или {self.INN_LENGTHS[1]} цифр",
			)
		self.__inn = clean

	@property
	def bik(self) -> str:
		return self.__bik

	@bik.setter
	def bik(self, value: str):
		if not isinstance(value, str):
			raise TypeException("bik", "str", type(value).__name__)
		clean = value.strip()
		if not clean.isdigit() or len(clean) != self.BIK_LENGTH:
			raise ValueException("bik", f"БИК должен состоять из {self.BIK_LENGTH} цифр")
		self.__bik = clean

	@property
	def account(self) -> str:
		return self.__account

	@account.setter
	def account(self, value: str):
		if not isinstance(value, str):
			raise TypeException("account", "str", type(value).__name__)
		clean = value.strip()
		if not clean.isdigit() or len(clean) != self.ACCOUNT_LENGTH:
			raise ValueException(
				"account",
				f"Расчетный счет должен состоять из {self.ACCOUNT_LENGTH} цифр",
			)
		self.__account = clean

	@property
	def ownership_form(self) -> str:
		return self.__ownership_form

	@ownership_form.setter
	def ownership_form(self, value: str):
		if not isinstance(value, str):
			raise TypeException("ownership_form", "str", type(value).__name__)
		if not value or not value.strip():
			raise ValueException("ownership_form", "форма собственности не может быть пустой")
		self.__ownership_form = value.strip()

	def __str__(self):
		return (
			f"organization_model(name={self.name!r}, inn={self.__inn}, "
			f"bik={self.__bik}, account={self.__account}, "
			f"ownership_form={self.__ownership_form!r}) "
		)

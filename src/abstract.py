from abc import ABC, abstractmethod
from uuid 
class Dish(ABC):
	def __init__(self):
		self.__name = " " # "__" -> это приват
		self.__id = uuid.uuid4()

	@property
	def name(self):
		return self._name
	
	@name.setter
	def name(self, value):
		self._name = value

	@property
	def id(self):
		return self._id

	@id.setter
	def id(self,value):
		self._id = value

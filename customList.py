class customList(list):
	def __init__(self, *args):
		super().__init__(args)
		self.pointer = 0

	@property
	def current(self):
		if self.pointer <= len(self) -1:
			return self[self.pointer]
		return None

	@current.setter
	def current(self, value):
		raise TypeError("このプロパティーには内容を指定できません。")

	def setNext(self):
		self.pointer += 1
		if self.current == None:
			return False
		return True

	def setprevious(self):
		self.pointer -= 1
		if self.current == None:
			return False
		return True

	def set(self, pointer):
		self.pointer = pointer
		if self.current == None:
			return False
		return True


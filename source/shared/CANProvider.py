from .CANService import CANService
from .CANService import MockCANService

class CANProvider: 
	_shared = None

	@classmethod
	def shared(cls, mocked=False):
		if cls._shared is None: 
			cls._shared = cls(mocked)
		return cls._shared

	def __init__(self, mocked):
		if mocked:
			self.can_service = MockCANService()
		else: 
			self.can_service = CANService()

	def subscribe_to_pid(self, pid):
		return self.can_service.subscribe_to_pid(pid)

	def shutdown(self):
		self.can_service.shutdown()

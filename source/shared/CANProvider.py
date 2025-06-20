from .CANService import CANService
# from .CANService import MockCANService

class CANProvider: 
	_shared = None

	@classmethod
	def shared(cls):
		if cls._shared is None: 
			cls._shared = cls()
		return cls._shared

	def __init__(self):
		self.can_service = CANService()
		# self.can_service = MockCANService()

	def subscribe_to_pid(self, pid):
		return self.can_service.subscribe_to_pid(pid)

	def shutdown(self):
		self.can_service.shutdown()

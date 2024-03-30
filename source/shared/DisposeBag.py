class DisposeBag: 
	_shared = None

	@classmethod
	def shared(cls):
		if cls._shared is None:
			cls._shared = cls()
		return cls._shared

	def __init__(self):
		self.subscriptions = []
		import atexit
		atexit.register(self.dispose)

	def add(self, subscription):
		self.subscriptions.append(subscription)

	def dispose(self):
		print("Cleaning up subscriptions")
		for subscription in self.subscriptions:
			subscription.dispose()
		self.subscriptions.clear()
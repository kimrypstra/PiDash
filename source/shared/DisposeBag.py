from threading import Thread

class DisposeBag: 
	_shared = None

	@classmethod
	def shared(cls):
		if cls._shared is None:
			cls._shared = cls()
		return cls._shared

	def __init__(self):
		self.subscriptions = []

	def add(self, subscription):
		self.subscriptions.append(subscription)

	def dispose(self):
		print("Cleaning up subscriptions")

		# Run disposal on background thread so Kivy can do it's thing on main thread
		def cleanup(*kwargs):
			for subscription in self.subscriptions:
				subscription.dispose()
			self.subscriptions.clear()

		Thread(target=cleanup).start()

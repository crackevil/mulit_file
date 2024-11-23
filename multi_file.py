
from io import RawIOBase
import logging


class MultiFilesWriter(RawIOBase):

	def __init__(self, fd, *fds):
		self.__files__ = [fd] + list(fds)
		assert self.writable()
		self.logger = logging.getLogger()

	def close(self):
		self.__files__ = []

	@property
	def closed(self):
		return not self.__files__

	def flush(self):
		for f in self.__files__:
			try:
				f.flush()
			except Exception as e:
				self.logger.exception(e)

	def isatty(self):
		return False

	def readable(self):
		return False

	def seekable(self):
		return False

	def writable(self):
		for t in self.__files__:
			if not t.writable():
				return False
		return True

	def read(self, *args, **kwargs):
		self._checkReadable()

	def write(self, b):
		for f in self.__files__:
			try:
				f.write(b)
			except Exception as e:
				self.logger.exception(e)


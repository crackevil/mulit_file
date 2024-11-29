
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

from threading import Thread, Event
from queue import Queue, Empty
import six

class MultiFilesWriter2(MultiFilesWriter):

	def __init__(self, fd, *fds):
		super(MultiFilesWriter2, self).__init__(fd, *fds)

		# (cmd, args, kwargs) in queue
		self.tasks = {f:Queue() for f in self.__files__}
		self.thread_stop_event = Event()
		self.thread_stop_event.clear()

		self.executors = [Thread(target=self.thread_func, args=(f, 0.01), ) for f in self.__files__]
		for t in self.executors:
			t.start()

	def thread_func(self, f, timeout):
		q = self.tasks[f]
		while not self.thread_stop_event.is_set():
			try:
				func, args, kwargs = q.get(block=False, timeout=timeout)
				try:
					func(*args, **kwargs)
				except Exception as e:
					self.logger.exception(e)
				q.task_done()
			except Empty:
				pass

	def close(self):
		for q in six.itervalues(self.tasks):
			q.join()
		self.tasks = {}
		self.thread_stop_event.set()
		for t in self.executors:
			t.join()
		self.executors = []
		super(MultiFilesWriter2, self).close()

	def flush(self):
		for f in self.__files__:
			self.tasks[f].put((f.flush, (), {}))

	def write(self, b):
		for f in self.__files__:
			self.tasks[f].put((f.write, (b, ), {}))


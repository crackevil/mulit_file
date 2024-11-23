
import unittest
import os
import io
import tempfile
from multi_file import MultiFilesWriter


class test_multi_file(unittest.TestCase):

	def test_forbid_seek(self):
		with io.open(os.devnull, 'wb') as f1, io.open(os.devnull, 'wb') as f2:
			f = MultiFilesWriter(f1, f2)
			with self.assertRaises(io.UnsupportedOperation):
				f.seek(0)

	def test_forbid_read(self):
		with io.open(os.devnull, 'wb') as f1, io.open(os.devnull, 'wb') as f2:
			f = MultiFilesWriter(f1, f2)
			with self.assertRaises(io.UnsupportedOperation):
				f.read()

	def test_write(self):
		with tempfile.TemporaryFile() as tf1, tempfile.TemporaryFile() as tf2:
			f = MultiFilesWriter(tf1, tf2)
			b = b'515436rfegyew5e'
			f.write(b)
			tf1.seek(0)
			x = tf1.read()
			self.assertEqual(x, b)
			tf2.seek(0)
			x = tf2.read()
			self.assertEqual(x, b)

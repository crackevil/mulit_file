
import unittest
import os
import io
import tempfile
from multi_file import MultiFilesWriter, MultiFilesWriter2


class test_multi_file(unittest.TestCase):

	def setUp(self):
		try:
			self.ClassForTest
		except AttributeError:
			self.skipTest('base class')

	def test_forbid_seek(self):
		with io.open(os.devnull, 'wb') as f1, io.open(os.devnull, 'wb') as f2:
			with self.ClassForTest(f1, f2) as f:
				with self.assertRaises(io.UnsupportedOperation):
					f.seek(0)

	def test_forbid_read(self):
		with io.open(os.devnull, 'wb') as f1, io.open(os.devnull, 'wb') as f2:
			with self.ClassForTest(f1, f2) as f:
				with self.assertRaises(io.UnsupportedOperation):
					f.read()

	def test_write(self):
		b = b'515436rfegyew5e'
		with tempfile.TemporaryFile() as tf1, tempfile.TemporaryFile() as tf2:
			with self.ClassForTest(tf1, tf2) as f:
				f.write(b)
				f.flush()
			tf1.seek(0)
			x = tf1.read()
			self.assertEqual(x, b)
			tf2.seek(0)
			x = tf2.read()
			self.assertEqual(x, b)


class test_multi_file1(test_multi_file):
	ClassForTest = MultiFilesWriter


class test_multi_file2(test_multi_file):
	ClassForTest = MultiFilesWriter2

#! /usr/bin/env python3
from os import urandom as os_urandom
from random import choice as rand_choice
from string import ascii_letters
from sys import stdout as sys_stdout

from .path_manager import PathManager
from .printing import print_msg
from .exception import *


class ProgressBar:
	def __init__(self, filename, size, op_name):
		self.filename = filename
		self.size = size
		self.op_name = op_name

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		print()

	def display(self, current):
		percents = 100
		# Prévention division par 0
		if self.size != 0:
			percents = round(100.0 * current / self.size, 1)
		msg = '{:.1f}% {}'.format(percents, self.filename)
		print_msg(self.op_name, msg, end='\r')
		return percents


class BasicFileOp:
	def __init__(self, src, op_name=''):
		if not src:
			raise MissingSource()
		self.mng = PathManager()
		self.src = self.mng.normalize_path(src)
		self.op_name = op_name
		self.filename = self.mng.get_filename(self.src)
		if not self.mng.exists(self.src):
			raise FileNotFound(self.filename)
		self.info = self.mng.get_meta(self.src)
		self.size = self.info.st_size
		self.block_size = self.info.st_blksize
		self.is_dir = self.mng.is_dir(self.src)
		self.is_file = self.mng.is_file(self.src)
		self.is_writable = self.mng.is_writable(self.src)
		self.is_readable = self.mng.is_readable(self.src)

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def get_random_bytes(self, size, blank):
		if blank:
			return b'\x00' * size
		return os_urandom(size)

	def get_random_string(self, size):
		res = ''
		for i in range(size):
			res += rand_choice(ascii_letters)
		return res

	def read_bytes(self, src):
		content = b'start'
		with open(src, 'rb') as fd:
			while content:
				content = fd.read(self.block_size)
				if content:
					yield content

	def read_string(self, src):
		content = 'start'
		with open(src, 'r') as fd:
			while content:
				content = fd.read(self.block_size)
				if content:
					yield content

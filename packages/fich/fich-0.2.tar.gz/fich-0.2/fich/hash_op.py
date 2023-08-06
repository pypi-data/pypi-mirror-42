#! /usr/bin/env python3
from shutil import copystat as shutil_copystat, SameFileError
from hashlib import new as hash_new

from .file_op import BasicFileOp
from .printing import print_msg
from .exception import *


class HashOp(BasicFileOp):
	DEF_HASH_TYPE = 'sha256'
	HASH_TYPE = [
		'sha224', 
		'sha256', 
		'sha384', 
		'sha512',
		'sha3_224',
		'sha3_256',
		'sha3_512',
	]

	def __init__(self, src, hash_type):
		super().__init__(src, 'hash')
		self.hash_type = hash_type
		if not self.is_file:
			raise FileNotFound(self.name_src)
		if not self.is_readable:
			raise ReadAccessError(self.name_src)
		if not hash_type in self.HASH_TYPE:
			self.hash_type = self.DEF_HASH_TYPE

	def launch(self):
		read = 0
		hash_func = hash_new(self.hash_type)
		hash_src = ''
		try:
			if self.size > 0:
				for block in self.read_bytes(self.src):
					hash_func.update(block)
					read += len(block)
					self.print_progress(read)
			else:
				self.print_progress(0)
			hash_src = hash_func.hexdigest()
		except KeyboardInterrupt:
			raise OperationAbort(self.op_name)
		return hash_src

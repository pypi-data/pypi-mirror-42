#! /usr/bin/env python3
from hashlib import new as hash_new
from hashlib import algorithms_available

from .file_op import BasicFileOp, ProgressBar
from .printing import print_msg
from .exception import *


class HashOp(BasicFileOp):
	if 'sha256' in algorithms_available:
		DEF_HASH_TYPE = 'sha256'
	else:
		DEF_HASH_TYPE = algorithms_available[0]
	HASH_TYPE = algorithms_available

	def __init__(self, src, hash_type, digest_size):
		super().__init__(src, 'hash')
		self.hash_type = hash_type
		self.digest_size = digest_size
		if not self.is_file:
			raise FileNotFound(self.name_src)
		if not self.is_readable:
			raise ReadAccessError(self.name_src)
		if not self.hash_type in self.HASH_TYPE:
			self.hash_type = self.DEF_HASH_TYPE
		if self.digest_size <= 0:
			self.digest_size = 1

	def launch(self):
		read = 0
		hash_src = ''
		hash_func = hash_new(
			self.hash_type, 
			digest_size=self.digest_size)
		progress_bar = ProgressBar(
			self.filename, 
			self.size, 
			self.op_name)
		try:
			if self.size > 0:
				# Gestion affichage progression
				with progress_bar as pbar:
					for block in self.read_bytes(self.src):
						hash_func.update(block)
						read += len(block)
						pbar.display(read)
			else:
				print_msg(self.op_name, self.filename, end='')
			# Prise en compte cas special pour shake (voir doc python)
			if self.hash_type.startswith('shake'):
				hash_src = hash_func.hexdigest(self.digest_size)
			else:
				hash_src = hash_func.hexdigest()
		except KeyboardInterrupt:
			raise OperationAbort(self.op_name)
		return hash_src

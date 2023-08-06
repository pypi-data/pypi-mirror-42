#! /usr/bin/env python3
from .file_op import BasicFileOp
from .exception import *
from .printing import *


class DeleteOp(BasicFileOp):
	MIN_SIZE_NAME = 16

	def __init__(self, src, niter, blank, only_unlink):
		super().__init__(src, 'delete')
		self.niter = niter
		self.blank = blank
		self.only_unlink = only_unlink
		if not self.is_file:
			raise FileNotFound(self.name_src)
		if not self.is_writable:
			raise WriteAccessError(self.name_src)
		if self.niter <= 0:
			self.niter = 1

	def launch(self):
		overwritten = 0
		cursor = 0
		written = 0
		try:
			# Réecriture de données sur le fichier physique
			if not self.only_unlink and not self.size == 0:
				with open(self.src, 'wb') as fd:
					content = self.get_random_bytes(
						self.block_size, 
						self.blank)
					while cursor < self.size:
						if (self.block_size + cursor) <= self.size:
							nbytes = self.block_size
						else:
							nbytes = self.size - cursor
						for i in range(self.niter):
							fd.seek(cursor)
							written += fd.write(content[:nbytes])
						overwritten = written // self.niter
						self.print_progress(overwritten)
						cursor += nbytes
			else:
				print_msg(self.op_name, self.filename, end='')
			# Suppression du nom du fichier
			size_name = len(self.filename)
			if size_name < self.MIN_SIZE_NAME:
				size_name = self.MIN_SIZE_NAME
			new_name = self.get_random_string(size_name)
			new_path = self.mng.rename(self.src, new_name)
			# Suppression du fichier logique
			self.mng.unlink(new_path)
		except KeyboardInterrupt:
			raise OperationAbort(self.op_name)
		return overwritten

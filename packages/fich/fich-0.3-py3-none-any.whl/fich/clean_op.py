#! /usr/bin/env python3
from tempfile import NamedTemporaryFile as TempFile
from shutil import disk_usage

from .file_op import BasicFileOp, ProgressBar
from .exception import *


class CleanOp(BasicFileOp):
	def __init__(self, src, niter, blank):
		super().__init__(src, 'clean')
		self.niter = niter
		self.blank = blank
		if self.is_file:
			self.src = self.mng.get_dir(self.src)
			self.is_dir = self.mng.is_dir(self.src)
		if not self.is_dir:
			raise FileNotFound(self.filename)
		if not self.is_writable:
			raise WriteAccessError(self.filename)
		if self.niter <= 0:
			self.niter = 1
		self.size = disk_usage(self.src).free

	def launch(self):
		overwritten = 0
		cursor = 0
		written = 0
		progress_bar = ProgressBar(
			self.filename, 
			self.size, 
			self.op_name)
		try:
			if self.size:
				with TempFile(dir=self.src, mode='wb') as hole:
					content = self.get_random_bytes(
						self.block_size, 
						self.blank)
					with progress_bar as pbar:
						while cursor < self.size:
							if (self.block_size + cursor) <= self.size:
								nbytes = self.block_size
							else:
								nbytes = self.size - cursor
							for i in range(self.niter):
								hole.seek(cursor)
								written += hole.write(content[:nbytes])
							overwritten = written // self.niter
							pbar.display(overwritten)
							cursor += nbytes
		except KeyboardInterrupt:
			raise OperationAbort(self.op_name)
		return overwritten

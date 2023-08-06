#! /usr/bin/env python3
from stat import filemode as stat_filemode
from grp import getgrgid as grp_getgrgid
from pwd import getpwuid as pwd_getpwuid
from datetime import datetime

from .file_op import BasicFileOp
from .exception import *


class InfoOp(BasicFileOp):
	def __init__(self, src):
		super().__init__(src, 'info')
		if not self.is_file:
			raise FileNotFound(self.name_src)

	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def get_owner(self, uid):
		return pwd_getpwuid(uid)[0]

	def get_group(self, gid):
		return grp_getgrgid(gid)[0]

	def get_last_access(self, timestamp):
		res = ''
		now = datetime.today()
		last_access = datetime.fromtimestamp(timestamp)
		if now.date() == last_access.date():
			res = last_access.strftime('%H:%M')
		else:
			res = last_access.strftime('%d-%m-%Y %H:%M')
		return res

	def get_size_repr(self, size):
		res = ''
		if size <= 1024:
			res = '{}'.format(size)
		elif size <= 1024 ** 2:
			res = '{0:.2f} Ko'.format(size/1024)
		elif size <= 1024 ** 3:
			res = '{0:.2f} Mo'.format(size/(1024**2))
		else:
			res = '{0:.2f} Go'.format(size/(1024**3))
		return res

	def launch(self):
		info_src = ''
		try:
			buff = stat_filemode(self.info.st_mode) + ' '
			buff += '{} '.format(self.info.st_nlink)
			buff += self.get_owner(self.info.st_uid) + ' '
			buff += self.get_group(self.info.st_gid) + ' '
			buff += self.get_size_repr(self.size) + ' '
			buff += self.get_last_access(self.info.st_atime) + ' '
			buff += '{}'.format(self.info.st_ino)
			info_src = buff
		except KeyboardInterrupt:
			raise OperationAbort(self.op_name)
		return info_src

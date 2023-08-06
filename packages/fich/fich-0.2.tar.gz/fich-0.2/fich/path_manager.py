#! /usr/bin/env python3
from os.path import getsize as ospath_getsize
from os.path import islink as ospath_islink
from os.path import isfile as ospath_isfile
from os.path import isdir as ospath_isdir
from os.path import exists as ospath_exists
from os.path import abspath as ospath_abspath
from os.path import realpath as ospath_realpath
from os.path import samefile as ospath_samefile
from os.path import basename as ospath_basename
from os.path import dirname as ospath_dirname
from os.path import join as ospath_join
from os.path import normcase as ospath_normcase
from os.path import normpath as ospath_normpath
from os import unlink as os_unlink
from os import access as os_access
from os import replace as os_replace
from os import link as os_link
from os import stat as os_stat
from os import W_OK as os_WOK
from os import R_OK as os_ROK


class PathManager:
	def exists(self, src):
		return ospath_exists(src)

	def is_writable(self, src):
		return os_access(src, os_WOK)

	def is_readable(self, src):
		return os_access(src, os_ROK)

	def is_file(self, src):
		return ospath_isfile(src)

	def is_dir(self, src):
		return ospath_isdir(src)

	def is_link(self, src):
		return ospath_islink(src)

	def is_samefile(self, src, dst):
		return ospath_samefile(src, dst)

	def is_on_same_dev(self, src, dst):
		src_dev = self.get_meta(src).st_dev
		dst_dev = self.get_meta(dst).st_dev
		return src_dev == dst_dev

	def have_many_links(self, src):
		return self.get_meta(src).st_nlink > 1

	def get_size(self, src):
		return ospath_getsize(src)

	def get_dir(self, src):
		return ospath_dirname(src)

	def get_filename(self, src):
		return ospath_basename(src)

	def get_abspath(self, src):
		return ospath_abspath(src)

	def get_realpath(self, src):
		return ospath_realpath(src)

	def get_meta(self, src):
		return os_stat(src)

	def link(self, src, dst):
		return os_link(src, dst)

	def unlink(self, src):
		return os_unlink(src)

	def join(self, src, dst):
		return ospath_join(src, dst)

	def rename(self, src, new_filename):
		src_dir = self.get_dir(src)
		new_path = self.join(src_dir, new_filename)
		os_replace(src, new_path)
		return new_path

	def normalize_path(self, src):
		src = ospath_normcase(src)
		src = ospath_normpath(src)
		src = ospath_abspath(src)
		return src

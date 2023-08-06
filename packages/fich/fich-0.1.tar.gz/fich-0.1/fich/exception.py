#! /usr/bin/env python3

class OpError(Exception):
	def __init__(self, msg=''):
		super().__init__(msg)
		self.msg = msg

	def __str__(self):
		return self.msg

	def __repr__(self):
		return self.msg


class FileNotFound(OpError):
	def __init__(self, actor):
		msg = '"{}" introuvable'.format(actor)
		super().__init__(msg)


class WriteAccessError(OpError):
	def __init__(self, actor):
		msg = '"{}" n\'est pas accessible en écriture'.format(actor)
		super().__init__(msg)


class ReadAccessError(OpError):
	def __init__(self, actor):
		msg = '"{}" n\'est pas accessible en lecture'.format(actor)
		super().__init__(msg)


class MissingSource(OpError):
	def __init__(self):
		msg = 'source manquante'
		super().__init__(msg)


class OperationAbort(OpError):
	def __init__(self, actor):
		msg = 'operation "{}" annulée'.format(actor)
		super().__init__(msg)

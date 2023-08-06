#!/usr/bin/env python3
from sys import argv as sys_argv
from time import time as time_time

from . import APP_VERSION
from .printing import print_msg
from .arg_parser import get_args
from .delete_op import DeleteOp
from .hash_op import HashOp
from .info_op import InfoOp
from .clean_op import CleanOp
from .exception import *


def launch_operation(operation):
	res = None
	if operation:
		with operation as op:
			res = op.launch()
	return res


def main():
	args = get_args(sys_argv[1:])
	res = None
	op = None
	try:
		time_begin = time_time() 
		if args.action in ['delete', 'del', 'd']:
			op = DeleteOp(args.src, args.niter, args.blank, 
				args.only_unlink)
			res = launch_operation(op)
		elif args.action in ['hash', 'h']:
			op = HashOp(args.src, args.hash_type, args.digest_size)
			res = launch_operation(op)
			print_msg(op.hash_type, res)
		elif args.action in ['info', 'inf', 'i']:
			op = InfoOp(args.src)
			res = launch_operation(op)
			print_msg('=', res)
		elif args.action in ['clean', 'c']:
			op = CleanOp(args.src, args.niter, args.blank)
			res = launch_operation(op)
		else:
			print_msg('version', APP_VERSION)
		total_time = time_time() - time_begin
		if args.time:
			print_msg('temps', '{0:.3f} secondes'.format(total_time))
	except OpError as err:
		print_msg('erreur', err.msg)
	except KeyboardInterrupt:
		print_msg('erreur', 'operation annulée')
	except Exception as err:
		print_msg('erreur', str(err))
		raise err

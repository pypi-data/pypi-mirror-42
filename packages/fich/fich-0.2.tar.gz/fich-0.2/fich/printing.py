#! /usr/bin/env python3
from sys import stdout as sys_stdout


def print_msg(ctx, msg, end='\n'):
	visual = '\033[1m\033[94m[{}]\033[0m {}{}'
	sys_stdout.write(visual.format(ctx, msg, end))
	sys_stdout.flush()

#! /usr/bin/env python3
from argparse import ArgumentParser

from . import APP_NAME


def append_action(parser):
	parser.add_argument('action', 
		help='action à effectuer',
		nargs='?',
		default='version')


def append_src(parser):
	parser.add_argument('src', 
		help='fichier source',
		nargs='?', 
		default='')


def append_niter(parser):
	parser.add_argument('--niter', 
		help='nombre de réecriture sur le fichier source',
		type=int, 
		default=1)


def append_blank(parser):
	parser.add_argument('--blank', 
		help='utiliser l\'octet nul pour la réecriture',
		action='store_true')


def append_only_unlink(parser):
	parser.add_argument('--only-unlink', 
		help='supprime uniquement le fichier logique',
		action='store_true')


def append_hash_type(parser):
	parser.add_argument('--hash-type', 
		help='Type de hash à appliquer au fichier destination',
		type=str,
		default='sha256')


def append_time(parser):
	parser.add_argument('--time',
		help='afficher la durée de l\'opération',
		action='store_true')


def get_args(stdin):
	usage = APP_NAME + ' <action> <src> <dst>'
	description = 'Utilitaire de suppression de fichier'
	parser = ArgumentParser(
		prog=APP_NAME, 
		usage=usage, 
		description=description)
	append_action(parser)
	append_src(parser)
	append_niter(parser)
	append_blank(parser)
	append_only_unlink(parser)
	append_hash_type(parser)
	append_time(parser)
	return parser.parse_args(stdin)

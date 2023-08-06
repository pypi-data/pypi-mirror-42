from hackerman.crypto import xor, hmc, blowfish
import argparse, getpass, sys

from hmcli.utils import load_module

modules = ["xor","hmc","blowfish"]



def parse_args():
	p = argparse.ArgumentParser()
	p.add_argument(
		"-m","--module",
		help=("Which hackerman.crypto module to use. Available: \
			xor, hmc, blowfish"),
		required=True)
	p.add_argument(
		"-e","--encrypt",
		help=("Encrypt input"),
		action="store_true")
	p.add_argument(
		"-d","--decrypt",
		help=("Decrypt input"),
		action="store_true")
	p.add_argument(
		"-p","--password",
		help=("Password to encrypt/decrypt input (if not given, user will be asked to input password securely)"))
	p.add_argument(
		"-f","--file",
		help=("Take input from file [default: prompt]"))
	p.add_argument(
		"-t","--text",
		help=("Take input from text [default: prompt]"))
	args = p.parse_args()
	#if args.encrypt is None and args.decrypt is None:
	if not args.encrypt and not args.decrypt:
		p.error("-e/--encrypt or -d/--decrypt is required")
	if args.module not in modules:
		p.error("module [%s] is not available" % args.module) 
	return args
def main(args):
	password = args.password if not args.password is None else getpass.getpass()
	crypto = load_module("hackerman.crypto",args.module)
	if args.text is None and args.file is None:
		tg = input("(Input)> ").encode()
	elif args.text:
		tg = args.text.encode()
	elif args.file:
		try:
			tg = open(args.file,"rb").read()
		except Exception as e:
			print("[!] Error reading input file [%s]:" % args.file,e)
			exit(1)

	res = crypto.encrypt(tg, password) if args.encrypt else crypto.decrypt(tg, password)
	sys.stdout.buffer.write(res) # print raw bytes

main(parse_args()) if __name__ == "__main__" else None

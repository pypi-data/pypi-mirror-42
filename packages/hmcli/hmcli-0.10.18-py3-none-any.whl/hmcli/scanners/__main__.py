import argparse
from hmcli.utils import load_module, print_raw

modules = ["tcp","http"]

def parse_args():
	p = argparse.ArgumentParser()
	p.add_argument(
		"-m","--module",
		help=("Which scanner to load. Available: tcp, http"),
		required=True)
	p.add_argument(
		"-t","--target",
		help=("Read target(s) from a comma-seperated list of addresses"))
	p.add_argument(
		"-f","--file",
		help=("Read target(s) from a newline-seperated list from a file"))
	args = p.parse_args()
	if args.target is None and args.file is None:
		p.error("-t/--target or -f/--file is required")
	return args
def main(args):
	mm = "_http" if args.module == "http" else args.module
	mod = load_module("hackerman.scanners",mm)
	tg = args.target.split(",") if args.target else open(args.file,"r").read().split("\n")
	res = {}
	for addr in tg:
		res[addr] = mod.knock(addr)
	for addr in res:
		print("%s: %s" % (addr, str(res[addr])))
main(parse_args()) if __name__ == "__main__" else None

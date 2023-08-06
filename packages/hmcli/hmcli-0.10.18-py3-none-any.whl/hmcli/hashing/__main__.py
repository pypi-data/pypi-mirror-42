import argparse
from hmcli.utils import load_module, print_raw

modules = ["sha256","sha1","md5"]

def parse_args():
	p = argparse.ArgumentParser()
	p.add_argument(
		"-m","--mode",
		help=("Which hashing mode to use. Available: \
			sha256, sha1, md5"),
		required=True)
	p.add_argument(
		"-t","--text",
		help=("Hash specified text"))
	p.add_argument(
		"-f","--file",
		help=("Hash specified file"))
	p.add_argument(
		"-d","--digest",
		help=("Output raw bytes or hexdigested[default]"),
		action="store_true")
	args = p.parse_args()
	if args.text is None and args.file is None:
		p.error("-t/--text or -f/--file is required")
	return args
def main(args):
	mod = load_module("hackerman.hashing",args.mode)
	tg = args.text.encode() if args.text else open(args.file,"rb").read()
	hd = False if args.digest else True
	res = mod(tg, hex=hd)
	if type(res) == str:
		print(res)
	else:
		print_raw(res)
main(parse_args()) if __name__ == "__main__" else None
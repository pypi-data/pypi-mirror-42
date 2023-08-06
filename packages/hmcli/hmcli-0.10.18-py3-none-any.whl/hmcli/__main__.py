import argparse

def parse_args():
	p = argparse.ArgumentParser()
	p.add_argument(
		"-l","--list",
		help=("List available modules"),
		action="store_true")
	p.add_argument(
		"-i","--info",
		help=("Print info about hmcli"),
		action="store_true")
	args = p.parse_args()
	if (not args.list) and (not args.info):
		p.error("no argument specified. nothing to do")
	return args
def main(args):
	if args.list:
		print("Modules: "+', '.join(["crypto","handlers","hashing","scanners"]))
	if args.info:
		print('''
	This program was made by Marcus Weinberger.
	It was made to provide a simple command-line
	interface to his hackerman library.

	GitHub: https://github.com/AgeOfMarcus
			''')
main(parse_args()) if __name__ == "__main__" else None
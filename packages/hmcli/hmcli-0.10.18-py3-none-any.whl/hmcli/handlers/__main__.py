import argparse, getpass

from hmcli.utils import load_module, print_raw

modules = ["reverse_tcp"]

def parse_args():
	p = argparse.ArgumentParser()
	p.add_argument(
		"-m","--module",
		help=("Which hackerman.handlers module to use. Available: \
			reverse_tcp"),
		required=True)
	p.add_argument(
		"--port",
		help=("Which port to bind to"),
		type=int,
		required=True)
	p.add_argument(
		"--password",
		help=("Password (if not selected, user will be given a secure input)"))
	p.add_argument(
		"-i","--interactive",
		help=("Drop into an interactive remote shell"),
		action="store_true")
	p.add_argument(
		"-c","--command",
		help=("Execute a command upon connection"))
	args = p.parse_args()
	if args.module not in modules:
		p.error("module [%s] is not available" % args.module)
	if args.interactive is None and args.command is None:
		p.error("-i/--interactive or -c/--command is required")
	return args
def main(args):
	mod = load_module("hackerman.handlers",args.module)
	password = getpass.getpass() if args.password is None else args.password
	handler = mod.Handler(args.port, password)
	if args.interactive:
		while True:
			try:
				cmd = input("(Handler)$ ")
				if cmd == "":
					continue
				elif cmd.startswith("cd "):
					print(handler.cd(cmd[2:]))
				else:
					print_raw(handler.sh(cmd))
			except KeyboardInterrupt:
				break
	else:
		res = handler.sh(args.command)
		print_raw(res)
main(parse_args()) if __name__ == "__main__" else None
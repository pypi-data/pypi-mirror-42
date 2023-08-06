import sys

def load_module(base, mod):
	try:
		exec("from %s import %s as module" % (base, mod))
		return locals()['module']
	except Exception as e:
		print("[!] Error loading hackerman.crypto.%s:" % mod,e)
		exit(1)

print_raw = sys.stdout.buffer.write

from pynodes import pynodes
from pynodes.ext import santi
import argparse, _thread

def parse_args():
	p = argparse.ArgumentParser()
	p.add_argument(
		"-m","--map",
		help=("Just find hosts. \
			Usage: --map"),
		action="store_true")
	p.add_argument(
		"-n","--node",
		help=("Start a simple node and print new peers. \
			Usage: --node 0.0.0.0:8080"))
	args = p.parse_args()
	if (not args.map) and (not args.node):
		p.error("nothing to do. Use -m/--map or -n/--node")
	return args
def main(args):
	if args.map:
		print("\n".join(santi.map_network()))
	if args.node:
		addr = args.node.split(":")[0], int(args.node.split(":")[1])
		node = pynodes.Node(addr)
		_thread.start_new_thread(node.start, ())
		old = node.peers
		while True:
			try:
				if not old == node.peers:
					new = node.peers
					[print("[*] New peer:",p) for p in new if not p in old]
					old = new
			except RuntimeError:
				continue
			except KeyboardInterrupt:
				break
main(parse_args()) if __name__ == "__main__" else None
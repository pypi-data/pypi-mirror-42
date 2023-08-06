from pynodes.ext import santi
import socket, _thread

class Node(object):
	def __init__(self, addr, timeout=2):
		self.timeout = timeout
		self.addr = addr
		self.server = socket.socket()
		self.server.setsockopt(socket.SOL_SOCKET, 
			socket.SO_REUSEADDR, 1)
		self.server.bind(addr)
		self.server.listen(100)
		self.peers = {}

	def checkpeerloop(self, check):
		while check():
			try:
				for peer in self.peers:
					conn = self.peers[peer]
					conn.settimeout(self.timeout)
					try:
						conn.send("nodealive".encode())
						r = conn.recv(1024)
					except (socket.timeout, ConnectionRefusedError, BrokenPipeError) as e:
						del self.peers[peer]
						conn.close()
			except RuntimeError:
				continue

	def getpeerloop(self, check):
		while check():
			net = santi.map_network()
			for ip in net:
				if ("%s:%i" % (ip, self.addr[1])) in self.peers:
					continue
				s = socket.socket()
				s.settimeout(self.timeout)
				try:
					s.connect((ip, self.addr[1]))
					self.peers["%s:%i" % (ip, self.addr[1])] = s
				except (socket.timeout, ConnectionRefusedError) as e:
					pass


	def start(self, check=lambda: True):
		_thread.start_new_thread(self.getpeerloop, (check,))
		_thread.start_new_thread(self.checkpeerloop, (check,))
		while check():
			conn, addr = self.server.accept()
			if ("%s:%i" % addr) in self.peers:
				continue
			self.peers["%s:%i" % addr] = conn

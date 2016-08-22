"""
	This class serves as a connection object;
	providing the caller a method to look at and handle incoming packets
"""
import socket
import os
import threading
import Queue
import collections
import struct

class Connection(object):
	HEADER_LEN = 15
	CLIENT, SERVER = (0, 1)

	def __init__(self, port, save_folder):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
		self.sock.bind(('0.0.0.0',port))

		self.save_folder = save_folder
		self.curr_file_lock = threading.lock()

		self.data_queue = Queue()
		self.cs_data = collections.defaultdict(int)


	def listen(self):
		while True:
			data = self.sock.recvfrom(0xFFFF)[0]
			self.data_queue.put(data)

	def parse(self, data):
		if len(data) < Connection.HEADER_LEN:
			return None

		header = data[:Connection.HEADER_LEN]
		message = data[Connection.HEADER_LEN:]

		csid, connection_id, msg_id, msg_len, side = struct.unpack('<LLLHB',header)

		if len(message) != msg_len:
			return None

		if side == Connection.CLIENT:
			side = 'client'
		else:
			side = 'server'

		return csid, connection_id, msg_id, side, message
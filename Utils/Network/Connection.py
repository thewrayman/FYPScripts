"""
	This class serves as a connection object;
	providing the caller a method to look at and handle incoming packets
"""
import socket
import os
import threading
from Queue import Queue
import collections
import struct
import time
import uuid
import pickle
import thread

MAX_CS_SIZE = 6*1024*1024  # 6 megs
CHUNKS_TIME = 60  # 1 minute

class Connection(object):
	HEADER_LEN = 15
	CLIENT, SERVER = (0, 1)

	def __init__(self, port, save_folder):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
		self.sock.bind(('127.0.0.1', port))

		self.save_folder = save_folder
		self.curr_file_lock = threading.Lock()

		self.data_queue = Queue()
		self.cs_data = collections.defaultdict(int)

		self.curr_out_filename = None
		self.curr_out_file = None

		self.log_every_packet = True

	def listen(self):
		while True:
			data = self.sock.recvfrom(0xFFFF)[0]
			print "data:",data
			self.data_queue.put(data)

	def parse(self, data):
		print "parsing data"
		print len(data)
		print data
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

	def write(self, packet):
		"""
			Write the provided packet data to a file as a pickled obj
		"""
		try:
			pktcs = packet[0]   #csid
			pktside = packet[-2]    #side

			if pktside != "server":
				return

			datasize = len(packet[-1])

			if self.curr_file_lock.aquire():
				if self.cs_data[pktcs] < MAX_CS_SIZE:
					if (self.curr_out_file is None) or (self.curr_out_filename is None):
						self.curr_out_filename = os.path.join(self.save_folder, str(time.time()) + '_' +
																str(uuid.uuid4()) + '_network_traffic')
						print("Starting dumping to new file:" + str(self.curr_out_filename))
						self.curr_out_file = open(self.curr_out_filename, 'wb')
					self.cs_data[pktcs] += datasize
					pickle.dump(packet, self.curr_out_file)
					self.curr_out_file.flush()
				self.curr_file_lock.release()
			else:
				print("Unable to obtain lock on current file, ignoring the packet.")
		except Exception as e:
			try:
				# Try to release the lock, to avoid deadlocks.
				self.curr_file_lock.release()
			except Exception as e1:
				# Ignore all exceptions.
				pass
			print("Unexpected error occurred while trying to write packet to file:" + str(e))

def pkt_processor_thread(connection):
    """
        Thread which parses each UDP pkt and writes the corresponding data into a file
    :param connection_object: Connection object, which is the producer of the data.
    :return: Never return
    """
    print "pkt process thread"
    target_data_queue = connection.data_queue
    while True:
        print "True"
        try:
            print "try"
            curr_data = target_data_queue.get(True, 5)
            print "getting packet"
            packet = connection.parse(curr_data)
            print "got packet"
            if packet is None:
                print "packet is none"
                continue
            print "logpacket is",connection.log_every_packet
            print "packet is",packet
            if connection.log_every_packet:
                csid, connection_id, msg_id, side, message = packet
                print("csid: " + str(csid) + " connection: " + str(connection_id) + " message_id: " + str(msg_id) +
                         " side: " + str(side))
            connection.write_packet(packet)
        except Exception as e:
            print("Error occurred while trying to process pkt:" + str(e) + ", Ignoring and moving on.")

def dumpIncomingData(connection):
    """
    Thread which writes the collected data to DB.
    :param connection_object: Connection object, which needs to be monitored.
    :return:
    """
    print("Starting Data Dumper Thread.")
    #cleanup_traffic_files = str2bool(os.environ.get('CLEANUP_RAW_TRAFFIC_FILES', "True"))
    while True:
        # sleep for chunks time.
        time.sleep(CHUNKS_TIME)
        try:
            target_file_name = None
            #curr_round = Round.current_round()
            if connection.curr_out_file is not None:
                # blocking acquire
                connection.curr_file_lock.acquire()
                # close the current files
                target_file_name = connection.curr_out_filename
                # Do not close file here (as it might delay the pkt processor thread),
                # just get the file object and move on
                # we want the network thread to be super fast.
                target_fp = connection.curr_out_file
                connection.curr_out_file = None
                connection.curr_out_filename = None
                connection.cs_data = collections.defaultdict(int)
                # release file locks.
                connection.curr_file_lock.release()
                # close the file
                target_fp.close()
                if target_file_name is not None:
                    #print("Chunk Time Expired in Round:" + str(curr_round.num) + ". Dumping the file:"
                             #+ str(target_file_name) + " into DB.")
                    fp = open(target_file_name, 'rb')
                    file_data = fp.read()
                    fp.close()
                    # check if we need to clean up..if yes, remove the file.
                    #if cleanup_traffic_files:
                        #os.system('rm ' + target_file_name)
                    #RawRoundTraffic.create(round=curr_round, pickled_data=file_data)
        except Exception as e:
            try:
                # To avoid deadlocks.
                connection.curr_file_lock.release()
            except Exception as e1:
                pass
            print("Error occurred while trying to save the dump file to DB:" + str(e))

def main():
	targetfolder = os.getcwd()
	port = 8080
	connection = Connection(port,targetfolder)
	thread.start_new_thread(pkt_processor_thread, (connection, ))
	print "starting to listen.."
	connection.listen()

if __name__ == '__main__':
    main()
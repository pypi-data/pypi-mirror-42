import socket
from threading import Thread

status = {
	200: "200 OK",
	404: "404 NOT FOUND",
	401: "401 Unauthorized"
}

def mkHeader(header):
	return f"\n\r{header}\n\r"

class HTTPServer(object):
	def __init__(self,callback, ip="0.0.0.0", port=8088):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((ip, port))
		self.sock.listen(1)
		self.running = True
		self.threads = []
		self.callback = callback
		self.server_info = (ip, port)
	
	def kill(self):
		self.running = False
	
	def run(self):
		while self.running:
			conn, addr = self.sock.accept()
			self.threads.append(Thread(target=self.__handleConn, args=(conn,addr)))
			self.threads[len(self.threads) - 1].start()
	
	def __handleConn(self, conn, addr):
		while self.running:
			data = conn.recv(1024)
			if not data: break
			
			headers = data.decode().split("\r\n")
			
			file = headers[0].split(" ")[1]
			
			status, payload = self.callback(file, addr, (self.server_info, headers))
			
			conn.send(f"HTTP/1.1 {status}\n\r".encode())
			conn.send(b"Content-Type: text/html; charset=UTF-8\n\r\n\r")
			conn.send(payload.encode())
			break
conn.close()
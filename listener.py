#!/usr/bin/env python3

import socket


def main():
	print("Starting socket on localhost port 12345")
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(("127.0.0.1", 12345))
		s.listen()
		while True:
			conn, _ = s.accept()
			with conn:
				data = conn.recv(1024)
				print("Received:", data.decode("utf-8"))


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("Shutting down")

#!/usr/bin/env python3

import argparse
import socket

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--turn-on", action="store_true")
	parser.add_argument("--turn-off", action="store_true")
	args = parser.parse_args()

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect(("127.0.0.1", 12345))
		if args.turn_on:
			s.send(b"turn on")
		elif args.turn_off:
			s.send(b"turn off")

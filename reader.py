#!/usr/bin/env python3

from pynput import keyboard
#!/usr/bin/env python3

from pynput import keyboard


class LogsReader():
	def __init__(self, filename: str = ".logs") -> None:
		self.filename = filename
		self.int_log = []


	def read_file(self):
		with open(self.filename, 'rb') as bin_logs:
			while (key := bin_logs.read(2)) != b'':
				self.int_log.append(int.from_bytes(key, byteorder="big"))
			print (self.int_log)

if __name__ == '__main__':
	reader = LogsReader()
	reader.read_file()

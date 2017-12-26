import serial
import logging

class PMSx003(object):

	cmd_read_passive = b'\x42\x4d\xe2\x00\x00\x01\x71'
	cmd_set_passive = b'\x42\x4d\xe1\x00\x00\x01\x70'
	cmd_set_active = b'\x42\x4d\xe1\x00\x01\x01\x71'
	cmd_sleep = b'\x42\x4d\xe4\x00\x00\x01\x73'
	cmd_wakeup = b'\x42\x4d\xe4\x00\x01\x01\x74'

	MODE_ACTIVE = 0x01
	MODE_PASIVE = 0x00
	
	def __init__(self,port):
		self.ser = serial.Serial(port,9600)
		self.mode = self.MODE_ACTIVE 
	
	def _checksum_check(self,data):
		checksum = sum(data[:-2])
		if checksum == int.from_bytes(data[-2:],byteorder='big'):
			return True
		return False
		
	def _parse_data(self,data):
		result = {}
		result["pm1.0std"] = int.from_bytes(data[0:2],byteorder='big')
		result["pm2.5std"] = int.from_bytes(data[2:4],byteorder='big')
		result["pm10std"] = int.from_bytes(data[4:6],byteorder='big')
		result["pm1.0"] = int.from_bytes(data[6:8],byteorder='big')
		result["pm2.5"] = int.from_bytes(data[8:10],byteorder='big')
		result["pm10"] = int.from_bytes(data[10:12],byteorder='big')
		result["0.3num"] = int.from_bytes(data[12:14],byteorder='big')
		result["0.5num"] = int.from_bytes(data[14:16],byteorder='big')
		result["1.0num"] = int.from_bytes(data[16:18],byteorder='big')
		result["2.5num"] = int.from_bytes(data[18:20],byteorder='big')
		result["5num"] = int.from_bytes(data[20:22],byteorder='big')
		result["10num"] = int.from_bytes(data[22:24],byteorder='big')
		return result

	def read_all(self):
		if self.mode != self.MODE_ACTIVE:
			raise(NotImplementedError("Passive mode not implemented"))
		try:
			while True:
				ch = self.ser.read(1)
				if (ch != b'\x42'):
					continue
				logging.debug("Got 0x42")
				ch = self.ser.read(1)
				if (ch != b'\x4d'):
					continue
				logging.debug("Got 0x4d")
				data = b'\x42\x4d'+self.ser.read(30)
				if not self._checksum_check(data):
					logging.warning("Checksum error")
					return None
				length = int.from_bytes(data[2:4],byteorder='big') 
				if length != 28:
					logging.warning("Length error ({} instead of 28)".format(length))
					return None
				return self._parse_data(data[4:])
		except IOError:
			logging.warning("IO error when reading")
			return None
	
	def wakeup(self):
		try:
			logging.debug("Waking up")
			self.ser.write(self.cmd_wakeup)
			self.read_all()
			logging.info("Woken up")
		except IOError:
			logging.warning("IO error when waking up")
			return None
	
	def sleep(self):
		try:
			self.ser.write(self.cmd_sleep)
		except IOError:
			logging.warning("IO error when putting to sleep")
			return None
		
	def set_active(self):
		try:
			self.ser.write(self.cmd_set_active)
		except IOError:
			logging.warning("IO error when setting to active")
			return None

	def set_passive(self):
		try:
			self.ser.write(self.cmd_set_passive)
		except IOError:
			logging.warning("IO error when setting to passive")
			return None

import sys
import os

#

class BytesDecoder:
	def decode(self, bytes):
		print("decode not implemented")
	
#

class XOrA3Decoder(BytesDecoder):
	def decode(self, bytes_to_decode):
		result = True
		try:
			for idx in range(0, len(bytes_to_decode)):
				bytes_to_decode[idx] ^= 0xa3
		except Exception as ex:
			print("Decode exception: ", ex)
			result = False
			
		return result
#

class BytesReader:
	def readBytes(self, path):
		source_file = None
		result = None
		try:
			source_file = open(path, "rb")
			result = source_file.read()
		except Exception as ex:
			print("BytesReader exception occurred:\n", ex)
		finally:
			if None != source_file:
				source_file.close()
				
		return result
	
#

class BytesWriter:
	def writeBytes(self, write_path, bytes):
		result = False;
		try:
			write_file = open(write_path, "wb")
			write_file.write(bytes)
			result = True
		except Exception as ex:
			print("BytesWriter exception occurred:\n", ex)
		finally:
			if None != write_file:
				write_file.close()
		return result

#

class Converter:
	def convert(self, source_path, destination_path):
		if None == self.bytes_reader:
			print("Converter needs a BytesReader object.")
			return False
			
		if None == self.bytes_writer:
			print("Converter needs a BytesWriter object.")
			return False
		
		if None == self.bytes_decoder:
			print("Converter needs a BytesDecoder object.")
			return False

		bytes = self.bytes_reader.readBytes(source_path)
		if None == bytes:
			print("Read file: ", source_path, " Failed")
			return False
			
		write_byte_array = bytearray(bytes)
		if False == self.bytes_decoder.decode(write_byte_array):
			print("Decode Failed")
			return False
		
		if self.bytes_writer.writeBytes(destination_path, write_byte_array):
			print("Complete!")
			return True
		else:
			print("Write file: ", destination_path, " Failed")
			return False

#

class PathParser:
	def Parse(self, full_path):
		if None == full_path:
			return False
		
		path_str_array = full_path.split(".")
		if 2 != len(path_str_array):
			print("Invalid path: ", full_path)
			return False

		self.full_path = full_path
		self.path_without_extension = path_str_array[0]
		self.extension_name = path_str_array[1]
		return True

#

if 2 != len(sys.argv):
	print("no input file")
else:
	path_parser = PathParser()
	
	if path_parser.Parse(sys.argv[1]):	
		converter = Converter()
		
		converter.bytes_reader = BytesReader()
		converter.bytes_writer = BytesWriter()
		
		converter.bytes_decoder = XOrA3Decoder()
		
		converter.convert(sys.argv[1], path_parser.path_without_extension + ".mp3")

os.system("pause")

import sys

#location to write message
byte = 0x5000

def main():
	#message to binary
	def string_to_bin(mess):
		l = []
		for i in mess:
			b = bin(ord(i))[2:]
			if len(bin(ord(i))[2:]) < 8:
				for i in range(8-len(bin(ord(i))[2:])):
					b ='0' + b
			for i in range(8):
				l.append(int(b[i]))
		return l


	#encode
	def encode(input_f, output_f, message_f):
		f = open(input_f, 'rb')
		l_in = f.read()
		file_mess = open(message_f,'rb')
		message = file_mess.read()
		m = string_to_bin(message)
		l_out = []

		#copy 64 bytes header
		for i in range(byte):
			l_out.append(l_in[i])

		#add length message
		l_out.append(chr(len(message)))

		#add message
		for i in range(byte+1, len(l_in)):
			if (i-byte-1) < len(m): 
				if ord(l_in[i]) % 2 == 0:
					if m[i-byte-1] == 1:
						l_out.append(chr((ord(l_in[i]) + 1)%256))
					else:
						l_out.append(l_in[i])
				else:
					if m[i-byte-1] == 0:
						l_out.append(chr((ord(l_in[i]) + 1)%256))
					else:
						l_out.append(l_in[i])
			else:
				l_out.append(l_in[i])

		#write to output file
		o = open(output_f, 'wb')
		for i in range(len(l_out)):
			o.write(l_out[i])
		print "Success!!!"


	#binary to string
	def bin_to_string(l):
		a = []
		for i in range(0,len(l),8):
			s=''
			for j in range(i, i+8):
				s+=str(l[j])
			s = '0b' + s
			s = int(s,2)
			a.append(s)
		st = ''
		for i in range(len(a)):
			st+=chr(a[i])
		return st


	#decode
	def decode(input_f,output_f):
		f = open(input_f,'rb')
		l_in = f.read()
		l_out = []
		len_mess = ord(l_in[byte]) #check length message
		for i in range(byte+1, byte+1+len_mess*8):
			if ord(l_in[i]) % 2 == 0:
				l_out.append(0)
			else:
				l_out.append(1)
		#write to ouput file
		st = bin_to_string(l_out)
		o = open(output_f,'wb')
		o.write(st)
		print "Success!!!"

	#Usage:
	usage = '''Tool steganography to hiding message into audio using Parity method
	Usage:
		Encode:
			-e: Encode
			-i: Input file
			-m: Message file
			-o: Output file
			Example: python steg.py -e -i Example1.wav -m message.txt -o Example2.wav
		Decode:
			-d: Decode
			-i: Input file
			-o: Message output file
			Example: python steg.py -e -i Example1.wav -o message.txt
------------------------------Unicorn TEAM------------------------------
'''
	if len(sys.argv) > 1:
		if sys.argv[1] == '-e':
			input_f = ''
			message_f = ''
			output_f = ''
			for i in range(2, len(sys.argv)):
				if sys.argv[i] == '-i':
					input_f = sys.argv[i+1]
				elif sys.argv[i] == '-m':
					message_f = sys.argv[i+1]
				elif sys.argv[i] =='-o':
					output_f = sys.argv[i+1]
			if (input_f == '' or message_f == '' or output_f == ''):
				print usage
			else:
				encode(input_f, output_f,message_f)
		elif sys.argv[1] == '-d':
			input_f = ''
			output_f = ''
			for i in range(2, len(sys.argv)):
				if sys.argv[i] == '-i':
					input_f = sys.argv[i+1]
				elif sys.argv[i] =='-o':
					output_f = sys.argv[i+1]
			if (input_f == '' or output_f == ''):
				print usage
			else:
				decode(input_f, output_f)
	else:
		print usage
		

if __name__ == '__main__':
	main()

#pip install progressbar2
import sys
import time
import progressbar

def main():
	widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ',
    ]
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


	#add len message to output file
	def len_mess_e(len_m, l_out):
		n = hex(len_m)[2:]
		for i in range(8-len(n)):
			n = '0' + n
		l = []
		for i in range(0,len(n),2):
			s = '0x' + n[i] + n[i+1]
			l.append(int(s,16))
		for i in range(4):
			l_out.append(chr(l[i]))
		return l_out


	#check_parity
	def check_parity_encode(a, b, mess):
		count = 0
		a = bin(ord(a))[2:]
		b = bin(ord(b))[2:]
		if len(a) < 8:
			for i in range(8-len(a)):
				a = '0' + a
		if len(b) < 8:
			for i in range(8-len(b)):
				b ='0' + b
		a = a+b
		lsb = a[-1:]
		for i in a[:-1]:
			if int(i) == 1:
				count += 1
		if count % 2 == 0:	# even parity
			if mess == 1:	# message embed 1
				lsb = 1
			else:			# message embed 0
				lsb = 0
		else:				# odd parity
			if mess == 0:	# message embed 0
				lsb = 1
			else:			# message embed 1
				lsb = 0
		a = a[:-1] + str(lsb)
		return chr(int("0b"+a[0:8],2)%256), chr(int("0b"+a[8:],2)%256)

	def add_Pin(pin_e,l_out):
		h = hex(pin_e)[2:]
		for i in range(6-len(h)):
			h = "0"+h
		l_out.append(chr(int("0x"+h[:2],16)))
		l_out.append(chr(int("0x"+h[2:4],16)))
		l_out.append(chr(int("0x"+h[4:],16)))
		return l_out

	#encode
	def encode(input_f, output_f, message_f):
		# read sample
		f = open(input_f, 'rb')
		l_in = f.read()
		# read message
		file_mess = open(message_f,'rb')
		message = file_mess.read()
		m = string_to_bin(message)

		# Use pin_e
		pin_e = raw_input("Enter the PIN: ")
		while len(pin_e) > 6 or not pin_e.isdigit():
			print "PIN has a maximum length of 6 characters and only include digits"
			pin_e = raw_input("Enter the PIN: ")


		pin_e = int(pin_e)
		if pin_e <= 64:
			pin_e += 64
		if (len(l_in) - pin_e-1) < len(m):
			a = (len(l_in)-pin_e-1)/16
			print "Message too big. You only hiding %d words."%a
		else:	
			l_out = []
			print "\nRead file "+input_f+" and embed message.\n"
			#copy 64 bytes header
			for i in range(pin_e):
				l_out.append(l_in[i])

			#add PIN
			lout = add_Pin(pin_e,l_out)
			#add length message
			l_out = len_mess_e(len(message), l_out)

			#add message
			for i in progressbar.progressbar(range(pin_e+7, len(l_in), 2)):
				if (i-pin_e-7)/2 < len(m):
					a, b = check_parity_encode(l_in[i], l_in[i+1], m[(i-pin_e-7)/2])
					l_out.append(a)
					l_out.append(b)
				else:
					try:
						l_out.append(l_in[i])
						l_out.append(l_in[i+1])
					except:
						l_out.append(l_in[i])
			print "\nMake file " + output_f + "\n"
			#write to output file
			o = open(output_f, 'wb')
			for i in progressbar.progressbar(range(len(l_out))):
				o.write(l_out[i])
			print "\nSuccess!!!"


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


	#read len message to input file
	def len_mess_d(l_in, pin_d):
		l = []
		for i in range(4):
			l.append(ord(l_in[pin_d+i]))
		s = '0x'
		for i in range(len(l)):
			if len(hex(l[i])[2:])>1:
				s+=str(hex(l[i])[2:])
			else:
				s+="0" + str(hex(l[i])[2:])
		return int(s,16)
	

	#check PIN
	def check_PIN(l_in, pin_d):
		l = []
		for i in range(3):
			l.append(ord(l_in[pin_d+i]))
		s = '0x'
		for i in range(len(l)):
			if len(hex(l[i])[2:])>1:
				s+=str(hex(l[i])[2:])
			else:
				s+="0" + str(hex(l[i])[2:])
		pin = int(s,16)
		if pin != pin_d:
			print "The PIN you input maybe wrong. Try another PIN."
			exit(1)


	def check_parity_decode(a, b):
		count = 0
		a = bin(ord(a))[2:]
		b = bin(ord(b))[2:]
		if len(a) < 8:
			for i in range(8-len(a)):
				a = '0' + a
		if len(b) < 8:
			for i in range(8-len(b)):
				b ='0' + b
		a = a+b
		for i in a:
			if int(i) == 1:
				count += 1
		if count % 2 == 0:
			return 0
		else:
			return 1


	#decode
	def decode(input_f,output_f):
		# read sample
		f = open(input_f,'rb')
		l_in = f.read()
		l_out = []
		
		#Use pin_e 
		pin_d = raw_input("Enter the PIN: ")
		while len(pin_d) > 6 or not pin_d.isdigit():
			print "PIN has a maximum length of 6 characters and only include digits"
			pin_d = raw_input("Enter the PIN: ")


		pin_d = int(pin_d)
		if pin_d <= 64:
			pin_d += 64

		check_PIN(l_in,pin_d)
		len_mess = len_mess_d(l_in, pin_d+3) #check length message
		print "\nProcessing...\n"
		for i in progressbar.progressbar(range(pin_d+7, pin_d+7+len_mess*16,2)):
			a = check_parity_decode(l_in[i], l_in[i+1])
			l_out.append(a)
			time.sleep(0.0002)

		#write to ouput file
		st = bin_to_string(l_out)
		o = open(output_f,'wb')
		o.write(st)
		print "\nSuccess!!!"


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
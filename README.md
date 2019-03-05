# ToolStegAudioParity
Tool steganography to hiding message into audio using Parity method
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

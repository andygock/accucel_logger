import serial, sys, io, time

"""

Logger for iMax-B6, Turnigy Accucel-6 and similar 4-button chargers

by Andy Gock

CSV output in format:

	time,minutes,voltage,current,charge

If using Windows:

	Download wintee: http://code.google.com/p/wintee/
	(allows logging to file AND viewing output at the same time)

Run (Win):

	del file.txt
	python log.py COM14 | wtee file.txt

Run (Linux/Mac):

	python log.py /dev/ttyUSB0 | tee file.txt

Press Ctrl+C to terminate.

"""



""" From: https://gist.github.com/7h3rAm/5603718 """
def hexdump(src, length=16, sep='.'):
	FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or sep for x in range(256)])
	lines = []
	for c in xrange(0, len(src), length):
		chars = src[c:c+length]
		hex = ' '.join(["%02x" % ord(x) for x in chars])
		if len(hex) > 24:
			hex = "%s %s" % (hex[:24], hex[24:])
		printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or sep) for x in chars])
		lines.append("%08x: %-*s |%s|\n" % (c, length*3, hex, printable))
	print ''.join(lines)


""" Script starts here """

if len(sys.argv) == 1:
	print "Usage:"
	print "  python " + sys.argv[0] + " SERIAL_PORT"
	sys.exit()

try:
	ser = serial.Serial(sys.argv[1])
	if not ser:
		print "Could not open serial port: " + str(sys.argv[1])
		sys.exit()
except:
	print "Could not open serial port: " + str(sys.argv[1])
	sys.exit()

pos         = 0
data        = "" # binary string
frames_read = 0
time_start  = 0

while True:
	c = ser.read()
	if c == '{':
		#print "---\n"
		pos  = 0
		data = ""
		data += c

	elif c == '}':
		pos  += 1
		data += c
		
	else:
		pos  += 1
		data += c

	if c == '}': # End of frame marker
		
		if pos == 75: # Correct frame size
			sample = {}

			if frames_read == 0:
				time_start = time.time()
				sample['time'] = 0
			else:
				sample['time'] = round(time.time() - time_start,3)

			frames_read += 1

			#hexdump(data)
			#continue

			# Protocol reverse engineered by
			# Ref: http://blog.dest-unreach.be/2012/01/29/imax-b6-charger-protocol-reverse-engineered
			sample['current'] = ord(data[33])-128 + (ord(data[34])-128)/100.0
			sample['voltage'] = ord(data[35])-128 + (ord(data[36])-128)/100.0
			sample['input_voltage'] = ord(data[41])-128 + (ord(data[42])-128)/100.0
			sample['charge'] = (ord(data[43])-128)*100 + (ord(data[44])-128)
			sample['minutes'] = ord(data[70])-128

			#print sample

			if frames_read == 1:
				# Header row
				print "Time(s),Minutes,Voltage(V),Current(A),Charge(mAh)"

			print ','.join([
				str(sample['time']),
				str(sample['minutes']),
				str(sample['voltage']),
				str(sample['current']),
				str(sample['charge'])
			])
			sys.stdout.flush()

ser.close()

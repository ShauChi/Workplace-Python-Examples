# code to make a QRCode out os any input URL
import sys, io, pyqrcode
if len(sys.argv) != 2:
	print "Please enter 1 and only 1 URL\n"
else:
	URL = pyqrcode.create(sys.argv[1])
	URL.svg('output.svg', scale=4)

accucel_logger
==============

by Andy Gock

Logger for iMax-B6, Turnigy Accucel-6 and similar 4-button chargers

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

#!/usr/bin/env python

from hcmidiaSync import *

def main(argv):
	hosts = {}
	hosts['origemHost'] = 'http://192.168.0.76/hcmedia'
   	hosts['screenlyHost'] = 'http://192.168.0.11'
   	try:
   		opts, args = getopt.getopt(argv,"hi:o:",["sHost=","oHost="])
   	except getopt.GetoptError:
		print 'sync.py -s <screenlyHost> -o <origemHost>'
		sys.exit(2)
   	for opt, arg in opts:
		if opt == '-h':
			print 'sync.py -s <screenlyHost> -o <origemHost>'
			sys.exit()
		elif opt in ("-s", "--sHost"):
			hosts['screenlyHost'] = arg
		elif opt in ("-o", "--oHost"):
			hosts['origemHost'] = arg
	return hosts




hosts = main(sys.argv[1:])
host = hosts['screenlyHost']
hcmidia_host = hosts['origemHost']
sync()
import os
import mirouter

def get_online_dev():
	mr = mirouter()
	devlist = mr.get_devlist()
	for dev in devlist:
		print '* %s %s %s\n' % (dev['name'], dev['ip']['ip'], dev['ip']['online'])

if __name__ == '__main__':
	get_online_dev()

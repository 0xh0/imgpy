# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, os, multiprocessing
from subprocess import check_output


def progress(data):
	for path in data:
		if path.endswith('.jpg') or path.endswith('.jpeg'):
			try:
				check_output(['jpegtran', '-optimize', '-progressive', '-copy', 'none', '-perfect', '-trim' , '-outfile', path, path])
			except:
				print path

	sys.exit('End!')


if __name__ == '__main__':
	flist = []
	for ndir in os.listdir(sys.argv[1]):
		ndir = sys.argv[1] + '/' + ndir
		if os.path.isdir(ndir) is True:
			for nfile in os.listdir(ndir):
				flist.append(ndir + "/" + nfile)

	step = (len(flist)-1)/int(sys.argv[2])

	print step

	for num in xrange(0,len(flist)-1, step):
		if(num == len(flist)):
			continue

		multiprocessing.Process(target=progress, args=(flist[num:(num+step)],)).start()

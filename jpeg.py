# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, os, multiprocessing, logging, subprocess
from subprocess import check_output

def get_img(root, pool):
        for ndir in os.listdir(root):
                ndir = root + '/' + ndir
                if os.path.isdir(ndir):
                        get_img(ndir, pool)
                else:
                        if ndir.endswith('.jpg') or ndir.endswith('.jpeg'):
                                pool.put(ndir.strip())

def progress(pool):
	FNULL = open('tmp', 'a')
	while not pool.empty():
		path = pool.get()
		with open(os.devnull, "w") as fnull:
			try:
				tmp = subprocess.call(['jpegtran', '-optimize', '-progressive', '-outfile', path, path], stdout = fnull, stderr = fnull)
			except Exception as e:
				logging.error(path + ';;' + str(e))

	sys.exit('End!')

if __name__ == '__main__':
	logging.basicConfig(format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s', level = logging.DEBUG, filename = u'logging.txt')
	pool = multiprocessing.Queue()

	get_img(sys.argv[1], pool)

	for num in range(0, int(sys.argv[2])):
		multiprocessing.Process(target=progress, args=(pool,)).start()

import os
from kinparse import *

files_at_start = set([])

def setup_function(f):
    global files_at_start
    files_at_start = set(os.listdir('.'))

def teardown_function(f):
    files_at_end = set(os.listdir('.'))
    for file in files_at_end - files_at_start:
        try:
            os.remove(file)
        except Exception:
            pass

if __name__ == '__main__':
    setup_function(None)
    with open('test.txt','wb') as f:
        f.write('test')
    teardown_function(None)

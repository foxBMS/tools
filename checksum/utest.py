import unittest
import os
import sys
import shutil
import subprocess

import chksum

class TestChecksumTool(unittest.TestCase):

    def test_chksum(self):
        print '\n'
        for i in xrange(len(scases)):
            print "+--------------------+"
            print "|Running test", i+1, '     |'
            chksum, file = scases[i]
            chksum = chksum.split('.')[1]
            print "+--------------------+"
            print "|file:  ", file, '|'
            print "|chksum:", chksum, ' |'
            tool = 'python'
            script = os.path.join(FILE_PATH, 'chksum.py')
            ini_file = os.path.join(FILE_PATH, 'chksum.ini')
            hex_file = '-hf='+os.path.join(TEST_DIR, file)
            cmd = ' '.join([tool, script, ini_file, hex_file])
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            p.wait()
            out, err = p.communicate()
            cs = (((out.split('* 32-bit SW-Chksum:     ')[1]).split('*'))[0].strip())
            print "|cs:    ", cs, ' |'
            print "+--------------------+\n"
            self.assertEqual(cs, chksum)
        try:
            shutil.rmtree(os.path.join(FILE_PATH, 'build'))
        except OSError as e:
            print e

if __name__ == '__main__':
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    TEST_DIR = os.path.join(FILE_PATH,'utest')
    cases = os.listdir(TEST_DIR)
    scases = [cases[i:i + 2] for i in xrange(0, len(cases), 2)]
    unittest.main()

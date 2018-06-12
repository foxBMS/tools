# @copyright &copy; 2010 - 2018, Fraunhofer-Gesellschaft zur Foerderung der
#   angewandten Forschung e.V. All rights reserved.
#
# BSD 3-Clause License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1.  Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
# 2.  Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
# 3.  Neither the name of the copyright holder nor the names of its
#     contributors may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# We kindly request you to use one or more of the following phrases to refer to
# foxBMS in your hardware, software, documentation or advertising materials:
#
# &Prime;This product uses parts of foxBMS&reg;&Prime;
#
# &Prime;This product includes parts of foxBMS&reg;&Prime;
#
# &Prime;This product is derived from foxBMS&reg;&Prime;

import unittest
import os
import sys
import shutil
import subprocess
import logging
import filecmp

import chksum
import writeback

class TestChecksumTool(unittest.TestCase):

    def test_chksum(self):
        print('\n')
        for i in range(len(scases)):
            print('+--------------------+')
            print('|Running test', i+1, '     |')
            chksum, file, file_with_cs = scases[i]
            chksum = chksum.split('.')[1]
            print('+--------------------+')
            print('|file:  ', file, '|')
            print('|chksum:', chksum, ' |')
            tool = 'python'
            script = os.path.join(FILE_PATH, 'chksum.py')
            ini_file = os.path.join(FILE_PATH, 'chksum.ini')
            hex_file = '-hf='+os.path.join(TEST_DIR, file)
            input_file = os.path.join(TEST_DIR, file)
            result_file = os.path.join(TEST_DIR, file_with_cs)
            cmd = ' '.join([tool, script, ini_file, hex_file])
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, shell=True)
            p.wait()
            out, err = p.communicate()
            cs = (((out.split('* 32-bit SW-Chksum:     ')[1]).split('*'))[0].strip())
            print('|cs:    ', cs, ' |')
            print('+--------------------+\n')
            self.assertEqual(cs, chksum)
            print os.getcwd()
            self.assertTrue(filecmp.cmp(input_file, result_file))
        try:
            shutil.rmtree(os.path.join(TEST_DIR, 'build')) # TODO cwd dependent...
        except OSError as e:
            print e

if __name__ == '__main__':
    FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    TEST_DIR = os.path.join(FILE_PATH,'utest')
    cases = os.listdir(TEST_DIR)
    scases = [cases[i:i + 3] for i in xrange(0, len(cases), 3)] # TODO OS dependent
    unittest.main()

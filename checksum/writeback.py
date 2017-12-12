# @copyright &copy; 2010 - 2017, Fraunhofer-Gesellschaft zur Foerderung der angewandten Forschung e.V. All rights reserved.
#
# BSD 3-Clause License
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 1.  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 2.  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3.  Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# We kindly request you to use one or more of the following phrases to refer to foxBMS in your hardware, software, documentation or advertising materials:
#
# &Prime;This product uses parts of foxBMS&reg;&Prime;
#
# &Prime;This product includes parts of foxBMS&reg;&Prime;
#
# &Prime;This product is derived from foxBMS&reg;&Prime;

"""
@file       writeback.py
@date       30.11.2017 (date of creation)
@author     foxBMS Team
@ingroup    tools
@prefix     none
@brief      Writing a checksum back into a binary file
"""

import sys
import os
import argparse
import subprocess

__version__ = 0.1
__date__ = '2017-11-30'
__updated__ = '2017-11-30'

def main():
    HELP_TEXT = """Reads the ouput file of the checksum tool, and writes the \
checksum back into the specified elf file using the program passed by command \
line argument.
    """
    parser = argparse.ArgumentParser(description=HELP_TEXT, add_help=True)
    parser.add_argument('-c', '--conffile', help='directory where the checksum ouput is stored')
    parser.add_argument('-e', '--elffile', help='elffile the checksum shoudl be written into')
    parser.add_argument('-t', '--tool', default='arm-none-eabi-gdb', help='tool used to write in the elf file')
    args = parser.parse_args()

    conffile = args.conffile
    elffile = args.elffile
    tool = args.tool

    for _fr in [conffile, elffile, tool]:
        if not os.path.isfile(_fr):
            raise RuntimeError('{} is missing'.format(_fr))

    with open(conffile, 'r') as fcs_conf:
        __cs = fcs_conf.read()
    checksum = (((__cs.split('* 32-bit SW-Chksum:     ')[1]).split('*'))[0].strip())
    print '\nWriting checksum {} into {}'.format(checksum, elffile)
    cmd = '''{} -q -se={} --write \
-ex="set var ver_sw_validation.Checksum_u32={}" \
-ex="print ver_sw_validation.Checksum_u32" \
-ex="quit"'''.format(tool, elffile, checksum)
    print cmd
    proc_write_to_elf = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, shell=True)
    std_out, std_err = proc_write_to_elf.communicate()
    rtn_code = proc_write_to_elf.returncode
    if std_out:
        print std_out
        print 'done...'
    if std_err:
        print std_err
    if rtn_code != 0:
        sys.exit(rtn_code)


if __name__ == '__main__':
    main()

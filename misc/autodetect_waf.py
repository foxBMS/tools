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

"""This script searches for waf in and returns its name if it machtes
r'waf-[0-9]{1,}.[0-9]{1,}.[0-9]{1,}'.

Default is searching in the current directory, but a directory can be specified
as argument
The search can be done recursive.
The waf file found is retured on stdout.
If waf can not be found (not the correct version, or no waf at all), the
script exits with 1 and writes some error message to stderr.
"""

import os
import sys
import argparse
import logging
import re
import glob

__version__ = 0.1
__date__ = '2018-01-12'
__updated__ = '2018-01-12'

def find_wafs(search_dir=os.getcwd(), recursive=False):
    """Checks for all files matching the waf file name convention
r'waf-[0-9]{1,}.[0-9]{1,}.[0-9]{1,}'.

    Args:
        search_dir
        recursive

    Returns:
        list of found waf files
    """
    # TODO: recursive search
    search_dir = os.path.realpath(search_dir)
    if recursive:
        recursive_place_holder = r'\**\\'
    else:
        recursive_place_holder = ''
    content_tools = glob.glob('{0}{1}{2}'.format(search_dir,recursive_place_holder,r'*waf*'))
    logging.info('Search directory: {}'.format(search_dir))
    logging.info('Search recursive: {}'.format(recursive))
    #content_tools = os.listdir(dir)
    version_regex = re.compile(r'^waf-[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,} *$')
    wafs_list = []
    waf_names = []
    for waf in content_tools:
        waf_name = os.path.split(waf)[1]
        if version_regex.match(waf_name):
            wafs_list.append(waf)
            waf_names.append(waf_name)
    if not wafs_list:
        logging.error('Could not find \'waf\'')
        sys.exit(1)
    return wafs_list, waf_names

def find_waf_version(wafs_list, waf_names, search_version='latest'):
    """Searches either the latest or the user specififed version of waf and
returns the waf file name
    Args:
        wafs_list:
        search_version:

    Returns:
        found waf file
    """
    logging.debug('Search waf version: {}'.format(search_version))
    try:
        latest = (waf_names[0])[4:]
    except IndexError as err:
        logging.error('Could not access waf list')
        sys.exit(1)

    l_major, l_minor, l_patch = latest.split('.')
    try:
        l_major = int(l_major)
        l_minor = int(l_minor)
        l_patch = int(l_patch)
    except ValueError as err:
        logging.error(err)
        sys.exit(1)
    
    latest_index = 0
    found = None
    for i, el in enumerate(waf_names):
        vers = el[4:]
        if search_version != 'latest':
            if search_version == vers:
                found = vers
                latest_index = i
        else:
            logging.debug('checking: {}'.format(vers))
            major, minor, patch = vers.split('.')

            try:
                major = int(major)
                minor = int(minor)
                patch = int(patch)
            except ValueError as err:
                logging.error(err)
                sys.exit(1)
            if major > l_major:
                latest = vers
                latest_index = i
            elif major == l_major:
                if minor > l_minor:
                    latest = vers
                    latest_index = i
                elif minor == l_minor:
                    if patch > l_patch:
                        latest = vers
                        latest_index = i
            l_major, l_minor, l_patch = latest.split('.')
            try:
                l_major = int(l_major)
                l_minor = int(l_minor)
                l_patch = int(l_patch)
            except ValueError as err:
                logging.error(err)
                sys.exit(1)
            found = latest

    if found is None:
        logging.error('Could not find waf version: {}'.format(search_version))
        sys.exit(1)

    waf_string = 'waf-{0} ({1})'.format(found, wafs_list[latest_index])

    return waf_string

def main():
    """Use google style docstrings
from http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html
    """
    program_name = os.path.basename(sys.argv[0])
    program_version = '{}'.format(__version__)
    program_build_date = str(__updated__)
    program_version_message = '{} {}'.format(
        program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split('\n\n')[0]
    program_license = '''{}

    Created by the foxBMS Team on {}.
    Copyright 2017 foxBMS. All rights reserved.

    Licensed under the BSD 3-Clause License.

    Distributed on an "AS IS" basis without warranties
    or conditions of any kind, either express or implied.

USAGE
'''.format(program_shortdesc, str(__date__))

    parser = argparse.ArgumentParser(
        description=program_license,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        '-v',
        '--verbosity',
        dest='verbosity',
        action='count',
        help='set verbosity level')
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=program_version_message)
    parser.add_argument(
        '-d',
        '--directory',
        default=os.getcwd(),
        help='[default:cwd]')
    parser.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        default=False,
        help='[default:False]')
    parser.add_argument(
        '-wv',
        '--wafversion',
        default='latest',
        help='Specfiy the waf version which should be search for [default:latest]')

    args = parser.parse_args()

    if args.verbosity is not None:
        if args.verbosity == 1:
            logging.basicConfig(level=logging.INFO)
        elif args.verbosity > 1:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.ERROR)

    search_dir = args.directory
    search_rec = args.recursive
    search_waf_version = args.wafversion

    wafs, waf_names = find_wafs(search_dir, search_rec)
    waf_version = find_waf_version(wafs, waf_names, search_waf_version)

    print(waf_version)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import argparse
import os
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--program', type=str,
                        help='program under test, the executable')
    parser.add_argument('-d', '--directories', action='append',
                        help='a directories of output to check error codes')
    parser.add_argument('-t', '--testcase', type=str,
                        help='a specifc testcase')

    args = parser.parse_args()

    for directory in args.directories:
        assert(os.path.exists(directory))


    program = os.path.abspath(args.program)
    directories = [os.path.abspath(d) for d in args.directories]
    handler(directories, program)

def handler(directories, ELF):
    seen_ret_code = set()
    for directory in directories:
        for crash_file in os.listdir(directory):
            crash = os.path.abspath(directory + '/' + crash_file)
            res = subprocess.run([ELF, crash, 'mnt'],
                                 capture_output=True)
            seen_ret_code.add(res.returncode)

            print(f"{crash} returns {res.returncode}")
    print(seen_ret_code)

if __name__ == '__main__':
    main()

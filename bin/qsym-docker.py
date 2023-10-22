#!/usr/bin/env python3

import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--afl', type=str,
                        help='afl-slave tag')
    parser.add_argument('-o', '--output', type=str,
                        help='fuzzing output directory')
    parser.add_argument('-p', '--program', type=str,
                        help='fuzzing program')
    args = parser.parse_args()

    cmdline = ['docker', 'run', '-it', '--rm',
               '--cap-add=SYS_PTRACE',
               '--volume', f'{os.path.abspath(args.output)}:/o',
               '--volume', f'{os.path.abspath(args.program)}:/program.exe',
               'qsym:latest',
               '/workdir/qsym/bin/run_qsym_afl.py',
               '-a', args.afl,
               '-o', '/o',
               '-n', 'qsym',
               '--', '/program.exe']

    cmdline = ' '.join(cmdline)
    print(cmdline)
    os.system(cmdline)

if __name__ == '__main__':
    main()

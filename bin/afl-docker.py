#!/usr/bin/env python3

import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
                        help='fuzzing input directory')
    parser.add_argument('-o', '--output', type=str,
                        help='fuzzing output directory')
    parser.add_argument('-p', '--program', type=str,
                        help='fuzzing program directory')
    parser.add_argument('-M', '--master', action='store_true',
                        help='set as master')
    parser.add_argument('-Q', '--qemu', action='store_true',
                        help='QEMU mode')
    parser.add_argument('-S', '--slave', type=str,
                        help='slave tag')

    args = parser.parse_args()

    assert(os.path.exists(args.input))
    assert(os.path.exists(args.output))
    assert(os.path.exists(args.program))


    cmdline = ['docker', 'run', '-it', '--rm',
               '--cap-add=SYS_PTRACE',
               '--volume', f'{os.path.abspath(args.program)}:/program.exe',
               '--volume', f'{os.path.abspath(args.input)}:/i',
               '--volume', f'{os.path.abspath(args.output)}:/o',
               'afl/afl-fuzz',
               '-m', '8192', '-i', '/i', '-o', '/o']


    if args.qemu:
        cmdline.append('-Q')
    if args.master:
        cmdline.append('-M')
        cmdline.append('afl-master00')
    else:
        if args.slave != None:
            cmdline.append('-S')
            cmdline.append(args.slave)

    cmdline.append('--')
    cmdline.append('/program.exe')

    cmdline = ' '.join(cmdline)
    print(cmdline)
    os.system(cmdline)

if __name__ == '__main__':
    main()

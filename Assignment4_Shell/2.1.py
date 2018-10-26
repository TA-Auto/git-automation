#!/usr/bin/python
import pexpect

child = pexpect.spawn('./shell')
child.sendline('help')
try:
    index = child.expect('test', timeout=2)
    print child.after
    print 'Expected output result:', index
except:
    print 'Failed matching expected output: \'help\''

# child.interact()
child.close()

print('Shell exit status: {0}'.format(child.exitstatus))
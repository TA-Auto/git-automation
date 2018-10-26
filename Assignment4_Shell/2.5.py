#!/usr/bin/python
import pexpect
import os
import time
import subprocess
HEADER = '\033[95m'
ENDC = '\033[0m'
passedTests = 0
failedTests = 0

child = pexpect.spawn('./shell')
pid = child.pid
print "Sleep test case, user should be able to input command after this"
child.sendline('sleep 2 &')
child.sendline('')
child.expect(b'\s*.*>.*\s*', timeout=2)
child.sendline('ps')
child.expect(b'\s*.*>.*\s*', timeout=2)
print child.after

# Wait approx until done
time.sleep(2)

print "Check after the task is done"
print "If it still showing defunc then it is not killed properly"
print "If it is still there without defunct then the process is not done"
child.sendline('ps')
# child.getecho()
# print child.after
child.expect('\s*.*>.*\s*', timeout=2)
print child.after
# child.interact()
print HEADER + "Testing the exit command" + ENDC
# proc = subprocess.Popen(['ps xao pid,comm| grep shell |awk \'{print $1}\''], stdout=subprocess.PIPE, shell=True)
proc = subprocess.Popen(['ps xao pid | grep ' + str(pid)], stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()

# print "PID: " + parent_op
if int(parent_op) == pid:
    print 'Shell alive before exit - success'
    passedTests += 1
else:
    print 'Shell not alive before exit - failed'
    failedTests += 1

child.sendline('exit')
child.expect(b'^((?!>).)*$', timeout=1)
print child.after

proc = subprocess.Popen(['ps xao pid | grep ' + str(pid)], stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()

# print "PID: " + str(pid)
if not parent_op:
    print 'Shell dead after exit - success'
    passedTests += 1
else:
    print 'Shell not dead after exit - failed'
    failedTests += 1

print "Test done"
child.close()
print('shell exit status: {0}'.format(child.exitstatus))
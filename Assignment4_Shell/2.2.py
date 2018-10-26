#!/usr/bin/python
import pexpect
import subprocess
import time
import psutil
# HEADER = '\033[95m'
# ENDC = '\033[0m'
HEADER = '\n>>>>> '
ENDC = ' <<<<<'
passedTests = 0
failedTests = 0

print HEADER + "Spawn the shell" + ENDC
child = pexpect.spawn('./shell')
pid = child.pid
try:
    child.expect('.*', timeout=2)
    print "spawn the shell - success"
    passedTests += 1
except:
    print "spawn the shell - failed"
    failedTests += 1

print HEADER + "Testing the help command" + ENDC
child.sendline('help')
try:
    child.expect('.*', timeout=2)
    print '\'help\' - success'
    passedTests += 1
except:
    print '\'help\' - failed'
    failedTests += 1

proc = subprocess.Popen(['cd .. ; pwd'], stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()

print HEADER + "Testing the cd to the upper folder command" + ENDC
child.sendline('cd ..')
try:
    child.expect(b'\s*.*>.*\s*', timeout=2)
    print '\'cd ..\' - success'
    passedTests += 1
except:
    print '\'cd ..\' - failed'
    failedTests += 1
print HEADER + "Testing the pwd command" + ENDC
child.sendline('pwd')
# Change the regex to test somewhere else
try:
    child.expect(b'\s*.*>.*\s*', timeout=2)
    # print child.after
    if parent_op in child.after:
        print '\'pwd\' - success'
        passedTests += 1
    else:
        print '\'pwd\' - failed \n{0} \n{1}'.format(child.after.replace('pwd', ''), parent_op)
        failedTests += 1
except:
    print '\'pwd\' failed'
    failedTests += 1

print HEADER + "Testing the pipe" + ENDC
proc = subprocess.Popen(['ps ' + str(pid) + ' | wc -l'],
                        stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()
child.sendline('ps ' + str(pid) + ' | wc -l')
try:
    child.expect(b'\s*.*>.*\s*', timeout=2)
    if parent_op in child.after:
        print "pipe command - success"
        passedTests += 1
    else:
        print "pipe - failed"
        failedTests += 1
    # print child.after
except:
    print "pipe - failed"
    failedTests += 1

print HEADER + "Testing the input redirection" + ENDC
proc = subprocess.Popen(['wc -l < /bin/bash'],
                        stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()
child.sendline('wc -l < /bin/bash')
try:
    child.expect(b'\s*.*>.*\s*', timeout=2)
    if parent_op in child.after:
        print "input redirection - success"
        passedTests += 1
    else:
        print "input redirection - failed"
        failedTests += 1
except:
    print "input redirection - failed"
    failedTests += 1

print HEADER + "Testing the output redirection" + ENDC
proc = subprocess.Popen(['lscpu > /tmp/shell'],
                        stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()
child.sendline('lscpu > /tmp/shell_test')
proc = subprocess.Popen(['comm -3 /tmp/shell /tmp/shell_test'],
                        stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()

try:
    child.expect(b'\s*.*>.*\s*', timeout=2)
    # if parent_op in child.after:
    if proc.returncode == 0:
        print "output redirection - success"
        passedTests += 1
    else:
        print "output redirection - failed"
        failedTests += 1
except:
    print "input redirection - failed"
    failedTests += 1

print HEADER + "Testing the pipe with redirection" + ENDC
proc = subprocess.Popen(
    ['cat /tmp/shell | wc -l > /tmp/shell_count'], stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()
child.sendline('cat /tmp/shell_test | wc -l > /tmp/shell_test_count')
proc = subprocess.Popen(['comm -3 /tmp/shell_count /tmp/shell_test_count'],
                        stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()
try:
    child.expect(b'\s*.*>.*\s*', timeout=2)
    # if parent_op in child.after:
    if proc.returncode == 0:
        print "pipe with redirection - success"
        passedTests += 1
    else:
        print "pipe with redirection - failed"
        failedTests += 1
except:
    print "pipe with redirection - failed"
    failedTests += 1

# clean the files
proc = subprocess.Popen(
    ['rm /tmp/shell /tmp/shell_count /tmp/shell_test /tmp/shell_test_count > /dev/null 2>&1'], stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()

print HEADER + "Testing the background" + ENDC
child.sendline('sleep 2 &')
# time.sleep(300)
proc = subprocess.Popen(['ps xao pid,ppid,cmd | grep -w ' + str(pid) + '| grep -w sleep | grep -v grep| awk \'{print $1}\''],
                        stdout=subprocess.PIPE, shell=True)
sleep_pid = proc.communicate()[0].strip()
# print sleep_pid
child.sendline('echo \"hi\"')
proc = subprocess.Popen(['echo \"hi\"'], stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()
# print parent_op
try:
    child.expect(b'\s*.*>.*\s*', timeout=2)
    # print child.after
    if parent_op in child.after:
        print "process sent to bg - success"
        passedTests += 1
    else:
        print "process sent to bg - failed"
        failedTests += 1
except:
    print "process sent to bg - failed"
    failedTests += 1

time.sleep(2)
if sleep_pid:
    proc = subprocess.Popen(['ps xao pid | grep -w ' + str(sleep_pid)],
                            stdout=subprocess.PIPE, shell=True)
    parent_op = proc.communicate()[0].strip()
else:
    parent_op = True

if not parent_op:
    print 'bg process completed and cleaned - success'
    passedTests += 1
else:
    print 'bg process completed and cleaned - failed'
    failedTests += 1

print HEADER + "Testing the exit with signal handler" + ENDC
# proc = subprocess.Popen(['ps xao pid,comm| grep shell |awk \'{print $1}\''], stdout=subprocess.PIPE, shell=True)
proc = subprocess.Popen(['ps xao pid | grep -w ' + str(pid)],
                        stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()

# print "PID: " + parent_op
# if int(parent_op) == pid:
if parent_op:
    print 'shell alive before SIGINT - success'
    passedTests += 1
else:
    print 'shell alive before SIGINT - failed'
    failedTests += 1

child.sendline('kill -2 ' + str(pid))
time.sleep(2)
proc = subprocess.Popen(['ps xao pid | grep -w ' + str(pid)],
                        stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()

if not parent_op:
    print 'interrupt signal SIGINT handled - success'
    passedTests += 1
else:
    try:
        p = psutil.Process(int(pid))
        if p.status == psutil.STATUS_ZOMBIE:
            print 'interrupt signal SIGINT handled - success'
            passedTests += 1
        else:
            print 'interrupt signal SIGINT handled - failed', p.status
            failedTests += 1
    except:
        print 'interrupt signal SIGINT handled - success'
        passedTests += 1

child.close()

child = pexpect.spawn('./shell')
pid = child.pid

print HEADER + "Testing the exit command" + ENDC
proc = subprocess.Popen(['ps xao pid | grep -w ' + str(pid)],
                        stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()

# print "PID: " + parent_op
# if int(parent_op) == pid:
if parent_op:
    print 'shell alive before exit - success'
    passedTests += 1
else:
    print 'shell not alive before exit - failed'
    failedTests += 1

child.sendline('exit')

proc = subprocess.Popen(['ps xao pid | grep -w ' + str(pid)],
                        stdout=subprocess.PIPE, shell=True)
parent_op = proc.communicate()[0].strip()

if not parent_op:
    print 'shell dead after exit - success'
    passedTests += 1
else:
    try:
        p = psutil.Process(int(pid))
        if p.status == psutil.STATUS_ZOMBIE:
            print 'shell dead after exit - success'
            passedTests += 1
        else:
            print 'shell dead after exit - failed', p.status
            failedTests += 1
    except:
        print 'shell dead after exit - success'
        passedTests += 1

child.close()
print ''
print '='*50
print "Test done - Passed: {0}, Failed: {1}".format(passedTests, failedTests)
print('shell exit status: {0}'.format(child.exitstatus))
print '='*50

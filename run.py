import os
import datetime 
import urllib.request
import base64
import json

os.system("python install_packages.py")

import pexpect
 

###################################################################################

ASSIGNMENT = "assignment4"
DEADLINE = "2018-08-29 17:00:00"

ORGS = 'Fall18Systems'
API_TOKEN = '<generated token>'
GIT_API_URL = 'https://api.github.com'
MYUSERNAME = ""
MYPASSWORD = ""

HOME = "/vagrant"
PROMPT = ".*>>>$"
###################################################################################



def get_repos(url):
    result = None
    request = urllib.request.Request(GIT_API_URL + url + '?per_page=200')
    base64string = base64.encodestring(('%s/token:%s' % (MYUSERNAME, API_TOKEN)).encode()).decode().replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    result = urllib.request.urlopen(request)
    data = result.read()
    encoding = result.info().get_content_charset('utf-8')
    res = json.loads(data.decode(encoding))
    result.close()
    return res

def get_tests(child):
    global PROMPT,HOME

    child.sendline("ls "+HOME+"/tests")
    child.expect(PROMPT)
    return " ".join(child.after.split("\r\n")[1:-1]).split()


def pull_git_repos(child):
    global PROMPT,CLONE_SCRIPT
    child.sendline("")


def get_git_repos(child):
    global PROMPT,HOME

    child.sendline(HOME+"/repos")
    child.expect(PROMPT)

    for r in get_repos:
        child.sendline('git clone https://' + MYUSERNAME + ':' + MYPASSWORD + '@github.com/' + ORGS + '/' + r['name']+" &\n\n")
        child.expect(PROMPT)

    # wait for all gitclones to complete
    while True:
        child.sendline('ps uax | grep "git clone" | grep -v "grep"')
        child.expect(PROMPT)
        if not " ".join(child.after.split("\r\n")[1:-1]).split():
            break

    child.sendline("ls ")
    child.expect(PROMPT)

    return " ".join(child.after.split("\r\n")[1:-1]).split()


def process_late_submission(child):
    global PROMPT,DEADLINE

    late_submission = "submitted in time"
    child.sendline("git log -n 1 --date=format:'%Y-%m-%d %H:%M:%S' | grep Date")
    child.expect(PROMPT)
    date = child.after.split("\r\n")[1].strip()
    sd = datetime.datetime.strptime(date.split(": ")[1].strip(),'%Y-%m-%d %H:%M:%S')
    dd = datetime.datetime.strptime(DEADLINE,'%Y-%m-%d %H:%M:%S')
    if sd > dd:
        late_submission = "submission delayed by : "+str(sd - dd)

    return late_submission
 
    
if __name__ == "__main__":
    child = pexpect.spawn("bash")
    child.sendline("export PS1='>>>'")
    child.expect(PROMPT)

    # cleanup workdir 
    child.sendline("rm -rf output")
    child.expect(PROMPT)
    child.sendline("mkdir output")
    child.expect(PROMPT)
    child.sendline("mkdir repos")
    child.expect(PROMPT)
    
    tests = get_tests()

    for repo in get_git_repos(child):
        print "Testing submission :",repo

        child.sendline("cd "+HOME+"/repos/"+repo+"/"+ASSIGNMENT)
        child.expect(PROMPT)
        output_file = HOME+"/output/"+repo+"_output.txt"
        child.sendline("touch "+output_file)
        ls = process_late_submission(child)
        child.sendline("echo '"+ls+"' >> "+output_file)
        child.expect(PROMPT)

        for test in tests:

            print " "*3,"Running",test
            child.sendline("echo '"+"="*50+"' >> "+output_file)
            child.expect(PROMPT)
            child.sendline("echo '"+test+"' >> "+output_file)
            child.expect(PROMPT)
            child.sendline("echo '"+"="*50+"' >> "+output_file)
            child.expect(PROMPT)
            child.sendline("python "+test+" >> "+output_file)
            child.expect(PROMPT)
            child.sendline("echo '"+"="*50+"' >> "+output_file)
            child.expect(PROMPT)
            child.sendline("echo '' >> "+output_file)
            child.expect(PROMPT)

    child.close()

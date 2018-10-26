import os

req_packages = ["pexpect"]



if __name__ == "__main__":
    if not os.popen("which pip 2>/dev/null").read().strip():
        os.system("sudo yum -y install python-pip")

    if not os.popen("which pip 2>/dev/null").read().strip():
        print "failed to install pip"
        exit(1)

    installed_packages = os.popen("pip freeze").read().strip()

    for package in req_packages:
        if package not in installed_packages:
            os.system("sudo pip install "+package)


    installed_packages = os.popen("pip freeze").read().strip()
    failed_to_install = []
    for package in req_packages:
        if package not in installed_packages:
            failed_to_install.append(package)

    if failed_to_install:
        print "failed to install the following package : ",",".join(failed_to_install)
        exit(1)



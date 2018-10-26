# CCIS Vagrant VM
Vagrant is a program that helps with provisioning of virtual machines (similar to docker's provisioning of containers).
CCIS has released a "Vagrantfile" that you can use to set up a virtual machine very similar to the environment running on CCIS linux machines (same release of CentOS, same kernel, same installed programs).

[CCIS Vagrant box](https://app.vagrantup.com/ccis/boxes/CentOS-7.4)

You can set it up by [installing Vagrant](https://www.vagrantup.com/docs/installation/) and then running the following commands in an empty directory.

```zsh
vagrant box add ccis/CentOS-7.4 --box-version 0.0.1
```
```zsh
vagrant init ccis/CentOS-7.4 --box-version 0.0.1
```
To start the VM, go back to that directory and run
```zsh
vagrant up
```
Then, to SSH to the virtual machine, run
```zsh
vagrant ssh
```
You can see if it is still running with
```zsh
vagrant status
```
And shut it down with
```zsh
vagrant halt
```

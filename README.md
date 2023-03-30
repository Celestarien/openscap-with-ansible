# openscap-with-ansible
A script that orchestrates OpenSCAP and Ansible


## Requirements

- Python 3.10 (minimum) : [This tutorial worked for me](https://tecadmin.net/how-to-install-python-3-10-on-debian-11/)
- Ansible
- OpenSCAP (need to be on all your machines and your self too)
- OpenSCAP SSH script ([More Informations](https://wiki.debian.org/UsingSCAP)) :  

  ```bash
  wget https://raw.githubusercontent.com/OpenSCAP/openscap/maint-1.2/utils/oscap-ssh
  chmod 0755 oscap-ssh
  ```
  The OpenSCAP SSH script **must be** in the same folder as this script

 - Security guide for your machines (I had trouble installing security guides for Debian 10 and 11, but [this tutorial](https://itnixpro.com/install-openscap-on-debian-11/) worked for me)

## Environment tested

- Debian 10

## Run

```
python3.10 main.py
```

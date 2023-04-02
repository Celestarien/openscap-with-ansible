# openscap-with-ansible
A script that orchestrates OpenSCAP and Ansible


## Requirements

- Ansible
- OpenSCAP (need to be on all your machines and your self too)
- OpenSCAP SSH script ([More Informations](https://wiki.debian.org/UsingSCAP)) :  

  ```bash
  wget https://raw.githubusercontent.com/OpenSCAP/openscap/maint-1.2/utils/oscap-ssh
  chmod 0755 oscap-ssh
  ```
  The OpenSCAP SSH script **must be** in the same folder as this script

## Environment tested

- Ubuntu 18.04

## Supported platforms

- [X] Linux
- [ ] Windows
- [ ] MacOS

## Run

```
./main_bash.sh
```

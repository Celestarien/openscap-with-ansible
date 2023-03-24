from os.path import exists
import subprocess


def check_hosts_file_exist():
    hosts_file_exists = exists('./hosts.txt')

    if not hosts_file_exists :
        print('Hosts file doesn\'t exist')
        print('Create hosts file')
        with open('./hosts.txt', 'w', encoding='utf-8') as hosts_file:
            hosts_file.write('Name|IP example|SSH user example|OS example|SSH private key path')
        print('Hosts file created')
        print('Edit hosts.txt and restart programm')
        exit()


def generate_ansible_hosts_file(host):
    name = str(host).split('|')[0]
    ip_adress = str(host).split('|')[1]
    ssh_key_path = str(host).split('|')[4]
    with open('./ansible_hosts', 'w', encoding='utf-8') as hosts_file_ansible :
        hosts_file_ansible.write(f"{name} ansible_host={ip_adress} ansible_ssh_private_key_file={ssh_key_path}")


def install_security_guides():
    print("""

    Which guides do you want to install ?

    1 - All
    2 - Debian guides
    3 - Debian-based distributions (e.g. Ubuntu) guides
    4 - Other distributions guides (RHEL, Fedora, etc.)
    5 - Application-oriented guides (Firefox, JBoss, etc.)

    """)
    choice = input('Enter a number : ')
    match choice:
        case '1':
            bashCommand = "apt install ssg-debian ssg-debderived ssg-nondebian ssg-applications"
        case '2':
            bashCommand = "apt install ssg-debian"
        case '3':
            bashCommand = "apt install ssg-debderived"
        case '4':
            bashCommand = "apt install ssg-nondebian"
        case '5':
            bashCommand = "apt install ssg-applications"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def audit_openscap(host):
    name = str(host).split('|')[0]
    ip_adress = str(host).split('|')[1]
    os = str(host).split('|')[3]
    ssh_user = str(host).split('|')[2]
    ssh_key_path = str(host).split('|')[4]
    profile_openscap = str(host).split('|')[5]
    type_eval = str(host).split('|')[6]

    # Add SSH key in var
    # bashCommand = f"export "
    # process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=True)
    # output, error = process.communicate()

    # Scan
    print('Scan and report')
    bashCommand = f"export SSH_ADDITIONAL_OPTIONS='-i {ssh_key_path}' && ./oscap-ssh {ssh_user}@{ip_adress} 22 {type_eval} eval --report report_{name}.html --profile {profile_openscap} /usr/share/xml/scap/ssg/content/ssg-{os}-{type_eval}.xml"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print(output)
    
    # Compliance
    bashCommand = f"oscap {type_eval} eval --profile {profile_openscap} --results report_{name}.xml /usr/share/xml/scap/ssg/content/ssg-{os}-{type_eval}.xml"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    # Ansible file
    bashCommand = f"oscap {type_eval} generate fix --fix-type ansible --profile {profile_openscap} --output remediation_{name}.yml report_{name}.xml"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


def apply_security_with_ansible(host):
    name = str(host).split('|')[0]
    ip_adress = str(host).split('|')[1]
    ssh_key_path = str(host).split('|')[4]
    with open('./ansible_hosts', 'w', encoding='utf-8') as hosts_file_ansible :
        hosts_file_ansible.write(f"""[servers]
{name} ansible_host={ip_adress} ansible_ssh_private_key_file={ssh_key_path}

[all:vars]
ansible_python_interpreter=/usr/bin/python3
""")
    bashCommand = f"ansible-playbook remediation_{name}.yml -i ansible_hosts"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()


if __name__ == '__main__':

    while True :
        check_hosts_file_exist()

        with open('./hosts.txt', 'r') as hosts_file:
            hosts = hosts_file.readlines()
            count_hosts = len(hosts)
        
        print(f"""

        What do you want to do ?

        1 - Audit with OpenSCAP
        2 - Apply security measures with Ansible
        3 - Install security guides

        4 - Exit

        Host(s) found : {count_hosts}
        """)
        choice = input('Enter a number : ')
        match choice:
            case '1':
                for host in hosts :
                    audit_openscap(host)
            case '2':
                for host in hosts :
                    apply_security_with_ansible(host)
            case '3':
                install_security_guides()
            case '4' :
                exit()


    # # Ansible
    # with open('./ansible_hosts', 'w', encoding='utf-8') as hosts_file_ansible :
    #     hosts_file_ansible.write("[servers]\n")
    # for host in hosts:
    #     generate_ansible_hosts_file(host)
    # with open('./ansible_hosts', 'w', encoding='utf-8') as hosts_file_ansible :
    #     hosts_file_ansible.write("""
    #     """)

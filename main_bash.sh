#!/bin/bash

check_hosts_file_exist() {
    if [ ! -f "./hosts.txt" ]; then
        echo "Hosts file doesn't exist"
        echo "Create hosts file"
        echo "Name|IP example|SSH user example|OS example|SSH private key path" > ./hosts.txt
        echo "Hosts file created"
        echo "Edit hosts.txt and restart programm"
        exit
    fi
}

generate_ansible_hosts_file() {
    local host=$1
    local name=$(echo $host | cut -d '|' -f1)
    local ip_address=$(echo $host | cut -d '|' -f2)
    local ssh_key_path=$(echo $host | cut -d '|' -f5)
    echo "[servers]" > ./ansible_hosts
    echo "$name ansible_host=$ip_address ansible_ssh_private_key_file=$ssh_key_path" >> ./ansible_hosts
    echo "" >> ./ansible_hosts
    echo "[all:vars]" >> ./ansible_hosts
    echo "ansible_python_interpreter=/usr/bin/python3" >> ./ansible_hosts
}

install_security_guides () {
    cat <<EOM

    Which guides do you want to install?

    1 - All
    2 - Debian guides
    3 - Debian-based distributions (e.g. Ubuntu) guides
    4 - Other distributions guides (RHEL, Fedora, etc.)
    5 - Application-oriented guides (Firefox, JBoss, etc.)

EOM
    read -p "Enter a number: " choice

    case $choice in
        1)
            bashCommands=( "apt install ssg-debian ssg-debderived ssg-nondebian ssg-applications" )
            ;;
        2)
            bashCommands=( "apt install ssg-debian" "wget http://ftp.us.debian.org/debian/pool/main/s/scap-security-guide/ssg-debian_0.1.65-1_all.deb && apt install ./ssg-debian_0.1.65-1_all.deb" )
            ;;
        3)
            bashCommands=( "apt install ssg-debderived" )
            ;;
        4)
            bashCommands=( "apt install ssg-nondebian" )
            ;;
        5)
            bashCommands=( "apt install ssg-applications" )
            ;;
        *)
            echo "Invalid input"
            exit 1
            ;;
    esac

    for bashCommand in "${bashCommands[@]}"; do
        eval "$bashCommand"
    done
}

audit_openscap() {
    local host=$1
    local name=$(echo $host | cut -d '|' -f1)
    local ip_address=$(echo $host | cut -d '|' -f2)
    local os=$(echo $host | cut -d '|' -f4)
    local ssh_user=$(echo $host | cut -d '|' -f3)
    local ssh_key_path=$(echo $host | cut -d '|' -f5)
    local profile_openscap=$(echo $host | cut -d '|' -f6)
    local type_eval=$(echo $host | cut -d '|' -f7)

    echo "Creating a report for $name"
    export SSH_ADDITIONAL_OPTIONS="-i $ssh_key_path"
    ./oscap-ssh $ssh_user@$ip_address 22 $type_eval eval --report report_$name.html --profile $profile_openscap /usr/share/scap-security-guide/ssg-$os-$type_eval.xml

    echo "Production of a compliance check report for $name"
    oscap $type_eval eval --profile $profile_openscap --results report_$name.xml /usr/share/scap-security-guide/ssg-$os-ds.xml

    echo "Creating the ansible file for $name"
    oscap $type_eval generate fix --fix-type ansible --profile $profile_openscap --output remediation_$name.yml report_$name.xml

}

apply_security_with_ansible () {
    name=$(echo "$1" | cut -d'|' -f1)
    ip_address=$(echo "$1" | cut -d'|' -f2)
    ssh_key_path=$(echo "$1" | cut -d'|' -f5)
    cat > ./ansible_hosts <<EOF
[servers]
$name ansible_host=$ip_address ansible_ssh_private_key_file=$ssh_key_path

[all:vars]
ansible_python_interpreter=/usr/bin/python3
EOF
    echo "Apply security measures with Ansible $name..."
    ansible-playbook remediation_${name}.yml -i ansible_hosts
    echo "$name : Success"
}


while true; do
    check_hosts_file_exist

    hosts=$(cat ./hosts.txt)
    count_hosts=$(echo "$hosts" | wc -l)

    cat <<EOM

    What do you want to do?

    1 - Audit with OpenSCAP
    2 - Apply security measures with Ansible
    3 - Install security guides
    4 - Exit

    Host(s) found: $count_hosts

EOM

    read -p "Enter a number: " choice

    case $choice in
        1)
            for host in $hosts; do
                audit_openscap "$host"
            done
            ;;
        2)
            for host in $hosts; do
                apply_security_with_ansible "$host"
            done
            ;;
        3)
            install_security_guides
            ;;
        4)
            exit 0
            ;;
        *)
            echo "Invalid input"
            ;;
    esac

done

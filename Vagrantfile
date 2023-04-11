# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box_download_insecure=true
  config.vm.define "web1" do |w1|#Website 1
    w1.vm.box = "ubuntu/bionic64"
    w1.vm.network "private_network", ip: "192.168.10.21"
    w1.vm.hostname = "web1"
    w1.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
    end
  end

  config.vm.define "web2" do |w2|#Website 2
    w2.vm.box = "generic/debian10"
    w2.vm.network "private_network", ip: "192.168.10.22"
    w2.vm.hostname = "web2"
    w2.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
    end
  end

  # config.vm.define "data" do |db|#Database for web1 and web2
  #   db.vm.box = "ubuntu/bionic64"
  #   db.vm.network "private_network", ip: "192.168.10.13"
  #   db.vm.hostname = "data"
  #   db.vm.provider "virtualbox" do |vb|
  #     vb.memory = "512"
  #   end
  # end

  # config.vm.define "rproxy" do |r|#Reverse-proxy
  #   r.vm.box = "ubuntu/bionic64"
  #   r.vm.network "private_network", ip: "192.168.5.5"
  #   r.vm.hostname = "rproxy"
  #   r.vm.provider "virtualbox" do |vb|
  #     vb.memory = "512"
  #   end
  # end

  config.vm.define "wazuh1" do |wa1|#IDS/IPS Indexer
    wa1.vm.box = "ubuntu/bionic64"
    wa1.vm.network "private_network", ip: "192.168.10.11"
    wa1.vm.hostname = "wazuhi"
    wa1.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.cpus = 2
    end
  end

  config.vm.define "wazuh2" do |wa2|#IDS/IPS Server
    wa2.vm.box = "ubuntu/bionic64"
    wa2.vm.network "private_network", ip: "192.168.10.12"
    wa2.vm.hostname = "wazuhs"
    wa2.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end
  end

  config.vm.define "wazuh3" do |wa3|#IDS/IPS Dashboard
    wa3.vm.box = "ubuntu/bionic64"
    wa3.vm.network "private_network", ip: "192.168.10.13"
    wa3.vm.hostname = "wazuhd"
    wa3.vm.provider "virtualbox" do |vb|
      vb.memory = "4096"
      vb.cpus = 2
    end
  end
#  config.vm.define "pfsense" do |pf|#Firewall
#    pf.vm.box = "kennyl/pfsense"
#    pf.vm.box_version = "2.4.0"
#    pf.vm.network "private_network", ip: "192.168.5.4"
#    pf.vm.provision "shell", run: "always", inline: "route add default gw 192.168.5.2"
#    pf.vm.network "private_network", ip: "192.168.10.4"
#    pf.vm.hostname = "pfsense"
#    pf.vm.provider "virtualbox" do |vb|
#      vb.memory = "1024"
#    end
#  end

  config.vm.define "client1" do |c1|#client 1
    c1.vm.box = "ubuntu/bionic64"
    c1.vm.network "private_network", ip: "192.168.10.31"
    c1.vm.hostname = "client1"
    c1.vm.provider "virtualbox" do |vb|
      vb.memory = "256"
    end
  end

  config.vm.define "admin" do |a|#admin
    a.vm.box = "ubuntu/bionic64"
    a.vm.network "private_network", ip: "192.168.10.51"
    a.vm.hostname = "admin"
    a.vm.provider "virtualbox" do |vb|
      vb.memory = "512"
    end
  end
end
# -*- mode: ruby -*-
# vi: set ft=ruby :
# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.

    # Habilita la venta de visualización.
    # config.vm.provider :virtualbox do |vb|
    # vb.gui = true
    # end

  config.vm.box = "centos/7"
  config.vm.box_version = "1809.01"
  config.vm.synced_folder  "provisioning" , "/vagrant"

  
  config.vm.define "nodo1" do |nodo1|
    
        
            nodo1.vm.network :forwarded_port, guest: 4201, host: 4201
            nodo1.vm.network :forwarded_port, guest: 4198, host: 4198
        
        nodo1.vm.network "private_network", ip: "172.24.1.253", virtualbox__intnet: true
    
  end
  
  config.vm.define "nodo2" do |nodo2|
    
        
            nodo2.vm.network :forwarded_port, guest: 4202, host: 4202
            nodo2.vm.network :forwarded_port, guest: 4197, host: 4197
        
        nodo2.vm.network "private_network", ip: "172.24.3.253", virtualbox__intnet: true
    
  end
  
  config.vm.define "nodo3" do |nodo3|
    
        
            nodo3.vm.network :forwarded_port, guest: 4203, host: 4203
            nodo3.vm.network :forwarded_port, guest: 4196, host: 4196
        
        nodo3.vm.network "private_network", ip: "172.24.3.252", virtualbox__intnet: true
    
  end
  

  
  config.vm.define "router" do |router|
    
        
            router.vm.network :forwarded_port, guest: 4200, host: 4200
            router.vm.network :forwarded_port, guest: 4199, host: 4199
        
        router.vm.network "private_network", ip: "172.24.1.2", virtualbox__intnet: true
    
        
        router.vm.network "private_network", ip: "172.24.3.2", virtualbox__intnet: true
    
    
        router.vm.provision "ansible" do |ansible|
              ansible.playbook       = "provisioning/playbook.yml"
              ansible.limit          = "all"
              ansible.become = true
              ansible.groups = {
                "nodes" => ["nodo1","nodo2","nodo3"],
                "routers" => ["router"]
              }
              ansible.host_vars = {
                
                "nodo1" => {"gateway" => "172.24.1.2",
                                 "ip" => "172.24.1.253",
                                 "puerto" => "4201",
                                 "puerto_mosquitto" => "4198"},
                
                "nodo2" => {"gateway" => "172.24.3.2",
                                 "ip" => "172.24.3.253",
                                 "puerto" => "4202",
                                 "puerto_mosquitto" => "4197"},
                
                "nodo3" => {"gateway" => "172.24.3.2",
                                 "ip" => "172.24.3.252",
                                 "puerto" => "4203",
                                 "puerto_mosquitto" => "4196"},
                
                
                "router" => {"gateway" => "172.24.1.2",
                                 "ip" => "172.24.1.2",
                                 "puerto" => "4200",
                                 "puerto_mosquitto" => "4199"}
                

              }

        end
    
  end
  


  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false


  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
  #   vb.memory = "1024"
  # end
  #
  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL
end
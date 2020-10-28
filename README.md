[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/emilgaripov/nornir-hands-on-lab)
# Nornir hands-on lab
When interacting with a new network, we need a way to automatically configure all network devices. And the Nornir framework can help solve this problem.
Nornir framework is fully written in the Python programming language and is intended for use with Python.

# Note: 
Please note that below scripts/libraries or configurations are for learning purposes only, do not use them in production environment.

# Dependencies
```
pip3 install nornir"<3"
```

# Introduction:
We will need to generate a configuration template according to the lab work described below using the Nornir framework(version2!) and apply the configuration to network devices(switches).
Conditions of hands-on lab:

1.	On SW1, the interfaces eth0/1, eth0/2, eth0/3, eth1/0 should be in access mode in such VLANs respectively: 10, 20, 30, 40.
2.	On SW2: the eth0/2 interface should be in VLAN 20 access mode. 
3.	On SW3: the eth0/2 interface should be added in VLAN 30 access mode. 
4.	On SW4: the eth0/2-3 interface should be added to VLAN 40 access mode.
5.	On SW2 ports connected to SW1 must be in "desired" trunk creation mode.
6.	On SW1, the ports connected to SW2 must be in manual trunk creation mode.
7.	On SW3 ports connected to SW1 must be in manual trunk creation mode.
8.	The ports between SW4 and SW1 must be in manual trunk creation mode and removed dtp.
9.	On all trunk ports VLAN 108 should be transmitted untagged.
10.	On SW1 create interface vlan 20 with ip address 10.10.20.10/24, interface vlan 30 with ip address 10.10.30.10/24 and interface vlan 40 with ip address  10.10.40.10/24.
11.	On SW2 create interface vlan 20 with ip address 10.10.20.20/24.
12.	On SW3 create interface vlan 30 with ip address 10.10.30.30/24. 
13.	On SW4 create interface vlan 40 with ip address 10.10.40.40/24.
14.	On SW1 allow only those VLANs to be transmitted in trunks which are configured on other switches.
15.	After applying the configuration on network devices send ping from SW1 to ip address 255.255.255.255. All IP addresses configured on the switches should answer to the ping.

# Topology
![topology](https://github.com/emilgaripov/nornir_workshop/blob/master/topology.png)

# Rendering configuration in Nornir using Jinja2.
Jinja2 is a modern, user-friendly, full-featured template creation language for Python. Two configuration templates are used in this lab work.  These are hostnames.j2 and interfaces.j2, each of which will create configurations for hostname and device interfaces respectively. 

They are located in the "templates" directory.

The hostnames.j2 template looks like this:
```jinja2
{% for hostname in host["about"] %}
hostname {{the hostname.caption }}.
{% endfor %}
```
The part of interfaces.j2 template looks like this:
```jinja2
{% for interface in host["interfaces"] %}
interface {{ interface.name }}{{ interface.port_slot }}
{% if interface.unused is defined %}
shutdown
{% elif interface.vlan is defined %}
switchport mode {{ interface.mode }}
switchport access vlan {{ interface.vlan }}
no shutdown
{% elif interface.allowed_vlan is defined and interface.negotiation is defined %}
switchport trunk allowed vlan {{ interface.allowed_vlan }}
switchport trunk encapsulation {{ interface.encapsulation }}
switchport trunk native vlan {{ interface.native_vlan }}
switchport mode {{ interface.mode }}
switchport {{ interface.negotiation }}
no shutdown
```

The "Text" plugin is responsible for using Jinja templates in Nornir. The function "text.template_file" is used in this lab work. It renders the file data in the file "hosts.yaml" and converts the inventory data in this file into configuration using the template file.

The part of the code responsible for this task looks like this:
```python
def hostname_config(task):
    var = task.run(task=text.template_file,
                   name="Switches hostname configuration",
                   template="hostnames.j2",
                   path="templates")
    task.host["hostname_config"] = var.result    task.run(task=networking.netmiko_send_config,
             name="Configure hostname on the device",
             config_commands=task.host["hostname_config"],)
```

As a result of running this part of the code, the «hostname» will be configured for all devices.
![hostname](https://github.com/emilgaripov/nornir_workshop/blob/master/hostname.png)

The following part of the code is responsible for configuring the interfaces of network devices.
```python
def interfaces_config(task):
    var = task.run(task=text.template_file,
                   name="Switches interface configuration",
                   template="interfaces.j2",
                   path="templates")    task.host["interfaces_config"] = var.result
    task.run(
    task=networking.netmiko_send_config,
    name="Loading Configuration on the device",
    config_commands=task.host["interfaces_config"].splitlines())
```
As a result of running this part of the code, the interfaces will be configured for all devices according to conditions of laboratory work.



The following part of the code is responsible for sending ping from SW1 to ip address 255.255.255.255
```python
def send_ping(task):
task.run(
task=networking.netmiko_send_command, delay_factor=2, 
max_loops=500,
command_string='ping 255.255.255.255',
name="Sending Ping on the device")
```
As a result of running this part of the code, the ping will be sent to all devices.
[ping](https://github.com/emilgaripov/nornir_workshop/blob/master/ping.png) 

# How to Use

1. Clone the repo
```
git clone https://github.com/emilgaripov/nornir-hands-on-lab
```
2. cd into directory
```
cd nornir-hands-on-lab/device_configuration
```
3. Run the script by typing ```python3 devices_config.py``` and the script will execute. 

# About me
My name is Emil Garipov - Network automation enthusiast, teacher, pythonist, Cisco Champion 2020.
# Contact
[Twitter](https://twitter.com/gissarsky)

[LinkedIn](https://www.linkedin.com/in/garipov/)


from nornir import InitNornir
nr = InitNornir(config_file="config.yaml")
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
results = nr.run(netmiko_send_command, command_string = 'sh ip int brief')
print_result(results)
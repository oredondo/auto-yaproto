#!/usr/bin/env python
#
# sample vagrant configuration ( as in vagrantfile_config.py )
# vagrant_config = {
#     # Every Vagrant virtual environment requires a box to build off of.
#     # this is the name of that box.
#     'vm_box': 'precise64',
#     # The url from where the 'config.vm.box' box will be fetched if it
#     # doesn't already exist on the user's system.
#     'vm_box_url': 'http://files.vagrantup.com/precise64.box',
#     'vms': {
#         'core': {
#             'ip': '172.16.90.11',
#             'hostnames': {
#                 'primary': 'aci-vagrant-core',
#                 'others': ['aci-vagrant-core.example.com'],
#             },
#             'port_forwarding': [
#                 # (guest_port, host_port) pairs
#                 # where host_port on the host is forwarded to the guest_port on the guest vm
#                 (80, 8081),
#                 (8080, 8082),
#             ],
#         },
#         'core2': {
#             'ip': '172.16.90.13',
#             'hostnames': {
#                 'primary': 'aci-vagrant-core2',
#                 'others': ['aci-vagrant-core2.example.com'],
#             },
#             'port_forwarding': [
#                 (80, 8083),
#                 (8080, 8084),
#             ],
#         },
#         'services': {
#             'ip': '172.16.90.12',
#             'hostnames': {
#                 'primary': 'aci-vagrant-services',
#                 'others': ['aci-vagrant-services.example.com'],
#             },
#             'port_forwarding': [
#                 # (guest_port, host_port) pairs
#                 # where host_port on the host is forwarded to the guest_port on the guest vm
#                 (80, 8085),
#             ],
#         },
#         'services2': {
#             'ip': '172.16.90.14',
#             'hostnames': {
#                 'primary': 'aci-vagrant-services2',
#                 'others': ['aci-vagrant-services.example.com'],
#             },
#             'port_forwarding': [
#                 (80, 8086),
#             ],
#         },
#     },
# }

import os

import jinja2


class GenerateVagrantFile(object):

    def __init__(self, template_path='Vagrantfile.j2', vagrantfile_path='Vagrantfile', config=None):
        self.__generate_vagrantfile(template_path, vagrantfile_path, config)

    def __load_template(self, template_path):
        return (jinja2.Environment(autoescape=True,
                                   loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
                .get_template(template_path))

    def __generate_vagrantfile(self, template_path, vagrantfile_path, config):
        file = open(vagrantfile_path, 'w+')
        file.write(self.__load_template(template_path).render(config))
        file.close()

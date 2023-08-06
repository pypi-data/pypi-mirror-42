# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dhcpdoctor']

package_data = \
{'': ['*']}

install_requires = \
['scapy>=2.4,<3.0']

entry_points = \
{'console_scripts': ['dhcpdoctor = dhcpdoctor.dhcpdoctor:main']}

setup_kwargs = {
    'name': 'dhcpdoctor',
    'version': '0.1.0',
    'description': 'Tool for testing IPv4 and IPv6 DHCP services',
    'long_description': '# dhcpdoctor\n\nTool for testing IPv4 and IPv6 DHCP services\n\n![Logo](logo.png)\n\n## Description\n\ndhcpdoctor sends DHCP requests and checks if it gets an offer from DHCP server.\nIt supports BOOTP+DHCP for IPv4 (`-4`) and DHCPv6 for IPv6 (`-6`).\n\nIt can operate as a DHCP client by sending requests on the local network via\nbroadcast/multicast or as a DHCP clent and relay in one tool by unicasting\nrequests to the specified IP address (`-s`). When relaying requests you can\nspecify the relay address to send from (`-f`). By default the IP address of\nthe interface request is sent from is used. When specifying custom relay from\naddress, keep in mind that the DHCP server will send the response back to the\naddress you specify here, so it must be an address on the machine you are\nrunning tests from.\n\nYou can specify a custom client MAC or DUID (`-c`). By default the MAC address\nof the interface to send request from is used.\n\nYou can specify the interface to send requests from with `-i`.\n\nProgram output and exit codes are Nagios/Icinga [compatible](https://nagios-plugins.org/doc/guidelines.html). Response time from DHCP server is measured and returned as performance data.\n\n## Requirements\n\nThis tool uses [scapy](https://scapy.net/) under the hood to craft, dissect, send and receive packets. Because of this it needs root permissions to run.\n\n## Developing\n\nWe use [poetry](https://poetry.eustace.io/) to manage Python dependencies and virtual environments.\n',
    'author': 'Matej Vadnjal',
    'author_email': 'matej.vadnjal@arnes.si',
    'url': 'https://github.com/ArnesSI/dhcpdoctor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)

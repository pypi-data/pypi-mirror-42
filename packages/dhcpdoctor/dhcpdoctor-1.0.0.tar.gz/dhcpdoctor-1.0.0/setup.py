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
    'version': '1.0.0',
    'description': 'Tool for testing IPv4 and IPv6 DHCP services',
    'long_description': '# dhcpdoctor\n\nTool for testing IPv4 and IPv6 DHCP services\n\n![Logo](logo.png)\n\n## Description\n\ndhcpdoctor sends DHCP requests and checks if it gets an offer from DHCP server.\nIt supports BOOTP+DHCP for IPv4 (`-4`) and DHCPv6 for IPv6 (`-6`).\n\nIt can operate as a DHCP client by sending requests on the local network via\nbroadcast/multicast or as a DHCP client and relay in one tool by unicasting\nrequests to the specified IP address (`-s`). When relaying requests you can\nspecify the relay address to send from (`-f`). By default the IP address of\nthe interface request is sent from is used. When specifying custom relay from\naddress, keep in mind that the DHCP server will send the response back to the\naddress you specify here, so it must be an address on the machine you are\nrunning tests from.\n\nYou can specify a custom client MAC or DUID (`-c`). By default the MAC address\nof the interface to send request from is used.\n\nYou can specify the interface to send requests from with `-i`.\n\nProgram output and exit codes are Nagios/Icinga [compatible](https://nagios-plugins.org/doc/guidelines.html). Response time from DHCP server is measured and returned as performance data.\n\n## Requirements\n\ndhcpdoctor needs needs Python 3.4 or later to run.\n\nSince it uses [scapy](https://scapy.net/) under the hood to craft, dissect, send and receive packets, it needs root permissions to run.\n\n## Installing\n\nVia pip:\n\n```\npip install dhcpdoctor\n```\n\n## Icinga2 check command\n\nYou can use dhcpdoctor as a check command from Icinga2 or Nagios.\n\nThere is [dhcpdoctor.conf](dhcpdoctor.conf) config with a CheckCommand definition\nfor Icinga2 you can use. A service that uses this check command might look like\nthis:\n\n```\napply Service "dhcpd6" {\n    import "generic-service"\n    check_command = "dhcpdoctor"\n    vars.dhcpdoctor_ipv6 = true\n    vars.dhcpdoctor_client_id = "00:11:11:11:11:11"\n    assign where host.dhcpd6\n}\n```\n\nIf you are building an RPM from provided [SPEC](dhcpdoctor.spec) file, the\nCheckCommand config will be installed to\n`/etc/icinga2/conf.d/check_commands/dhcpdoctor.conf`.\n\n## Developing\n\nWe use [poetry](https://poetry.eustace.io/) to manage Python dependencies and virtual environments.\n\nTo setup development virtual environment:\n\n```\npoetry install\n```\n\nRun the tool:\n\n```\npoetry run dhcpdoctor -h\n```\n\n[Vagrant](https://www.vagrantup.com/) can be used to quickly spin-up VMs with \nDHCP servers to test against:\n\n```\nvagrant up\nvagrant ssh dhcpdoctor\ncd /vagrant\npoetry run dhcpdoctor -h\nexit\nvagrant destroy\n```\n\nSee comments in [Vagrantfile](Vagrantfile) for more information.\n\n## Releases\n\n```\npoetry run bumpversion patch\n```\n\nInstead of patch you can give `minor` or `major`.\nThis creates a commit and tag. Make sure to push it with `git push --tags`.\n\nThe `dev-version.sh` script will bump the version for development or release as\nneeded (based on whether we are on a git tag or not) and is called in CI jobs.\n\n## Building\n\nHere is how to build `dhcpdoctor` using pyinstaller into a single binary file\nand then package that into a RPM for Red-Hat based systems. The resulting\nbinary is setuid root, because `dhcpdoctor` needs to work on privileged UDP\nports, but is usually run as a special user when invoked from Nagios or Icinga.\n\n```\npip3 install --upgrade bumpversion poetry pyinstaller\npoetry install --no-dev\npoetry run pip freeze | grep -v egg=dhcpdoctor > requirements.txt\npip3 install -r requirements.txt\n./dev-version.sh\n./build.sh\n```\n',
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

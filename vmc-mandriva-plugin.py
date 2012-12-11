# -*- coding: utf-8 -*-
# Copyright (C) 2006-2007  Vodafone España, S.A.
# Author:  Pablo Martí
# Mandriva adaptions: Buchan Milne
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""Mandriva OSPlugin"""
__version__ = "$Rev: 1179 $"

import re

from twisted.python.procutils import which

from vmc.common.oses import LinuxPlugin
from vmc.utils.utilities import get_file_data

mandriva_customization = {
    'WVDIAL_CONN_SWITCH' : '--config',
    'gksudo_name' : 'gksu',
}

DEFAULT_TEMPLATE = """
debug
noauth
name wvdial
noipdefault
nomagic
usepeerdns
ipcp-accept-local
ipcp-accept-remote
nomp
noccp
nopredictor1
novj
novjccomp
nobsdcomp"""

PAP_TEMPLATE = DEFAULT_TEMPLATE + """
refuse-chap
refuse-mschap
refuse-mschap-v2
refuse-eap
"""

CHAP_TEMPLATE = DEFAULT_TEMPLATE + """
refuse-pap
"""

TEMPLATES_DICT = {
    'default' : DEFAULT_TEMPLATE,
    'PAP' : PAP_TEMPLATE,
    'CHAP' : CHAP_TEMPLATE,
}

class MandrivaBasedDistro(LinuxPlugin):
    """
    OSPlugin for Mandriva-based distros
    """
    os_name = re.compile("Mandriva")
    os_version = None
    customization = mandriva_customization
   
    #XXX: Almost duplicated code with Suse plugin
    def get_timezone(self):
        timezone_re = re.compile('ZONE=(?P<tzname>[\w/]+)')
        sysconf_clock_file = get_file_data('/etc/sysconfig/clock')
        search_dict = timezone_re.search(sysconf_clock_file).groupdict()
        return search_dict['tzname'] or None
 
    def get_connection_args(self, dialer):
        assert dialer.binary == 'wvdial'
        
        if not self.privileges_needed:
            return [dialer.bin_path, self.abstraction['WVDIAL_CONN_SWITCH'],
                    dialer.conf_path, 'connect']
        
        gksudo_name = self.abstraction['gksudo_name']
        gksudo_path = which(gksudo_name)[0]
        args = [dialer.bin_path, self.abstraction['WVDIAL_CONN_SWITCH'],
                dialer.conf_path, 'connect']
        return [gksudo_path, '-g', " ".join(args)]
    
    def get_disconnection_args(self, dialer):
        assert dialer.binary == 'wvdial'
        
        killall_path = which('killall')[0]
        if not self.privileges_needed:
            return [killall_path, 'pppd', 'wvdial']
        
        gksudo_name = self.abstraction['gksudo_name']
        gksudo_path = which(gksudo_name)[0]
        args = " ".join([killall_path, 'pppd', 'wvdial'])
        return [gksudo_path, '-g', args]

    def get_config_template(self, dialer_profile):
        return TEMPLATES_DICT[dialer_profile]

mandriva = MandrivaBasedDistro()

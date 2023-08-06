import os
import re
import subprocess

from . import settings
from .smartdata import SmartDataParser
from .hdparm import HdparmParser

__author__ = 'osso'


class HDDDock(object):

    def __init__(self, disk_name):
        self.disk_name = disk_name
        self.status = 'Initialized'
        self._smart_data_parser = SmartDataParser(disk_name)
        self._smart_data = self.get_smart_data()
        self._info = self.get_information_from_smart_data(self._smart_data)
        self.port = self.get_port()
        self.docktool_bay_nr = self.get_docktool_bay_nr()

    def is_sas(self):
        return 'sas' in self._info.get('Transport protocol', '').lower()

    def get_docktool_bay_nr(self):
        return settings.ATA_TO_BAY_NR.get(self.port, None)

    def get_port(self):
        if hasattr(self, 'port'):
            return self.port

        path = '/dev/disk/by-path/'
        port = None
        found_symlinks = [
            x for x in os.listdir(path)
            if (os.path.islink(os.path.join(path, x)) and
                ('../../{}'.format(self.disk_name) ==
                 os.readlink(os.path.join(path, x))))]
        if found_symlinks:
            assert len(found_symlinks) == 1
            for regex in [r'(ata-[0-9])+', r'(usb-[0-9])+']:
                match = re.search(regex, found_symlinks[0])
                if match:
                    port = match.groups()[0]
                    break

        return port or self.disk_name

    @property
    def smart_data_parser(self):
        return self._smart_data_parser

    def is_ssd(self):
        return 'solid state' in self._info.get('Rotation Rate', '').lower()

    def get_smart_data(self):
        return self.smart_data_parser.smart_data

    def get_information_from_smart_data(self, smart_data):
        return self.smart_data_parser.information

    def do_hdparm(self, action, secret):
        subprocess.check_output(
            ['/sbin/hdparm',
             '--user-master', 'u',
             action, secret,
             '/dev/{0}'.format(self.disk_name)])

    def hdparm_security_info(self):
        hdparm_parser = HdparmParser(self.disk_name)
        return hdparm_parser.get_security_info()

    def can_secure_erase_ssd(self):
        if not self.is_ssd():
            return False, 'Disk was not recognized as a Solid State Device'

        security_info = self.hdparm_security_info()

        for x in ['supported', 'enabled', 'locked', 'frozen']:
            if x not in security_info:
                return False, '{0} not found in security_info: {1}'.format(
                    x, security_info)

        if not security_info['supported']:
            return False, 'SSD secure erase seems not to be supported'

        if security_info['enabled']:
            return False, 'SSD password for secure erase is already set.'

        if security_info['locked']:
            return False, (
                'SSD is locked (try replugging the disk or '
                'hibernating system)')

        if security_info['frozen']:
            return False, (
                'SSD is frozen (try replugging the disk or '
                'hibernating system)')

        return True, None

    def secure_erase_ssd(self):
        # s1 = /dev/sdc
        # secret=`pwgen -s 32 1`
        # hdparm --user-master u --security-set-pass $secret $1
        # hdparm --user-master u --security-erase $secret $1

        if not settings.DEBUG:
            can_erase, error = self.can_secure_erase_ssd()

            if not can_erase:
                return False, error
            # Create secret
            secret = subprocess.check_output(
                ['/usr/bin/pwgen', '-s', '32', '1'])[:-1]

            # Set the password. This should set 'enabled' in hdparm
            # security info
            self.do_hdparm('--security-set-pass', secret)

            # Check 'enabled' in hdparm security info
            security_info = self.hdparm_security_info()
            if not security_info.get('enabled', False):
                return False, (
                    'SSD password could not be set, '
                    'security info: {0}'.format(security_info))

            # Only perform secure SSD erase if 'enabled'
            self.do_hdparm('--security-erase', secret)

            # Check that 'enabled' is again False
            security_info = self.hdparm_security_info()

            if security_info.get('enabled', True):
                return False, (
                    'SSD password could not be UNset, '
                    'security info: {0}, secret: {1}'.format(
                        security_info, secret))
            secret = None

        return True, None

    def can_secure_erase_hdd(self):

        security_info = self.hdparm_security_info()

        for x in ['supported', 'enabled', 'locked', 'frozen']:
            if x not in security_info:
                return False, (
                    '{0} not found in security_info: {1}'.format(
                        x, security_info))

        if not security_info['supported']:
            return False, 'HDD secure erase seems not to be supported'

        if security_info['enabled']:
            return False, 'HDD password for secure erase is already set.'

        if security_info['locked']:
            return False, (
                'HDD is locked (try replugging the disk or '
                'hibernating system)')

        if security_info['frozen']:
            return False, (
                'HDD is frozen (try replugging the disk or '
                'hibernating system)')

        return True, None

    def secure_erase_hdd(self):
        # s1 = /dev/sdc
        # secret=`pwgen -s 32 1`
        # hdparm --user-master u --security-set-pass $secret $1
        # hdparm --user-master u --security-erase $secret $1

        if not settings.DEBUG:
            can_erase, error = self.can_secure_erase_hdd()

            if not can_erase:
                return False, error
            # Create secret
            secret = subprocess.check_output(
                ['/usr/bin/pwgen', '-s', '32', '1'])[:-1]

            # Set the password. This should set 'enabled' in hdparm
            # security info
            self.do_hdparm('--security-set-pass', secret)

            # Check 'enabled' in hdparm security info
            security_info = self.hdparm_security_info()
            if not security_info.get('enabled', False):
                return False, (
                    'HDD password could not be set, '
                    'security info: {0}'.format(security_info))

            # Only perform secure HDD erase if 'enabled'
            self.do_hdparm('--security-erase', secret)

            # Check that 'enabled' is again False
            security_info = self.hdparm_security_info()

            if security_info.get('enabled', True):
                return False, (
                    'HDD password could not be UNset, '
                    'security info: {0}, secret: {1}'.format(
                        security_info, secret))
            secret = None

        return True, None

    def secure_erase_hdd_manual(self):
        if not settings.DEBUG:
            # secure erase by using /dev/urandom
            subprocess.check_output([
                '/usr/local/bin/run-lessrandom', '/dev/{}'.format(
                    self.disk_name)])
#                ['bash','-c','dd',
#                 #'if=/dev/urandom',
#                 'if=<(/usr/local/bin/lessrandom)',
#                 'of=/dev/{0}'.format(self.disk_name),
#                 'bs=32M',
#                 'conv=fsync'])
        self.status = 'Secure erased'

    def quick_erase(self):
        if not settings.DEBUG:
            # Quick erase by zeroing begin and end of disk
            subprocess.check_output(
                ['dd',
                 'if=/dev/zero',
                 'of=/dev/{0}'.format(self.disk_name),
                 'bs=16M',
                 'seek=0',
                 'count=10',
                 'conv=fsync'])
            size = subprocess.check_output(
                ['/sbin/blockdev',
                 '--getsz',
                 '/dev/{0}'.format(self.disk_name)])

            count = 204800

            subprocess.check_output(
                ['dd',
                 'if=/dev/zero',
                 'of=/dev/{0}'.format(self.disk_name),
                 'bs=512',
                 'count={0}'.format(count),
                 'seek={0}'.format(int(size) - count),
                 'conv=fsync'])

        self.status = 'Quick erased'

    def shutdown_disk(self):
        print('\nSpinning down/ejecting disk, please wait...\n')
        if self.is_sas():
            subprocess.check_output(
                ['/usr/bin/sdparm',
                 '--readonly',
                 '--command=stop',
                 '/dev/{0}'.format(self.disk_name)])
        else:
            subprocess.check_output(
                ['/sbin/hdparm',
                 '-Y',
                 '/dev/{0}'.format(self.disk_name)])
        self.status = 'Shutdown'

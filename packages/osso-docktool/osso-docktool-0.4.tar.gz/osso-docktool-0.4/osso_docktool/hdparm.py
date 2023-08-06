import subprocess

__author__ = 'osso'


class HdparmParser(object):
    def __init__(self, disk_name):
        self.information = {}
        self.disk_name = disk_name
        self._security_info = None
        self._data = subprocess.check_output(
            ['/sbin/hdparm',
             '-I',
             '/dev/{0}'.format(disk_name)])

    def get_security_info(self):
        if 'Security' in self._data:
            lines = self._data.split('\n')
            security_info = {}
            do_collect = False
            for line in lines:
                if do_collect:
                    if not line.startswith('\t'):
                        do_collect = False
                    else:
                        splitted = line.split('\t')
                        if (len(splitted) == 3 and
                                'master password' not in splitted[1].lower()):
                            security_info[splitted[2]] = (
                                splitted[1].lower() != 'not')
                elif line.startswith('Security'):
                    do_collect = True
            self._security_info = security_info
            return security_info
        return None

    def get_data(self):
        return self._data

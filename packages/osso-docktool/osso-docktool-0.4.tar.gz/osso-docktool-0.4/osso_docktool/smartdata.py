import re
import subprocess

__author__ = 'osso'


class SmartDataParser(object):
    def __init__(self, disk_name):
        self.disk_name = disk_name
        self.smart_data = self.get_smart_data()
        self.information = self.get_information_from_smart_data()
        self.smart_attributes = self.get_smart_attributes()

    def get_smart_data(self):
        try:
            smart_data = subprocess.check_output(
                ["/usr/sbin/smartctl",
                 "-x",
                 "/dev/{0}".format(self.disk_name)])
        except Exception as e:
            smart_data = e.output
        # Some devices return junk as part of the vendor name.
        return smart_data.decode('utf8', 'ignore')

    @property
    def sector_size(self):
        match = re.match(r'([0-9]*) ', self.information.get('Sector Size', ''))
        if match:
            return int(match.groups()[0])
        # Default to 512 (bytes)
        return 512

    def __get_value(self, search_str, column_name):
        data = [
            x for x in self.smart_attributes
            if x.get('attribute_name', '').lower() == search_str]

        if data:
            value = data[0].get(column_name, None)
            try:
                value = int(value)
            except ValueError:
                pass
            return value
        return None

    @property
    def wear_leveling_count(self):
        return self.__get_value('wear_leveling_count', 'value')

    @property
    def power_on_hours(self):
        return self.__get_value('power_on_hours', 'raw_value')

    @property
    def lbas_read(self):
        return self.__get_value('total_lbas_read', 'raw_value')

    @property
    def lbas_written(self):
        return self.__get_value('total_lbas_written', 'raw_value')

    @property
    def reallocated_sector_ct(self):
        return self.__get_value('reallocated_sector_ct', 'raw_value')

    @property
    def reallocated_event_count(self):
        return self.__get_value('reallocated_event_count', 'raw_value')

    @property
    def current_pending_sector(self):
        return self.__get_value('current_pending_sector', 'raw_value')

    @property
    def offline_uncorrectable(self):
        return self.__get_value('offline_uncorrectable', 'raw_value')

    def get_smart_attributes(self):
        if 'ID# ATTRIBUTE_NAME' in self.smart_data:
            lines = self.smart_data.split('\n')
            info = []
            do_collect = False
            headers = []
            for line in lines:
                if do_collect:
                    splitted = re.split(r' +', line)

                    if splitted[0] == '':
                        splitted = splitted[1:]

                    if '|' in splitted[0]:
                        break
                    else:
                        values = {}
                        for nr, x in enumerate(headers):
                            values[x] = splitted[nr]
                        info.append(values)

                elif 'ID# ATTRIBUTE_NAME' in line:
                    headers = [x.lower() for x in re.split(r' +', line)]
                    do_collect = True
            return info
        return []

    def get_information_from_smart_data(self):
        if 'START OF INFORMATION SECTION' in self.smart_data:
            lines = self.smart_data.split('\n')
            information = {}
            do_collect = False
            for line in lines:
                if do_collect:
                    if line == '':
                        break
                    else:
                        splitted = line.split(':')
                        param = splitted[0]
                        value = ':'.join(splitted[1:]).lstrip()
                        information.update({param: value})
                elif 'START OF INFORMATION SECTION' in line:
                    do_collect = True
            return information
        return {}


if __name__ == "__main__":
    parser = SmartDataParser('inv')

    print(parser.sector_size)
    print(parser.lbas_written)
    print(parser.lbas_read)
    print(parser.power_on_hours)
    print(parser.wear_leveling_count)
    print(parser.reallocated_sector_ct)
    print(parser.reallocated_event_count)
    print(parser.current_pending_sector)
    print(parser.offline_uncorrectable)

import json

import requests

try:
    from urllib.parse import urljoin  # py3
except ImportError:
    from urlparse import urljoin  # py2

from . import settings
from .jwt_token_provider import get_jwt_token, is_expired

__author__ = 'osso'


def get_device_model(information):
    if 'Device Model' in information:
        return information['Device Model']
    return information['Product']


def get_serial_number(information):
    key_options = [
        x for x in information.keys() if x.lower() == 'serial number']

    if len(key_options) == 1:
        return information[key_options[0]]

    raise Exception(
        "Serial number could not be determined from info: {0}".format(
            information))


class InventoryRESTClient(object):
    def __init__(self, base_url):
        self.base_url = urljoin(base_url, '/api/')
        self.hdd_uid = None
        self.__jwt_token = None

    @property
    def auth_header(self):
        if self.__jwt_token:
            if is_expired(self.__jwt_token):
                self.__jwt_token = None
        if not self.__jwt_token:
            self.__jwt_token = get_jwt_token(
                settings.DASHBOARD_SCHEME_URL,
                settings.DASHBOARD_AUTH_TOKEN)
        return {'Authorization': 'JWT {0}'.format(self.__jwt_token)}

    def __post_json(self, url, data):
        headers = {'content-type': 'application/json'}
        headers.update(self.auth_header)
        res = requests.post(
            urljoin(self.base_url, url), data=json.dumps(data),
            headers=headers)
        return res

    def __patch_json(self, url, data):
        headers = {'content-type': 'application/json'}
        headers.update(self.auth_header)
        res = requests.patch(
            urljoin(self.base_url, url),
            data=json.dumps(data),
            headers=headers)
        return res

    def get(self, url):
        return self.__get(url)

    def __get(self, url):
        res = requests.get(
            urljoin(self.base_url, url),
            headers=self.auth_header)
        return res

    def __generic_patch(self, url, data):
        res = self.__patch_json(url, data)
        if res.status_code == 200:
            return res.json()
        else:
            raise Exception(
                "Status code {0}, message {1}".format(
                    res.status_code,
                    res.text))

    def __generic_post(self, url, data):
        res = self.__post_json(url, data)
        if res.status_code == 201 or res.status_code == 200:
            return res.json()
        else:
            raise Exception(
                "Status code {0}, message {1}".format(
                    res.status_code,
                    res.text))

    def get_last_owner(self, asset_id):
        res = self.__get(
            'assets/asset_owner/?asset={0}&order_by=-date&limit=1'.format(
                asset_id)
        )
        if res.status_code == 200:
            data = res.json()
            if not data:
                return None
            return data[0]['name']
        elif res.status_code == 400:
            return None
        else:
            raise Exception("Status code {0}, message {1}".format(
                res.status_code, res.text))

    def get_hdd_url(self, asset_id):
        return urljoin(self.base_url, '/app/assets/hdd/{}/'.format(
            asset_id))

    def get_hdd(self, asset_id):
        res = self.__get(
            'assets/hdd/?id={0}'.format(
                asset_id)
        )
        if res.status_code == 200:
            data = res.json()
            if not data:
                return None
            return data
        elif res.status_code == 400:
            return None
        else:
            raise Exception("Status code {0}, message {1}".format(
                res.status_code, res.text))

    def change_bay(self, hdd_id, bay):
        return self.__generic_patch(
            'assets/hdd/{0}/?update_bay'.format(hdd_id),
            {'bay': bay})

    def add_owner(self, hdd_id, name, email=" "):
        return self.__generic_patch(
            'assets/hdd/{0}/?update_owner'.format(hdd_id),
            {'name': name,
             'email': email})

    def add_location(self, hdd_id, location):
        return self.__generic_patch(
            'assets/hdd/{0}/?update_location'.format(hdd_id),
            {'location': location})

    def add_status(self, hdd_id, status, extra_info=' '):
        return self.__generic_patch(
            'assets/hdd/{0}/?update_status'.format(hdd_id),
            {'status': status,
             'extra_info': extra_info})

    def add_health_status(self, hdd_id, status, extra_info=' '):
        return self.__generic_patch(
            'assets/hdd/{0}/?update_health'.format(hdd_id),
            {'status': status,
             'extra_info': extra_info})

    def add_wbpclass(self, hdd_id, wbp_class_number, extra_info=' '):
        return self.__generic_patch(
            'assets/hdd/{0}/?update_wbpclass'.format(hdd_id),
            {'wbp_class_number': wbp_class_number,
             'extra_info': extra_info})

    def add_smart_data(self, hdd_id, smart_data):
        return self.__generic_post(
            'assets/hdd_smartdata/',
            {'data': smart_data,
             'hdd': hdd_id})

    def add_hdd(self, information, bay='', asset_uid=None):
        data = {
            'device_model': get_device_model(information),
            'serial_number': get_serial_number(information),
            'user_capacity': information['User Capacity'],
            'ata_version': information.get('ATA Version is', 'unknown'),
            'firmware_version': information.get('Firmware Version', 'unknown'),
            'smart_support': information.get('SMART support is', 'unknown'),
            'bay': bay}

        if 'Model Family' in information:
            data.update({'model_family': information['Model Family']})

        return self.__generic_post('api/assets/hdd/', data)

    def get_hdd_id(self, device_model, serial_number):
        res = self.__get(
            'assets/hdd/?serial_number={0}&device_model={1}'.format(
                serial_number, device_model)
        )

        if res.status_code == 200:
            data = res.json()
            if not data:
                return None
            return data[0]['id']
        else:
            raise Exception("Status code {0}, message {1}".format(
                res.status_code, res.text))

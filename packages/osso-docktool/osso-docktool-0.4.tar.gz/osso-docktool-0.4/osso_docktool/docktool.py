from __future__ import print_function

from datetime import datetime
import argparse
import traceback
import sys

from . import settings
from .diskemptysampler import DiskEmptySampler
from .hdddock import HDDDock
from .inventoryrestclient import (
    InventoryRESTClient, get_device_model, get_serial_number)
from .labelprinterapiclient import get_labelprinter


try:
    raw_input  # py2
except NameError:
    def raw_input(msg=None):  # py3
        if msg is not None:
            print(msg, end='')
        return input()


class SymlinkNotFound(Exception):
    pass


def register_disk(smart_data, disk_name, inventory_rest_client):
    print('')
    print('Disk is not registered yet, please specify the following fields:')
    owner = raw_input('Owner [OSSO]: ')

    # Default to OSSO
    if owner in (None, ''):
        owner = 'OSSO'

    bay = raw_input('bay ['']: ')

    if bay in (None, ''):
        bay = ''

    erase = None
    while erase not in ('y', 'n', 'Y', 'N', ''):
        erase = raw_input('Quick erase? (y/N): ')

    # Retrieve information
    hdd_dock = HDDDock(disk_name)
    information = hdd_dock.get_information_from_smart_data(smart_data)

    result = inventory_rest_client.add_hdd(information, bay)
    tag_uid = result['tag_uid']
    hdd_id = result['id']

    inventory_rest_client.add_smart_data(
        hdd_id,
        smart_data)

    inventory_rest_client.add_status(
        hdd_id,
        'REGISTERED',
        'Registered at OSSO HQ docktool')

    inventory_rest_client.add_owner(
        hdd_id,
        owner)

    inventory_rest_client.add_location(
        hdd_id,
        'OSSO HQ: HDD docktool')

    if erase == 'y' or erase == 'Y':
        print('Start wiping')
        hdd_dock.quick_erase()
        inventory_rest_client.add_status(
            hdd_id,
            'QUICK_WIPED',
            'Quick wiped at OSSO HQ docktool'
        )
        print('Disk wiped')

    # Print label
    labelprinter_rest_client = get_labelprinter()
    labelprinter_rest_client.print_hdd_label(
        tag_uid, get_serial_number(information), owner)

    if not settings.DEBUG:
        hdd_dock.shutdown_disk()
    raw_input('Registration complete, press enter')
    exit(0)


def registered_disk_actions(
        smart_data, hdd_id, disk_name, inventory_rest_client,
        print_data, print_smart_data):

    hdd_dock = HDDDock(disk_name)
    information = hdd_dock._info

    if not settings.DEBUG:
        # Always add smart data, even when disk is registered
        inventory_rest_client.add_smart_data(
            hdd_id,
            smart_data)

        # Always add a status & location
        # of the disk being seen at OSSO HQ
        inventory_rest_client.add_status(
            hdd_id,
            'CHECKED_IN',
            'Checked in at OSSO HQ docktool')

        inventory_rest_client.add_location(
            hdd_id,
            'OSSO HQ: HDD docktool')

    hdd = inventory_rest_client.get_hdd(hdd_id)[0]
    current_owner = hdd.get('current_owner', None)

    if current_owner:
        current_owner = current_owner.get('name', None)
    if not current_owner:
        current_owner = 'Notset'

    # current_status = hdd.get('status', None)

    # if current_status:
    #     current_status = current_status.get('name', None)
    # if not current_status:
    #     current_status = 'Notset'

    current_health_status = hdd.get('current_health', None)

    if current_health_status:
        current_health_status = current_health_status.get('status', None)

    if not current_health_status:
        current_health_status = 'Notset'

    is_ssd = hdd_dock.is_ssd()
    print_data += print_smart_data

    print_data.append(['', '-'])
    print_data.append(['REGISTRATION INFORMATION', '-'])
    print_data.append(['=', '-'])
    print_data.append(['Disk is already registered as', '{0}'.format(
        hdd['id'])])
    print_data.append(['Last owner', '{0}'.format(current_owner)])
    # print_data.append(['Last status', '{0}'.format(current_status)])
    print_data.append(['Last health status', '{0}'.format(
        current_health_status)])
    print_data.append(['Server bay', '{0}'.format(hdd['bay'])])

    do_print(print_data, disk_name, hdd_dock)

    print('')
    print('Inventory-url: {0}'.format(
        inventory_rest_client.get_hdd_url(hdd['id'])))
    print('')
    print('Possible actions:')
    print('1. Change owner')
    print('2. Reprint label')
    print('3. Quick erase {0}'.format('SSD' if is_ssd else 'disk'))

    if is_ssd:
        print('4. Secure erase SSD')
    else:
        print('4. Secure erase HDD')

    print('5. Change server bay')
    print('6. Change health status')
    print('7. Print health label')
    print('8. Secure erase HDD (manual, slow)')

    print('')
    print('9. Quit')

    action_whitelist = ('1', '2', '3', '4', '5', '6', '7', '8', '9')

    action = ''

    while action != '9':
        while action not in action_whitelist:
            action = raw_input('Action: ')
        if action == '1':
            owner = ''
            while len(owner) == 0:
                owner = raw_input('New owner: ')
            inventory_rest_client.add_owner(
                hdd_id,
                owner)
            current_owner = owner
        elif action == '2':
            # Print label
            labelprinter_rest_client = get_labelprinter()
            labelprinter_rest_client.print_hdd_label(
                hdd['tag_uid'],
                get_serial_number(information),
                current_owner)
        elif action == '3':
            print('Start quick wiping')
            hdd_dock.quick_erase()
            inventory_rest_client.add_status(
                hdd_id,
                'QUICK_WIPED',
                'Quick wiped at OSSO HQ docktool'
            )
            print('Disk/ssd quick wiped')
        elif action == '4':
            if is_ssd:
                can_wipe, error = hdd_dock.can_secure_erase_ssd()
                if not can_wipe:
                    print('Error: {0}'.format(error))
                    inventory_rest_client.add_status(
                        hdd_id,
                        'SSD_SECURE_WIPED_ERROR',
                        'SSD secure wipe error at OSSO HQ docktool, '
                        '{0}'.format(error))
                else:
                    print('Start secure wiping SSD')
                    success, error = hdd_dock.secure_erase_ssd()
                    if success:
                        print('SSD secure wiped')

                        sample_count = settings.SDD_SAMPLE_COUNT
                        sample_size = settings.SSD_SAMPLE_SIZE

                        disk_empty_sampler = DiskEmptySampler(
                            disk_name, sample_count, sample_size)
                        print(
                            'Sampling SSD to check if empty... '
                            '(sample_count: {0}, sample_size {1})'.format(
                                sample_count, sample_size))

                        result = disk_empty_sampler.sample_disk()

                        if result is None:
                            print(
                                'Error occured, please report to '
                                'administrator')
                        elif result:
                            print('OK: All samples are empty')
                            inventory_rest_client.add_status(
                                hdd_id,
                                'SSD_SECURE_WIPED',
                                ('SSD secure wiped at OSSO HQ docktool & '
                                 'checked {0} {1}').format(
                                    sample_count, sample_size))
                        else:
                            print('ERROR: Found not empty sample!')
                            print('Please check SSD manually!')
                            inventory_rest_client.add_status(
                                hdd_id,
                                'SSD_SECURE_WIPED_ERROR',
                                ('SSD secure wipe error at OSSO HQ '
                                 'docktool, found not empty samples'))
                    else:
                        print('Error: {0}'.format(error))
            else:
                can_wipe, error = hdd_dock.can_secure_erase_hdd()
                if not can_wipe:
                    print('Error: {0}'.format(error))
                    inventory_rest_client.add_status(
                        hdd_id,
                        'HDD_SECURE_WIPED_ERROR',
                        ('HDD secure wipe error at OSSO HQ '
                         'docktool, {0}'.format(error)))
                else:
                    print('Start secure wiping HDD')
                    success, error = hdd_dock.secure_erase_hdd()
                    if success:
                        print('HDD secure wiped')

                        sample_count = settings.SDD_SAMPLE_COUNT
                        sample_size = settings.SSD_SAMPLE_SIZE

                        disk_empty_sampler = DiskEmptySampler(
                            disk_name, sample_count, sample_size)
                        print(
                            'Sampling HDD to check if empty... '
                            '(sample_count: {0}, sample_size {1})'.format(
                                sample_count, sample_size))

                        result = disk_empty_sampler.sample_disk()

                        if result is None:
                            print(
                                'Error occured, please report to '
                                'administrator')
                        elif result:
                            print('OK: All samples are empty')
                            inventory_rest_client.add_status(
                                hdd_id,
                                'HDD_SECURE_WIPED',
                                ('HDD secure wiped at OSSO HQ docktool & '
                                 'checked {0} {1}'.format(
                                     sample_count, sample_size)))
                        else:
                            print('ERROR: Found not empty sample!')
                            print('Please check HDD manually!')
                            inventory_rest_client.add_status(
                                hdd_id,
                                'HDD_SECURE_WIPED_ERROR',
                                ('HDD secure wipe error at OSSO HQ '
                                 'docktool, found not empty samples'))
                    else:
                        print('Error: {0}'.format(error))

        elif action == '5':
            bay = ''
            while len(bay) == 0:
                bay = raw_input('New server bay: ')
            hdd = inventory_rest_client.change_bay(
                hdd_id,
                bay)
            print('Server bay changed to: {0}'.format(hdd['bay']))
        elif action == '6':
            health_status = ''
            while len(health_status) == 0:
                health_status = raw_input('New health status: ')
            inventory_rest_client.add_health_status(
                hdd_id,
                health_status)
            current_health_status = health_status
        elif action == '7':
            # Print label
            lines = [
                'Health status: {0} @ {1}'.format(
                    current_health_status.upper(),
                    datetime.now().strftime('%Y-%m-%d')),
                '',
                'Serial : {0}'.format(get_serial_number(information)),
            ]
            total_bytes_written = [
                x for x in print_smart_data
                if 'Total bytes written' in x[0]][0]
            total_bytes_read = [
                x for x in print_smart_data
                if 'Total bytes read' in x[0]][0]

            lines.append('Total bytes written/read: {0}/{1}'.format(
                total_bytes_written[1], total_bytes_read[1]))

            for item in ['Power on hours', 'Reallocated sector count']:
                lines += [
                    ' : '.join([x[0].rstrip(), x[1]])
                    for x in print_smart_data if item in x[0]]

            labelprinter_rest_client = get_labelprinter()
            labelprinter_rest_client.print_generic_label(lines)
        elif action == '8':
            print('Start wiping, please wait this can take a long time...')
            hdd_dock.secure_erase_hdd_manual()
            inventory_rest_client.add_status(
                hdd_id,
                'SECURE_WIPED',
                'Secure wiped (manual) at OSSO HQ docktool')
            print('Disk wiped')

        if action != '9':
            action = ''

    if settings.DEBUG:
        hdd_dock.shutdown_disk()
    exit(0)


def human_readable_bytes(byte_count):
    options = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']

    counter = 0
    while int(byte_count / 1024.0) > 0:
        byte_count = byte_count / 1024.0
        counter += 1
        if counter == len(options) - 1:
            break

    return '{0} {1}'.format(round(byte_count, 2), options[counter])


def fix_length(text):
    return text


def do_print(data, disk_name, hdd_dock):
    key_length = 0
    item_length = 0

    for x in data:
        if len(x[1]) > item_length:
            item_length = len(x[1])
        if len(x[0]) > key_length:
            key_length = len(x[0])

    print('DISK INFORMATION [BAY NR: {0}]'.format(
        hdd_dock.docktool_bay_nr))

    print('=' * (key_length + item_length + 3))

    for x in data:
        if x[0] == '=':
            print('=' * (key_length + item_length + 3))
        elif x[1] == '-':
            print(x[0])
        else:
            x[0] = x[0] + ' ' * (key_length - len(x[0]))
            print(' : '.join(x))


def main_menu(disk_name):
    hdd_dock = HDDDock(disk_name)
    smart_data_parser = hdd_dock.smart_data_parser
    information = hdd_dock._info
    sys.stdout.write('\x1b]2;DOCKTOOL DISK BAY: {0}\x07'.format(
        hdd_dock.docktool_bay_nr))

    data = []

    data.append(['Device model', '{0}'.format(get_device_model(information))])
    data.append(['Serial', '{0}'.format(get_serial_number(information))])
    data.append(['Device/port', '{0}/{1}'.format(
        disk_name, hdd_dock.port if hdd_dock.port else 'Unknown')])
    data.append(['SSD', '{0}'.format('yes' if hdd_dock.is_ssd() else 'no')])
    data.append(['SAS (detected)', '{0}'.format(
        'yes' if hdd_dock.is_sas() else 'no')])
    data.append(['User Capacity', information.get('User Capacity', 'Notset')])

    smart_data = []

    if smart_data_parser.sector_size and smart_data_parser.lbas_written:
        byte_count = (
            smart_data_parser.sector_size *
            smart_data_parser.lbas_written)
        smart_data.append(['Total bytes written', '{0}'.format(
            human_readable_bytes(byte_count))])
    else:
        smart_data.append(['Total bytes written', 'Notset'])

    if smart_data_parser.sector_size and smart_data_parser.lbas_read:
        byte_count = (
            smart_data_parser.sector_size * smart_data_parser.lbas_read)
        smart_data.append(['Total bytes read', '{0}'.format(
            human_readable_bytes(byte_count))])
    else:
        smart_data.append(['Total bytes read', 'Notset'])

    def _NS(value):
        if value is None:
            return 'Notset'
        return str(value)

    smart_data.append([
        'Power on hours',
        '{0} hours'.format(_NS(smart_data_parser.power_on_hours))])
    smart_data.append([
        'Wear leveling count',
        _NS(smart_data_parser.wear_leveling_count)])
    smart_data.append([
        'Reallocated sector count',
        _NS(smart_data_parser.reallocated_sector_ct)])
    smart_data.append([
        'Reallocated event count',
        _NS(smart_data_parser.reallocated_event_count)])
    smart_data.append([
        'Current pending sector',
        _NS(smart_data_parser.current_pending_sector)])
    smart_data.append([
        'Offline uncorrectable',
        _NS(smart_data_parser.offline_uncorrectable)])

    inventory_rest_client = InventoryRESTClient(
        settings.DASHBOARD_BASE_URL)

    # HDD is an asset so asset_id = hdd_id
    hdd_id = inventory_rest_client.get_hdd_id(
        get_device_model(information), get_serial_number(information))

    if hdd_id is None:
        do_print(data + smart_data, disk_name, hdd_dock)
        register_disk(hdd_dock._smart_data, disk_name, inventory_rest_client)
    else:
        registered_disk_actions(hdd_dock._smart_data, hdd_id, disk_name,
                                inventory_rest_client, data, smart_data)


def main():
    parser = argparse.ArgumentParser(
        description='Docktool for processing disks.')
    parser.add_argument(
        'device', metavar='D', type=str, help='Device to use for example: sda')
    args = parser.parse_args()

    try:
        main_menu(args.device)
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        raw_input('Error found, please inform administrator. Press enter')
        raise e


if __name__ == '__main__':
    main()

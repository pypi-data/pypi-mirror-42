from hashlib import md5
import random

__author__ = 'osso'


# dd if=/dev/zero of=output.dat  bs=1M  count=1 && md5sum output.dat
OPTIONS = {
    'KB': {
        'md5_hash': '0f343b0931126a20f133d67c2b018a3b',
        'size': 1024},
    'MB': {
        'md5_hash': 'b6d81b360a5672d80c27430f39153e2c',
        'size': 1024 ** 2}
}


class DiskEmptySampler(object):
    """
    Divide the disk in 'sample_count' regions
    and sample (md5sum) 'sample_size' bytes randomly per region
    """

    def __init__(self, disk_name, sample_count=100, sample_size='MB'):
        if sample_size not in OPTIONS:
            raise Exception('Unknown sample_size, options are {0}'.format(
                OPTIONS.keys()))
        self.disk_name = disk_name

        # No divide by zero errors
        if sample_count == 0:
            raise Exception('Sample size should not be zero')

        self.sample_count = sample_count
        self.sample_size_opt = sample_size
        self.expected_hash = OPTIONS[sample_size]['md5_hash']
        self.sample_size = OPTIONS[sample_size]['size']

    def sample_disk(self):
        is_empty = True

        with open('/dev/{0}'.format(self.disk_name), 'rb') as f:
            # Get the size of disk
            f.seek(0, 2)
            size = f.tell()

            # divide the disk into sample_regions
            sample_region_size = size / self.sample_count

            # Check if the regions are large enough to get a sample from
            if self.sample_size > sample_region_size:
                print('Sample size is to large')
                return None

            # Loop through the sample_regions
            for sample_nr in range(0, self.sample_count):
                # calculate begin and end of region based on sample_region size
                # Note: should never exceed the size of disk
                region_start = sample_nr * sample_region_size
                region_end = min((sample_nr + 1) * sample_region_size, size)

                # pick random offset within region
                offset = random.randint(
                    region_start, region_end - self.sample_size)

                # Jump to offset
                f.seek(offset)

                # Check if md5 is same as the expected_hash
                md5_sum = md5(f.read(self.sample_size)).hexdigest()
                if md5_sum != self.expected_hash:
                    print('Digests are not same: {0} {1}'.format(
                        md5_sum, self.expected_hash))
                    print('for offset: {0} (sample_size: {1})'.format(
                        offset, self.sample_size))
                    is_empty = False
                    break

        return is_empty

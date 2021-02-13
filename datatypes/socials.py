"""

This module generates social security numbers

"""

from common import helpers


class Datatype:

    def __init__(self, cli_object):
        self.cli = 'ssn'
        self.description = 'Social Security Numbers'
        self.filetype = 'text'
        self.datasize: int = int(cli_object.data_size)

    @staticmethod
    def create_ssn():
        ssn = helpers.random_numbers(9)
        ssn = ssn[0:3] + "-" + ssn[3:5] + "-" + ssn[5:9]
        return ssn

    def generate_data(self):
        print('[*] Generating data...')
        ssns = ''
        # This is approx 1 meg of socials
        for single_ssn in range(0, 81500 * self.datasize):
            ssns += self.create_ssn() + ', '
        return ssns

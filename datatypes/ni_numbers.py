"""

This module generates UK National Insurance Numbers.

Format is 2 prefix letters, 6 digits, 1 suffix letter:
AB123456C

They are sometimes printed with spaces:
AB 12 34 56 C

This modules doesn't take correct letter prefixing into account,
it just generates them randomly. But this is probably good
enough for basic regex-type filters to detect.

"""

from common import helpers


class Datatype:

    def __init__(self, cli_object):
        self.cli = 'ni'
        self.description = 'UK National Insurance Numbers'
        self.filetype = 'text'
        self.datasize = int(cli_object.data_size)

    @staticmethod
    def create_ni():
        ni_n = helpers.random_numbers(6)
        ni_s = (helpers.random_string(3)).upper()
        ni = ni_s[0:2] + ni_n[0:6] + ni_s[2:3]
        return ni

    def generate_data(self):
        print('[*] Generating data...')
        nis = ''
        # This is approx 1 meg of ni's (not including ", ")
        for single_ni in range(0, 100000 * self.datasize):
            nis += self.create_ni() + ', '
        return nis

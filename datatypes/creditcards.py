"""

This module generates credit card data

"""

import copy
import random


class Datatype:

    def __init__(self, cli_object):
        self.cli = 'cc'
        self.description = 'Credit Card Numbers'
        self.filetype = 'text'
        self.datasize = int(cli_object.data_size)

    @staticmethod
    def completed_number(prefix, length, the_generator):
        """
        'prefix' is the start of the CC number as a string, any number of digits.
        'length' is the length of the CC number to generate. Typically 13 or 16
        """

        ccnumber = prefix

        # generate digits
        while len(ccnumber) < (length - 1):
            digit = str(the_generator.choice(range(0, 10)))
            ccnumber.append(digit)

        # Calculate sum
        _sum = 0
        pos = 0

        reversed_cc_number = []
        reversed_cc_number.extend(ccnumber)
        reversed_cc_number.reverse()

        while pos < length - 1:
            odd = int(reversed_cc_number[pos]) * 2
            if odd > 9:
                odd -= 9

            _sum += odd

            if pos != (length - 2):
                _sum += int(reversed_cc_number[pos + 1])
            pos += 2

        # Calculate check digit
        checkdigit = ((_sum / 10 + 1) * 10 - _sum) % 10
        ccnumber.append(str(checkdigit))
        return ''.join(ccnumber)

    def credit_card_number(self, prefix_list, length, how_many):

        generator = random.Random()
        generator.seed()

        result = []

        while len(result) < how_many:
            ccnumber = copy.copy(generator.choice(prefix_list))
            result.append(self.completed_number(ccnumber, length, generator))

        return result

    def generate_data(self):
        print('[*] Generating data...')
        # credit card constants
        visa_prefix_list = [
            ['4', '5', '3', '9'],
            ['4', '5', '5', '6'],
            ['4', '9', '1', '6'],
            ['4', '5', '3', '2'],
            ['4', '9', '2', '9'],
            ['4', '0', '2', '4', '0', '0', '7', '1'],
            ['4', '4', '8', '6'],
            ['4', '7', '1', '6'],
            ['4']]
        mastercard_prefix_list = [
            ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]
        amex_prefix_list = [['3', '4'], ['3', '7']]

        mastercards = self.credit_card_number(
            mastercard_prefix_list, 16, 19800 * self.datasize)
        visas = self.credit_card_number(
            visa_prefix_list, 16, 19800 * self.datasize)
        amexes = self.credit_card_number(
            amex_prefix_list, 15, 19800 * self.datasize)

        all_cards = mastercards + visas + amexes
        final_cards = ''

        for card in all_cards:
            final_cards += card + ', '

        return final_cards

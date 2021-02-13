"""

This module creates names, addresses, and SSNs.

"""

import random
from common import helpers


class Datatype:

    # self.cli, self.description, and self.filetype are required attributes.
    # self.cli is what is listed (along with self.description) when running
    # --list-datatypes.  self.cli is also used in conjunction with --datatype
    # to specify the datatype.  self.description is just a description of the
    # data being generated.  self.filetype should be set to text if it is a text
    # data being generated (vs. binary).
    # The __init__ has full access to all command line parameters passed
    # in at runtime.
    def __init__(self, cli_object):
        self.cli = 'identity'
        self.datasize = int(cli_object.data_size)
        self.description = 'Full names, Addresses, and Socials'
        self.filetype = 'text'
        self.first_names = [
            'michael', 'john', 'david', 'chris', 'mike', 'james',
            'mark', 'jason', 'robert', 'jessica', 'sarah', 'jennifer',
            'paul', 'brian', 'kevin', 'daniel', 'ryan', 'matt', 'andrew',
            'michelle', 'steve', 'lisa', 'alex', 'joe', 'amanda', 'ashley',
            'scott', 'richard', 'eric', 'jeff', 'justin', 'karen', 'linda',
            'mary', 'adam', 'melissa', 'matthew', 'nick', 'stephanie',
            'anthony', 'tom', 'josh', 'laura', 'tim', 'jim', 'amy', 'peter',
            'dan', 'nicole', 'tony']
        self.last_names = [
            'smith', 'johnson', 'jones', 'williams', 'brown',
            'lee', 'khan', 'singh', 'kumar', 'miller', 'davis', 'wilson',
            'taylor', 'thomas', 'garcia', 'anderson', 'sharma', 'martin',
            'rodriguez', 'ali', 'white', 'jackson', 'thompson', 'moore',
            'ahmed', 'martinez', 'lopez', 'harris', 'patel', 'king', 'walker',
            'hernandez', 'clark', 'lewis', 'robinson', 'young', 'gonzalez',
            'hall', 'wright', 'scott', 'perez', 'green', 'allen', 'tan',
            'shah', 'roberts', 'adams', 'nguyen', 'james', 'hill']
        self.addresses = [
            'PO Box 4927 Montgomery, AL 36103', 'PO Box 110801 Juneau, AK 99811-0801',
            '1110 W. Washington Street, Suite 155 Phoenix, AZ 85007',
            'One Capitol Mall Little Rock, AR 72201',
            'PO Box 1499 Sacramento, CA 95812',
            '1625 Broadway Suite 2700 Denver, CO 80202',
            '755 Main Street Hartford, CT 06103',
            '99 Kings Highway PO Box 1401 Dover, DE 19903',
            'PO Box 1100 Tallahassee, FL 32302',
            '75 Fifth Street, N.W., Suite 1200 Atlanta, GA 30308',
            'PO Box 2359 Honolulu, HI 96804',
            '700 West State St. Boise, ID 83720-0093',
            '620 E. Adams Springfield, IL 62701',
            'One North Capitol Indianapolis, IN 46204',
            '200 East Grand Ave. Des Moines, IA 50309',
            '1000 S.W. Jackson Street Topeka, KS 66612',
            '500 Mero St. #2200 Frankfurt, KY 40601',
            '#59 State House Station Augusta, ME 04333-0059',
            '217 Redwood St Baltimore, MD 21202',
            '10 Park Plaza Boston, MA 02116',
            '300 N. Washington Sq. Lansing, MI 48913',
            '500 Metro Square St. Paul, MN 55101',
            '1424 9th Ave. Helena, MT 59620-0533',
            '401 North Carson St. Carson City, NV 89701',
            '20 W. State St. Trenton, NJ 08625',
            '491 Old Santa Fe Trail Santa Fe, NM 87501',
            '301 N. Wilmington St. Raleigh, NC 27601',
            '604 East Boulevard Bismark, ND 58505-0825'
            '77 South High St Columbus, OH 43266-0544',
            '775 Summer St, NE Salem, OR 97310',
            '4070 Hawthorne Lane West Orange, NJ 07052',
            '6683 1st Avenue Kearny, NJ 07032',
            '4692 Mill Road Glen Ellyn, IL 60137',
            '9024 6th Avenue Clifton, NJ 07011',
            '1990 Shady Lane Chicago, IL 60621',
            '5169 Forest Street Mableton, GA 30126',
            '714 5th Street Riverside, NJ 08075',
            '248 7th Avenue Quincy, MA 02169',
            '110 3rd Street Lenoir, NC 28645',
            '6 Broadway Myrtle Beach, SC 29577',
            '110 3rd Street Lenoir, NC 28645',
            '488 Schoolhouse Lane Johnston, RI 02919',
            '658 Market Street New Brunswick, NJ 08901'
        ]

    @staticmethod
    def create_ssn():
        ssn = helpers.random_numbers(9)
        ssn = ssn[0:3] + "-" + ssn[3:5] + "-" + ssn[5:9]
        return ssn

    # generate is a required function.  This is what is called by the framework
    # to generate the data.  Any number of "sub functions" can be created, but
    # generate should be considered the "main" function.  generate must return
    # the generated data.
    def generate_data(self):

        data = ''

        # Every 17 records is a meg (approx)
        total_number = 17000 * self.datasize
        for number in range(0, total_number):
            data += random.choice(self.first_names) + ' ' +\
                random.choice(self.last_names) + ', ' + self.create_ssn() +\
                ', ' + random.choice(self.addresses) + '\n'

        return data

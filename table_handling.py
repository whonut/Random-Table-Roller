import csv
from random import randint
from itertools import chain


class TableFormatError(Exception):
    '''Raised when the user tries to load an improperly formatted table
       file.'''

    def __init__(self, msg):
        self.err_msg = msg


def load_table(filepath, headers=False):
    '''Return a dict representing a roll table loaded from filepath.

    Loads a roll table from the CSV file at filepath into a dict whose keys
    are ranges containing the range of rolls (min, max) associated with the
    event specified in that key's value (a string describing the event).
    If headers is True, then it is assumed that the first row of the file
    contains some descriptive headers and the row is ignored. It defaults
    to False.

    The first column of the CSV should be the numbers or ranges of numbers
    to roll in order to 'bring about' the associated event in the same row
    of the second column. Ranges should be specified with dashes e.g.
    a roll of 1 to 10 inclusive would be written as '1-10'. None of the
    intervals should overlap. If there is a gap in the table i.e. a roll
    within the bounds of the table which is not associated with an event, an
    IOError is raised.'''

    table = {}
    with open(filepath, newline='') as table_file:
        try:
            table_reader = csv.reader(table_file, strict=True)
        except csv.Error as err:
            # Bad CSV input.
            raise TableFormatError("Bad CSV input") from err

        for row in table_reader:
            if headers and table_reader.line_num == 1:
                # Ignore the first line if headers is True
                continue
            roll = row[0]
            event = row[1]
            if row[0].find("-") != -1:
                # A range of rolls has been specified for this table item.
                min_roll = int(roll[:roll.find("-")])
                max_roll = int(roll[roll.find("-")+1:])
                table[range(min_roll, max_roll+1)] = event
            else:
                # A single roll has been specified for this table item.
                roll_num = int(roll)
                table[range(roll_num, roll_num+1)] = event

    # Check if there is a gap in the table by comparing its keys to a range.
    rolls_in_table = sorted(list(chain(*table.keys())))
    max_in_table = max(rolls_in_table)
    min_in_table = min(rolls_in_table)
    gap = rolls_in_table != list(range(min_in_table, max_in_table+1))
    if gap:
        filename = filepath[filepath.rfind("/")+1:]
        err_msg = 'There is a gap in the table: {}'.format(filename)
        raise TableFormatError(err_msg)

    return table


def roll_against(table):
    '''Return a randomly chosen entry (a dict value) from a roll table.

    table must be a dict of the same format as those created by load_table.'''

    # Get the range of rolls that the table caters for.
    permitted = list(chain(*table.keys()))
    max_permitted = max(permitted)
    min_permitted = min(permitted)

    # Generated a random integer bounded by the maximum and minimum permitted
    # rolls.
    roll = randint(min_permitted, max_permitted)

    # Check which event the roll corresponds to and return the description of
    # that event.
    for entry in table.items():
        if roll in entry[0]:
            return entry[1]

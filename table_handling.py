import csv
from random import randint
from itertools import chain, product


class TableFormatError(Exception):
    '''Raised when the user tries to load an improperly formatted table
       file.'''

    def __init__(self, msg):
        self.err_msg = msg


def load_table(filepath):
    '''Return a dict representing a roll table loaded from filepath.

    Loads a roll table from the CSV file at filepath into a dict whose keys
    are ranges containing the range of rolls (min, max) associated with the
    event specified in that key's value (a string describing the event).
    The first row of the file should contain some descriptive headers and
    should begins with a '%'. If this is the case, then the row is ignored.

    The first column of the CSV should be the numbers or ranges of numbers
    to roll in order to 'bring about' the associated event in the same row
    of the second column. Ranges should be specified with dashes e.g.
    a roll of 1 to 10 inclusive would be written as '1-10'. None of the
    intervals should overlap. Event descriptions containing commas should be
    wrapped in double quotes e.g. 6,"Well, well, well...". If there is an issue
    with the formatting of the CSV file, then TableFormatError is raised.'''

    table = {}
    with open(filepath, newline='') as table_file:
        table_reader = csv.reader(table_file, strict=True)
        for row in table_reader:
            if len(row) != 2:
                # Tables should only have two columns.
                raise TableFormatError("Tables should only have two columns.")
            if table_reader.line_num == 1:
                # Check that the header line begins with a '%'
                if row[0][0] == "%":
                    # Ignore the first line.
                    continue
                else:
                    raise TableFormatError(("The header (first) line should "
                                            "start with a '%'"))
            roll = row[0]
            event = row[1]
            if row[0].find("-") != -1:
                # A range of rolls has been specified for this table item.
                min_roll = int(roll[:roll.find("-")])
                max_roll = int(roll[roll.find("-")+1:])
                r = range(min_roll, max_roll+1)
                if r not in table:
                    table[r] = event
                else:
                    # Don't allow repeated roll ranges
                    raise TableFormatError("Roll ranges must be unique.")
            else:
                # A single roll has been specified for this table item.
                roll_num = int(roll)
                r = range(roll_num, roll_num+1)
                if r not in table:
                    table[r] = event
                else:
                    # Don't allow repeated roll ranges
                    raise TableFormatError("Roll ranges must be unique.")

    # Check if any of the roll ranges overlap.
    for p in product(table.keys(), repeat=2):
        first_in_second = (p[0].start in p[1]) or ((p[0].stop - 1) in p[1])
        second_in_first = (p[1].start in p[0]) or ((p[0].stop - 1) in p[0])
        if first_in_second or second_in_first:
            raise TableFormatError("Roll ranges cannot overlap.")

    # Check if there is a gap in the table by comparing its keys to a range.
    rolls_in_table = sorted(list(chain(*table.keys())))
    max_in_table = max(rolls_in_table)
    min_in_table = min(rolls_in_table)
    gap = rolls_in_table != list(range(min_in_table, max_in_table+1))
    if gap:
        filename = filepath[filepath.rfind("/")+1:]
        err_msg = 'There is a gap in the table.'.format(filename)
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

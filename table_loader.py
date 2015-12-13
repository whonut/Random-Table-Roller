import csv
from itertools import chain


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
        table_reader = csv.reader(table_file)
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
    rolls_in_table = chain(table.keys())
    max_in_table = max(rolls_in_table)
    min_in_table = min(rolls_in_table)
    gap = list(rolls_in_table) != list(range(min_in_table, max_in_table+1))
    if gap:
        raise IOError('There is a gap in the table "{}"'.format(filepath))

    return table

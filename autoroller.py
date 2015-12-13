from random import randint
from itertools import chain


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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py-oeis

A Python library to access the OEIS (Online Encyclopedia of Integer Sequences).

Sumant Bhaskaruni
v0.1
"""

__version__ = '0.1'

import pendulum
import requests


class NegativeIndexError(IndexError):
    """Raised when a negative index is passed."""


class IndexTooHighError(IndexError):
    """Raised when an index too high to handle is passed."""


class Sequence(object):
    """An object to represent a single OEIS sequence.

    Initializer arguments:
        number (int): the OEIS sequence ID

    Instance attributes:
        seq_id (int): the OEIS sequence ID
        name (str): the name of the sequence
        formula (str): the text of the 'Formula' section on OEIS
        sequence (list): the first few values of the sequence
        comments (str): the text of the 'Comments' section on OEIS
        author (str): the author of the sequence
        created (str): when the sequence was created
    """

    def __init__(self, seq_id):
        """See class docstring for details."""

        info = requests.get('https://oeis.org/search?fmt=json&q=id:A{:d}'.
                            format(seq_id)).json()['results'][0]
        self.seq_id = info['number']
        self.name = info['name']
        self.formula = '\n'.join(info['formula'])
        self.comments = '\n'.join(info.get('comment', ''))
        self.author = info['author']
        self.created = pendulum.parse(
            info['created']).astimezone('utc').to_cookie_string()

        seq_page = requests.get('https://oeis.org/A{0:d}/b{0:06d}.txt'.format(
            self.seq_id)).text.rstrip('\n').split('\n')
        self.sequence = [int(item.split()[1]) for item in seq_page]

    def __contains__(self, item):
        return self.contains(item)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.nth_term(key)
        elif isinstance(key, slice):
            return self.subsequence(key.start, key.stop, key.step)

    def __iter__(self):
        for value in self.sequence:
            yield value

    def __len__(self):
        return len(self.sequence)

    def contains(self, item):
        """Check if the sequence contains the specified item. Note that this
        has the limit of the amount of numbers that OEIS hols.

        Positional arguments:
            item (int): the item to check for

        Returns whether the sequence contains item.
        """

        return item in self.sequence

    def find(self, item, instances = None):
        """Find specified number of instances of the specified item. Note that
        this has the limit of the amount of numbers that OEIS hols.

        Positional arguments:
            item (int): the item to find
            instances (int): the number of instances of item to find
                             (default: 1)

        Returns a list of sequence indices.
        """

        if instances is None:
            instances = 1

        result = []

        for index, value in enumerate(self.sequence):
            if len(result) == instances:
                return result

            if value == item:
                result.append(index)

        return result

    def nth_term(self, index):
        """Get the nth element of the sequence. 0-indexed. Raises an exception
        if the number is negative or too high.

        Positional arguments:
            index (int): the index of the element

        Returns the element of the sequence at index.
        """

        if index < 0:
            # sequences don't have negative indices, ya silly goofball
            raise NegativeIndexError(
                'The index passed ({:d}) is negative.'.format(index))

        if index > len(self):
            # OEIS only holds values up to a certain limit
            raise IndexTooHighError('{0:d} is higher than the amount of '
                                    'values OEIS holds ({1:d}).'.format(
                                        index, len(self)))

        return self.sequence[index]

    def subsequence(self, start = None, stop = None, step = None):
        """Get a subsequence of the sequence. 0-indexed. Raises an exception if
        either of the indices are negative or too high.

        Positional arguments:
            start (int): the starting index of the subsequence (default: 0)
            stop (int): the ending index of the subsequence
                        (default: len(sequence))
            step (int): the amount by which the index increases (default: 1)

        Returns a list of sequence items.
        """

        if start is None:
            start = 0

        if stop is None:
            stop = len(self)

        if step is None:
            step = 1

        if start < 0 or stop < 0:
            raise NegativeIndexError(
                'The index passed ({:d}) is negative.'.format(index))

        if start > len(self.sequence) or stop > len(self.sequence):
            raise IndexTooHighError('{0:d} is higher than the amount of '
            'values OEIS holds ({1:d}).'.format(
            index, len(self)))

        return self.sequence[start:stop:step]

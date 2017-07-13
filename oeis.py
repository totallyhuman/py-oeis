#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py-oeis

A Python library to access the OEIS.

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
        number (int): The OEIS sequence ID
    """

    def __init__(self, seq_id):
        """See class docstring for details."""

        info = requests.get('https://oeis.org/search?fmt=json&q=id:A{:d}'.
                            format(seq_id)).json()['results'][0]
        self.seq_id = info['number']
        self.name = info['name']
        self.formula = '\n'.join(info['formula'])
        self.sequence = list(map(int, info['data'].split(',')))
        self.comments = '\n'.join(info.get('comment', ''))
        self.author = info['author']
        self.created = pendulum.parse(
            info['created']).astimezone('utc').to_cookie_string()

    def __len__(self):
        values = requests.get(
            'https://oeis.org/A{0:d}/b{0:d}.txt'.format(self.seq_id))
        return len(values.split('\n'))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.nth_term(key)
        elif isinstance(key, slice):
            return self.subsequence(key.start, key.stop, key.step)

    def __iter__(self):
        values = requests.get(
            'https://oeis.org/A{0:d}/b{0:d}.txt'.format(self.seq_id))
        return (int(value.split()[1]) for value in values.split('\n'))

    def nth_term(self, index):
        """Get the nth element of the sequence. 0-indexed. Raises an exception
        if the number is negative or too high.

        Positional arguments:
            index (int): the index of the element

        Returns the element of the sequence at index.
        """

        if index < 0:
            # sequences don't have negative indices, ya silly goofball
            raise NegativeIndexError()

        try:
            return self.sequence[index]
        except IndexError:
            # fall back to scraping
            pass

        try:
            values = requests.get(
                'https://oeis.org/A{0:d}/b{0:d}.txt'.format(self.seq_id))
            return int(values.split('\n')[index].split()[1])
        except IndexError:
            # OEIS only holds values up to a certain limit
            raise IndexTooHighError()

    def subsequence(self, start = None, stop = None, step = None):
        """Get a subsequence of the sequence. 0-indexed. Raises and exception
        if either of the indexes are negative or too high.

        Positional arguments:
            start (int): the starting index of the subsequence (default: 0)
            stop (int): the ending index of the subsequence
                        (default: len(sequence))
            step (int): the amount by which the index increases (default: 1)
        """

        if start is None:
            start = 0

        if stop is None:
            stop = len(self)

        if step is None:
            step = 1

        if start < 0 or stop < 0:
            raise NegativeIndexError()

        try:
            return self.sequence[start:stop:step]
        except IndexError:
            pass

        try:
            values = requests.get(
                'https://oeis.org/A{0:d}/b{0:d}.txt'.format(self.seq_id))
            return [int(value.split()[1]) for value in values[start:stop:step]]
        except IndexError:
            raise IndexTooHighError()

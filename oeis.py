#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py-oeis

A Python library to access the OEIS.

Sumant Bhaskaruni
v0.1
"""

__version__ = '0.1'

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
        self.created = info['created']
        # TODO: parse the date into a better format

    def get_element(self, index):
        """Get the nth element of the sequence. 0-indexed. Raises an exception
        if the number is negative or too high.

        Positional arguments:
            index (int): the index of the element

        Returns the element of the sequence at index n.
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

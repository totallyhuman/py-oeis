#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py-oeis

A Python library to access the OEIS.

Sumant Bhaskaruni
v0.1
"""

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
        self.comments = '\n'.join(info['comment'])
        self.author = info['author']
        self.created = info['created']

    def get_element(self, index):
        """Get the nth element of the sequence. 0-indexed. Raises an exception
        if the number is too high.

        Positional arguments:
            n (int): the index of the element

        Returns the element of the sequence at index n."""

        if index < 0:
            raise NegativeIndexError()

        try:
            return self.sequence[index]
        except IndexError:
            pass

        try:
            values = requests.get(
                'https://oeis.org/A{0:d}/b{0:d}.txt'.format(self.seq_id))
            return int(values.split('\n')[index].split()[1])
        except IndexError:
            raise IndexTooHighError()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py-oeis

A Python library to access the OEIS (Online Encyclopedia of Integer Sequences).

Sumant Bhaskaruni
v2.0
"""

__version__ = '2.0'

import pendulum
import requests


class NonExistentSequence(LookupError):
    """Raised when a sequence with the ID passed does not exist."""


class NegativeIndexError(IndexError):
    """Raised when a negative index is passed."""


class IndexTooHighError(IndexError):
    """Raised when an index too high to handle is passed."""


class EmptyQuery(ValueError):
    """Raised when an empty list of query terms is passed."""


class Sequence(object):
    """An object to represent a single OEIS sequence.

    Initializer arguments:
        seq_id (int): the OEIS sequence ID

    Instance attributes:
        seq_id (int): the OEIS sequence ID
        sequence (list): the first few values of the sequence
        info (dict): information pertaining to the sequence including:
            name (str): the name of the sequence
            formula (str): the text of the 'Formula' section on OEIS
            comments (str): the text of the 'Comments' section on OEIS
            example (str): the text of the 'Example' section on OEIS
            crossrefs (str): the text of the 'Crossrefs' section on OEIS
            keywords (list): the keywords (tags) of the sequence
            author (str): the author of the sequence
            created (float): when the sequence was created (epoch timestamp)
            url (str): the URL of the sequence on OEIS
    """

    def __init__(self, seq_id):
        """See class docstring for details."""

        info = requests.get('https://oeis.org/search?fmt=json&q=id:A{:d}'.
                            format(seq_id)).json()['results']

        if info is None:
            raise NonExistentSequence(
                'Sequence with the ID {:d} was not found.'.format(seq_id))
        else:
            info = info[0]

        self.seq_id = info['number']
        self.sequence = list(map(int, info['data'].split(',')))

        self.info = {
            'name':
                info['name'],
            'formula':
                '\n'.join(info.get('formula', '')),
            'comments':
                '\n'.join(info.get('comment', '')),
            'example':
                '\n'.join(info.get('example', '')),
            'crossrefs':
                '\n'.join(info.get('xref', '')),
            'keywords':
                info.get('keyword', '').split(','),
            'author':
                info.get('author', '').replace('_', ''),
            'created':
                pendulum.parse(
                    info['created']).astimezone('utc').timestamp(),
            'url':
                'https://oeis.org/A{:06d}'.format(info['number'])
        }

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

    def __eq__(self, other):
        if not isinstance(other, Sequence):
            return False

        return self.seq_id == other.seq_id

    def __str__(self):
        return '<Sequence [A{0:06d}: {1:s}]>'.format(self.seq_id, self.name)

    def __repr__(self):
        return '<Sequence [A{0:06d}: {1:s}]>'.format(self.seq_id, self.name)

    def fetch_sequence(self):
        """Fetch all the values of the sequence from OEIS. Only do this if you
        want a *lot* of values."""

        seq_page = requests.get('https://oeis.org/A{0:d}/b{0:06d}.txt'.format(
            self.seq_id)).text.rstrip('\n').split('\n')
        seq_page = filter(lambda x: not x.startswith('#'), seq_page)
        self.sequence = [int(item.split()[1]) for item in seq_page]

    def contains(self, item):
        """Check if the sequence contains the specified item. Note that this
        has the limit of the amount of numbers that OEIS holds.

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

    def next(self, item):
        """Find the number that comes after the specified number in the
        sequence.

        Positional arguments:
            item (int): the number to find the number after

        Returns the number after item in the sequence.
        """
        return self.sequence[self.find(item) + 1]

    def prev(self, item):
        """Find the number that comes before the specified number in the
        sequence.

        Positional arguments:
            item (int): the number to find the number before

        Returns the number before item in the sequence.
        """
        return self.sequence[self.find(item) - 1]

    def nth_term(self, index):
        """Get the nth element of the sequence. 0-indexed. Raises an exception
        if the index is negative or too high.

        Positional arguments:
            index (int): the index of the element

        Returns the element of the sequence at index.
        """

        if index < 0:
            # sequences don't have negative indices, ya silly goofball
            raise NegativeIndexError(
                'The index passed ({:d}) is negative.'.format(index))

        if index >= len(self):
            # OEIS only holds values up to a certain limit
            raise IndexTooHighError('{0:d} is higher than the amount of '
                                    'values fetched ({1:d}).'.format(
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

        if start < 0:
            raise NegativeIndexError(
                'The index passed ({:d}) is negative.'.format(start))

        if stop < 0:
            raise NegativeIndexError(
                'The index passed ({:d}) is negative.'.format(stop))

        if start > len(self):
            raise IndexTooHighError('{0:d} is higher than the amount of '
                                    'values fetched ({1:d}).'.format(
                                        start, len(self)))

        if stop > len(self):
            raise IndexTooHighError('{0:d} is higher than the amount of '
                                    'values fetched ({1:d}).'.format(
                                        stop, len(self)))

        return self.sequence[start:stop:step]

    def first(self, items):
        """Get the first n terms of the sequence. Raises an exception if n is
        negative or too high.

        Positional arguments:
            items (int): the amount of terms to return

        Returns a list of sequence items.
        """

        return self.subsequence(start = 0, stop = items)


def query(terms, start = None, results = None):
    """Query the OEIS for sequences that match the terms.

    See https://oeis.org/hints.html for more information.

    Positional arguments:
        terms (list): the terms to search for
        start (int): how far down the list of results to return sequences from
                     (default: 0)
        results (int): how many sequences to return (default: 10)

    Returns a list of Sequence objects.
    """

    if not terms:
        raise EmptyQuery('List of query terms passed is empty.')

    if start is None:
        start = 0

    if results is None:
        results = 10

    terms = requests.utils.quote(' '.join(terms))
    result = []
    search = requests.get(
        'https://oeis.org/search?fmt=json&q={0:s}&start={1:d}'.format(
            terms, start)).json()['results']

    if search is None:
        return []

    for seq in search[:results]:  # search results :P
        result.append(Sequence(seq['number']))

    return result

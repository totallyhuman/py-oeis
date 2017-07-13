#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
py-oeis

A Python library to access the OEIS.

Sumant Bhaskaruni
v0.1
"""

import requests


class Sequence(object):
    """An object to represent a single OEIS sequence.

    Initializer arguments:
        number (int): The OEIS sequence ID
    """

    def __init__(self, seq_id):
        """See class docstring for details."""

        self.seq_id = seq_id
        self.val_url = 'https://oeis.org/A{0:d}/b{0:d}.txt'.format(seq_id)
        self.info = requests.get(
            'https://oeis.org/search?fmt=json&q=id:A{:d}'.format(
                seq_id)).json()['results'][0]

        self.name = self.info['name']
        self.author = self.info['author']
        self.created = self.info['created']

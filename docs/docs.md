# py-oeis

A Python library to access the OEIS (Online Encyclopedia of Integer Sequences).

## Sequence

An object to represent a single OEIS sequence.

Initializer arguments:
-   seq_id (int): the OEIS sequence ID

Instance attributes:
-   seq_id (int): the OEIS sequence ID
-   sequence (list): the first few values of the sequence
-   info (dict): information pertaining to the sequence including:
    -   name (str): the name of the sequence
    -   formula (str): the text of the 'Formula' section on OEIS
    -   comments (str): the text of the 'Comments' section on OEIS
    -   example (str): the text of the 'Example' section on OEIS
    -   crossrefs (str): the text of the 'Crossrefs' section on OEIS
    -   keywords (list): the keywords (tags) of the sequence
    -   author (str): the author of the sequence
    -   created (float): when the sequence was created (epoch timestamp)
    -   url (str): the URL of the sequence on OEIS

### fetch\_sequence

`fetch_sequence()`: 

Fetch all the values of the sequence from OEIS. Only do this if you
want a *lot* of values.

### contains

`contains(item)`:

Check if the sequence contains the specified item. Note that this
has the limit of the amount of numbers that OEIS holds.

Positional arguments:
-   item (int): the item to check for

Returns whether the sequence contains item.

### find

`find(item, instances)`: 

Find specified number of instances of the specified item. Note that
this has the limit of the amount of numbers that OEIS hols.

Positional arguments:
-   item (int): the item to find
-   instances (int): the number of instances of item to find
                     (default: 1)

Returns a list of sequence indices.

### next

`next(item)`: 

Find the number that comes after the specified number in the
sequence.

Positional arguments:
-   item (int): the number to find the number after

Returns the number after item in the sequence.

### prev

`prev(item)`: 

Find the number that comes before the specified number in the
sequence.

Positional arguments:
-   item (int): the number to find the number before

Returns the number before item in the sequence.

### nth\_term

`nth_term(index)`: 

Get the nth element of the sequence. 0-indexed. Raises an exception
if the index is negative or too high.

Positional arguments:
-   index (int): the index of the element

Returns the element of the sequence at index.

### subsequence

`subsequence(start, stop, step)`: 

Get a subsequence of the sequence. 0-indexed. Raises an exception if
either of the indices are negative or too high.

Positional arguments:
-   start (int): the starting index of the subsequence (default: 0)
-   stop (int): the ending index of the subsequence (default: len(sequence))
-   step (int): the amount by which the index increases (default: 1)

Returns a list of sequence items.

### first

`first(items)`: 

Get the first n terms of the sequence. Raises an exception if n is
negative or too high.

Positional arguments:
-   items (int): the amount of terms to return

Returns a list of sequence items.

### query

`query(terms, start, results)`: 

Query the OEIS for sequences that match the terms.

See https://oeis.org/hints.html for more information.

Positional arguments:
-   terms (list): the terms to search for
-   start (int): how far down the list of results to return sequences from (default: 0)
-   results (int): how many sequences to return (default: 10)

Returns a list of Sequence objects.


#!/usr/bin/env python

import sys
import re


alpha = 0.85

get_values_string = "v(\d+),(\d*.\d*),(\d*.\d*),?(.*)?"
get_values_regex = re.compile(get_values_string)

key = None
prev_key = None

# Key data is of form iteration, current PageRank, previous PageRank,
# neighbors.
key_data_default = [-1, 1 - alpha, "-1", ""]
key_data = key_data_default[:]


for line in sys.stdin:
    (key, value) = line.split("\t")
    key = key[1:]

    if prev_key is None:
        prev_key = key

    # Found a new key, and since the input is sorted, flush the current key
    # data as the computation is over. "is not None" prevents an empty flush
    # at the beginning.
    if prev_key is not None and key != prev_key:
        sys.stdout.write("%s\t%s\n" % (prev_key, str(key_data)))
        key_data = key_data_default[:]
        prev_key = key

    # This tuple is part of PageRank summation.
    if value[0] is "r":
        key_data[1] += float(value[1:])

    # This tuple contains the other information for the node.
    else:
        value = get_values_regex.match(value).groups()
        # Increase iteration
        key_data[0] = str(int(value[0]) + 1)
        key_data[2] = value[1]
        key_data[3] = value[3]

sys.stdout.write("%s\t%s\n" % (prev_key, str(key_data)))

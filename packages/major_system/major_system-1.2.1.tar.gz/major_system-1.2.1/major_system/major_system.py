#!/usr/bin/env python3

import sys
import re
import itertools
import collections

DEFAULT_DICT_FILENAME = "/usr/share/dict/words"

__doc__ = """
Usage: {} [options] <number>...

<number>...                Numbers to turn into words
                           If -, take <number>... from STDIN.

Options:
  -d, --dict=<filename>    Dictionary file to use
                           [DEFAULT: {}]
  -M, --max-words=<number> Maximum number of words to split into
                           [DEFAULT: 3]
  -m, --min-words=<number> Minimum number of words to split into
                           [DEFAULT: 1]
  -v, --version            Show version
""".format(sys.argv[0], DEFAULT_DICT_FILENAME)

from docopt import docopt


def regex_component(i):
  if i == 0:
    return r'[sSzZ]+'
  if i == 1:
    return r'[tTdD]+'
  if i == 2:
    return r'[nN]+'
  if i == 3:
    return r'[mM]+'
  if i == 4:
    return r'[rR]+'
  if i == 5:
    return r'[lL]+'
  if i == 6:
    return r'(j|J|sh|SH|ch|CH)'
  if i == 7:
    return r'[kKgGcC]+'
  if i == 8:
    return r'[fFvV]+'
  if i == 9:
    return r'[PpBb]+'
  if i == None:
    return r'[AaEeIiOoUuWwHhYy]*'
  raise ValueError("Expected a single digit or None")


def major_words(dictfile, number):
  # If it's something that can only be iterated through once (like a file
  # pointer), reset to the beginning again
  if isinstance(dictfile, collections.Iterator):
    dictfile.seek(0)
  regex = r'^' + regex_component(None)
  for character in str(number):
    regex += regex_component(int(character)) + regex_component(None)
  regex += r'$'
  for line in dictfile:
    if re.match(regex, line):
      yield line.strip()


def phrases_from_partition(dictfile, partition):
  word_collection = []
  for part in partition:
    words = major_words(dictfile, part)
    word_collection.append(words)
  for tup in itertools.product(*word_collection):
    yield " ".join(tup)


def phrases(dictfile, number, max_words=None, min_words=None, *, verbosity=2):
  for partition in partitions(number, max_words, min_words):
    if verbosity > 1:
      for part in partition[:-1]:
        print(part, end=", ")
      print(partition[-1])
    for phrase in phrases_from_partition(dictfile, partition):
      yield phrase


def ordered_tuples(tuple_length, num_elts):
  if tuple_length == 1:
    for i in range(1, num_elts):
      yield (i,)
  else:
    for tup in ordered_tuples(tuple_length - 1, num_elts):
      for i in range(tup[-1] + 1, num_elts):
        yield tup + (i,)


def partitions(arr, max_partitions=None, min_partitions=None):
  arr = str(arr)
  has_max = False
  try:
    has_max = True
    max_partitions = int(max_partitions)
  except (TypeError, ValueError) as e:
    has_max = False
  has_min = False
  try:
    has_min = True
    min_partitions = int(min_partitions)
  except (TypeError, ValueError) as e:
    has_min = False

  if has_max and max_partitions < 1:
    return []
  if has_min and has_max and min_partitions > max_partitions:
    return []
  num_elts = len(arr)

  to_return = []
  # length 1
  if not (has_min and min_partitions > 1):
    to_return = [[arr]]
  # higher lengths
  for partition_length in range(2, num_elts + 1):
    if has_max and partition_length > max_partitions:
      continue
    if has_min and partition_length < min_partitions:
      continue
    tuple_length = partition_length - 1
    for tup in ordered_tuples(tuple_length, num_elts):
      partition = []
      partition.append(arr[0:tup[0]])
      for i in range(0, tuple_length - 1):
        partition.append(arr[tup[i]:tup[i + 1]])
      partition.append(arr[tup[-1]:num_elts])
      to_return.append(partition)
  return to_return


def main():
  args = docopt(__doc__, version='1.2.1')
  dict_filename = args['--dict']
  try:
    with open(dict_filename, 'r') as dictfile:
      for number in args['<number>']:
        print("{}:".format(number))
        for phrase in phrases(dictfile, number, args['--max-words'],
            args['--min-words']):
          print("  " + phrase.strip())
  except FileNotFoundError as e:
    print("Give a file full of words to the -d flag.")
    if dict_filename == DEFAULT_DICT_FILENAME:
      print("(The default location ('{}') doesn't exist "
          "on your system.)".format(dict_filename))
    else:
      print("No file at '{}'.".format(dict_filename))


if __name__ == "__main__":
  main()

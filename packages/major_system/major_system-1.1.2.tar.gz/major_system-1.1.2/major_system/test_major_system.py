from major_system import major_system as ms
import pytest

@pytest.fixture
def dictfile():
  return ['abc', 'dog', 'Cat', 'tag', 'toggle', 'at', 'yell', 'well',
      'what', 'tall', 'deal', 'gill', 'gal', 'ick', 'sail', 'sole',
      'seal']

def assert_equal_except_order(left, right):
  assert len(left) == len(right)
  for i in left:
    assert i in right

def test_partitions():
  assert ms.partitions("a") == [["a"]]
  assert ms.partitions("ab") == [["ab"], ["a", "b"]]
  assert ms.partitions("abc") == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abcd") == [["abcd"], ["a", "bcd"], ["ab", "cd"], ["abc", "d"], ["a", "b", "cd"], ["a", "bc", "d"], ["ab", "c", "d"], ["a", "b", "c", "d"]]
  assert ms.partitions("a", 0) == []
  assert ms.partitions("ab", 1) == [["ab"]]
  assert ms.partitions("abc", 0) == []
  assert ms.partitions("abc", 1) == [["abc"]]
  assert ms.partitions("abc", 2) == [["abc"], ["a", "bc"], ["ab", "c"]]
  assert ms.partitions("abc", 3) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", 4) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", 5) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", 6) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", 7) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abc", None) == [["abc"], ["a", "bc"], ["ab", "c"], ["a", "b", "c"]]
  assert ms.partitions("abcd") == [["abcd"], ["a", "bcd"], ["ab", "cd"], ["abc", "d"], ["a", "b", "cd"], ["a", "bc", "d"], ["ab", "c", "d"], ["a", "b", "c", "d"]]


def test_major_words(dictfile):
  assert [x for x in ms.major_words(dictfile, 17)] == ["dog", 'tag']
  assert [x for x in ms.major_words(dictfile, 175)] == ["toggle"]
  assert [x for x in ms.major_words(dictfile, 8)] == []
  assert [x for x in ms.major_words(dictfile, 5)] == ['yell', 'well']
  assert [x for x in ms.major_words(dictfile, "17")] == ["dog", 'tag']
  assert [x for x in ms.major_words(dictfile, "175")] == ["toggle"]
  assert [x for x in ms.major_words(dictfile, "8")] == []
  assert [x for x in ms.major_words(dictfile, "5")] == ['yell', 'well']
  assert [x for x in ms.major_words(dictfile, "05")] == ['sail', 'sole', 'seal']


def test_phrases_from_partition(dictfile):
  partitions = [[175], [17, 5], [1, 75], [1, 7, 5], [15], [7], [1, 5], [1],
      [5],]
  expected_phrases_list = [
    ['toggle'],
    ['dog yell', 'dog well', 'tag yell', 'tag well'],
    ['at gill', 'at gal', 'what gill', 'what gal'],
    ['at ick yell', 'at ick well', 'what ick yell', 'what ick well'],
    ['tall', 'deal'],
    ['ick'],
    ['at yell', 'at well', 'what yell', 'what well'],
    ['at', 'what'],
    ['yell', 'well'],
  ]
  for partition, expected_phrases in zip(partitions, expected_phrases_list):
    phrases = [x for x in ms.phrases_from_partition(dictfile, partition)]
    assert phrases == expected_phrases
    as_strings = [str(x) for x in partition]
    phrases = [x for x in ms.phrases_from_partition(dictfile, as_strings)]
    assert phrases == expected_phrases


def test_phrases(dictfile):
  for fifteen in [15, '15']:
    phrases = [x for x in ms.phrases(dictfile, fifteen)]
    assert phrases == [
      'tall', 'deal', 'at yell', 'at well', 'what yell', 'what well'
    ]
  
  for one75 in [175, '175']:
    phrases = [x for x in ms.phrases(dictfile, one75)]
    assert set(phrases) == set([
      'toggle',
      'dog yell', 'dog well', 'tag yell', 'tag well',
      'at gill', 'at gal', 'what gill', 'what gal',
      'at ick yell', 'at ick well', 'what ick yell',
      'what ick well',
    ])

  for fifteen in [15, '15']:
    phrases = [x for x in ms.phrases(dictfile, fifteen, 1)]
    assert phrases == [
      'tall', 'deal',
    ]

  for one75 in [175, '175']:
    phrases = [x for x in ms.phrases(dictfile, one75, 3)]
    assert set(phrases) == set([
      'toggle',
      'dog yell', 'dog well', 'tag yell', 'tag well',
      'at gill', 'at gal', 'what gill', 'what gal',
      'at ick yell', 'at ick well', 'what ick yell',
      'what ick well',
    ])
    phrases = [x for x in ms.phrases(dictfile, one75, 2)]
    assert set(phrases) == set([
      'toggle',
      'dog yell', 'dog well', 'tag yell', 'tag well',
      'at gill', 'at gal', 'what gill', 'what gal',
    ])
    phrases = [x for x in ms.phrases(dictfile, one75, 1)]
    assert set(phrases) == set([
      'toggle',
    ])
    phrases = [x for x in ms.phrases(dictfile, one75, 0)]
    assert set(phrases) == set([
    ])

    phrases = [x for x in ms.phrases(dictfile, "705")]
    assert set(phrases) == set([
      'ick sail', 'ick sole', 'ick seal'
    ])

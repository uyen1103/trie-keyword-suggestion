import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Code.trie import Trie

def test_load_from_list_size():

    trie = Trie()

    trie.load_from_list(
        ["apple", "app", "banana"]
    )

    print("Size =", trie.size())

    assert trie.size() == 3


def test_search_case_insensitive():

    trie = Trie()

    trie.insert("Apple")

    print(
        "Search APPLE =",
        trie.search("APPLE")
    )

    print(
        "Search apple =",
        trie.search("apple")
    )

    assert trie.search("APPLE")
    assert trie.search("apple")


def test_prefix_search():

    trie = Trie()

    trie.load_from_list(
        ["apple", "app", "application"]
    )

    result = trie.prefix_search("app")

    print(
        "Prefix search:",
        result
    )

    assert "apple" in result
    assert "app" in result
    assert "application" in result


def test_longest_common_prefix():

    trie = Trie()

    words = [
        "flower",
        "flow",
        "flight"
    ]

    result = trie.longest_common_prefix(
        words
    )

    print(
        "Longest Common Prefix =",
        result
    )

    assert result == "fl"


def test_prefix_not_found():

    trie = Trie()

    trie.load_from_list(
        ["apple", "banana"]
    )

    result = trie.prefix_search("xyz")

    print(
        "Prefix xyz =",
        result
    )

    assert result == []
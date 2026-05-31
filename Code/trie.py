# trie.py
# Trie data structure for keyword storage and prefix lookup

from trie_node import TrieNode


class Trie:

    def __init__(self):
        self.root = TrieNode()

    # INSERT
    def insert(self, word):

        node = self.root

        for char in word:

            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True
        node.word = word

    # SEARCH
    def search(self, word):

        node = self.root

        for char in word:

            if char not in node.children:
                return False

            node = node.children[char]

        return node.is_end

    # PREFIX SEARCH
    def prefix_search(self, prefix, max_results=10):

        node = self.root

        for char in prefix:

            if char not in node.children:
                return []

            node = node.children[char]

        result = []

        self._dfs(node, prefix, result, max_results)

        return result

    # DFS đệ quy trên Trie
    def _dfs(self, node, current_word, result, max_results):

        if len(result) >= max_results:
            return

        if node.is_end:
            result.append(current_word)

        for char, child in node.children.items():
            self._dfs(
                child,
                current_word + char,
                result,
                max_results
            )

# CHIA ĐỂ TRỊ - LONGEST COMMON PREFIX

def common_prefix(str1, str2):

    result = ""

    length = min(len(str1), len(str2))

    for i in range(length):

        if str1[i] == str2[i]:
            result += str1[i]
        else:
            break

    return result


def longest_common_prefix(words, left, right):

    if left == right:
        return words[left]

    mid = (left + right) // 2

    left_lcp = longest_common_prefix(
        words,
        left,
        mid
    )

    right_lcp = longest_common_prefix(
        words,
        mid + 1,
        right
    )

    return common_prefix(
        left_lcp,
        right_lcp
    )

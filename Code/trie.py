# trie.py
# Trie data structure for keyword storage and prefix lookup

from Code.trie_node import TrieNode


class Trie:

    def __init__(self):
        self.root = TrieNode()
        self._size=0;
    
    def size(self)->int:
        return self._size
    
    def load_from_list(self,words: list[str])->int:
        count =0
        for word in words:
            self.insert(word)
            count+=1
        
        return count

    # INSERT
    def insert(self, word):
        word=word.casefold()
        node = self.root

        for char in word:

            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        if not node.is_end:
            self._size+=1

        node.is_end = True
        node.word = word

    # SEARCH
    def search(self, word):
        word=word.casefold()
        node = self.root

        for char in word:

            if char not in node.children:
                return False

            node = node.children[char]

        return node.is_end

    # PREFIX SEARCH
    def prefix_search(self, prefix, max_results=10):
        prefix=prefix.casefold()
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
    # Dung ham public nay khong dung 2 ham duoi
    def longest_common_prefix(self, words):

        if not words:
            return ""

        words = [word.casefold() for word in words]

        return self._longest_common_prefix(
            words,
            0,
            len(words) - 1
        )

    def _common_prefix(self,str1, str2):

        result = ""

        length = min(len(str1), len(str2))

        for i in range(length):

            if str1[i] == str2[i]:
                result += str1[i]
            else:
                break

        return result

    def _longest_common_prefix(self,words, left, right):

        if left == right:
            return words[left]

        mid = (left + right) // 2

        left_lcp = self._longest_common_prefix(
            words,
            left,
            mid
        )

        right_lcp = self._longest_common_prefix(
            words,
            mid + 1,
            right
        )

        return self._common_prefix(
            left_lcp,
            right_lcp
        )

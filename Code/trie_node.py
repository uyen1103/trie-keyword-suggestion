# trie_node.py
# Trie node implementation for keyword suggestion

class TrieNode:

    def __init__(self) -> None:
        self.children: dict = {}
        self.is_end: bool = False
        self.word: str | None = None
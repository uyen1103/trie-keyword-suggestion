# main.py
# Application entry point for trie keyword suggestion

from trie import Trie, longest_common_prefix

# Khởi tạo Trie
trie = Trie()

# 5 từ mẫu
words = [
    "cat",
    "car",
    "camera",
    "camp",
    "call"
]

# ======================
# TEST INSERT
# ======================

for word in words:
    trie.insert(word)

print("Đã thêm từ vào Trie:")
print(words)

# TEST SEARCH

print("\n=== SEARCH ===")

print("cat:", trie.search("cat"))
print("car:", trie.search("car"))
print("camera:", trie.search("camera"))

# không tồn tại
print("dog:", trie.search("dog"))
print("cow:", trie.search("cow"))

# TEST PREFIX SEARCH

print("\n=== PREFIX SEARCH ===")

print("Prefix 'ca':")
print(trie.prefix_search("ca"))

print("\nPrefix 'cam':")
print(trie.prefix_search("cam"))

print("\nPrefix 'car':")
print(trie.prefix_search("car"))

print("\nPrefix 'do':")
print(trie.prefix_search("do"))

# TEST LONGEST COMMON PREFIX

print("\n=== LONGEST COMMON PREFIX ===")

lcp = longest_common_prefix(
    words,
    0,
    len(words) - 1
)

print("LCP =", lcp)
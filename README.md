# Trie Keyword Suggestion

Project gợi ý từ khóa tìm kiếm sử dụng cấu trúc dữ liệu Trie (Prefix Tree).

---

# Kiến trúc hệ thống

<!-- Chèn hình architecture.png tại đây -->

---

# Chức năng

- Prefix Search
- Ranking Suggestions
- Search History
- Top-k Suggestions

---

# Công nghệ

- Python
- CustomTkinter
- SQLite3

---

# Cấu trúc project

```text
TRIE-KEYWORD-SUGGESTION/
│
├── Code/
│   ├── app_controller.py      # Điều phối hệ thống
│   ├── database.py            # Quản lý SQLite Database
│   ├── gui.py                 # Giao diện CustomTkinter
│   ├── main.py                # File chạy chính
│   ├── ranker.py              # Ranking Engine
│   ├── trie.py                # Trie Prefix Search
│   └── trie_node.py           # Trie Node Structure
│
├── Data/
│   └── keywords.txt           # Dataset keyword mẫu
│
├── DB/
│   └── search_history.db      # SQLite Search History
│
├── Docs/
│   ├── architecture.md        # Tài liệu kiến trúc hệ thống
│   └── architecture.png       # Sơ đồ kiến trúc hệ thống
│
├── Tests/
│   └── .gitkeep
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Chạy project

```bash
pip install -r requirements.txt
python Code/main.py
```

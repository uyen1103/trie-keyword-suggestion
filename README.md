# Trie Keyword Suggestion

Xây dựng cấu trúc cây Trie để lưu trữ từ điển. Khi người dùng nhập một tiền tố, hệ thống nhanh chóng liệt kê các từ gợi ý hoặc tìm tiền tố chung dài nhất của một tập hợp các từ.

---

# Kiến trúc hệ thống

![System Architecture](Docs/architecture.png)

---

# Chức năng

- Prefix Search — Nhập tiền tố, gợi ý các từ phù hợp theo thời gian thực
- Longest Common Prefix — Tìm tiền tố chung dài nhất (Chia để trị)
- Ranking Suggestions — Xếp hạng gợi ý theo tần suất + độ mới
- Search History — Lưu lịch sử tìm kiếm bằng SQLite
- Top-K Suggestions — Trả về K gợi ý tốt nhất

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
# 1. Clone project
git clone https://github.com/uyen1103/trie-keyword-suggestion.git
cd trie-keyword-suggestion

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Chạy ứng dụng
python Code/main.py
```

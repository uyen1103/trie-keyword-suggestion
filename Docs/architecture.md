# Interface giữa các module — Trie Keyword Suggestion

> Tài liệu này định nghĩa **tên hàm, tham số, và kiểu trả về** của từng module.  
> Tất cả thành viên phải implement đúng theo đây để AppController kết nối được.

---

## Module 1: `trie_node.py` — TV1

**Mô tả:** Định nghĩa cấu trúc 1 node trong cây Trie.

```python
class TrieNode:

    # Thuộc tính
    children : dict[str, TrieNode]   # các node con, key là ký tự
    is_end   : bool                  # True nếu đây là cuối 1 từ
    word     : str | None            # lưu từ đầy đủ khi is_end = True

    def __init__(self) -> None
```

---

## Module 2: `trie.py` — TV1

**Mô tả:** Cấu trúc cây Trie, hỗ trợ tiếng Việt và tiếng Anh (Unicode NFC).

```python
class Trie:

    def __init__(self) -> None
    # Tạo cây Trie rỗng với 1 node gốc.

    def insert(self, word: str) -> None
    # Thêm 1 từ vào Trie.
    # Input : word — chuỗi bất kỳ (tiếng Việt, tiếng Anh)
    # Output: None
    # Lưu ý: tự động normalize NFC + casefold trước khi insert.
    # Độ phức tạp: O(m), m = số ký tự của word.

    def load_from_list(self, words: list[str]) -> int
    # Nạp toàn bộ danh sách từ vào Trie.
    # Input : words — danh sách từ/cụm từ
    # Output: số từ được thêm mới vào Trie
    # Gọi khi khởi động app để load từ điển.

    def search(self, word: str) -> bool
    # Kiểm tra từ đầy đủ có tồn tại trong Trie không.
    # Input : word — từ cần kiểm tra
    # Output: True nếu tồn tại đầy đủ, False nếu chỉ là tiền tố
    # Ví dụ: search("tìm") = False khi chỉ có "tìm kiếm" trong Trie.
    # Độ phức tạp: O(m)

    def prefix_search(self, prefix: str, max_results: int = 10) -> list[str]
    # Liệt kê các từ có cùng tiền tố — hàm quan trọng nhất.
    # Input : prefix      — tiền tố người dùng nhập
    #         max_results — số kết quả tối đa trả về
    # Output: list[str] — danh sách từ có tiền tố, tối đa max_results phần tử
    # Chiến lược: DFS đệ quy (Chương 3)
    # Độ phức tạp: O(m + k), k = số node trong cây con cần duyệt

    def longest_common_prefix(self, words: list[str]) -> str
    # Tìm tiền tố chung dài nhất của một danh sách từ.
    # Input : words — danh sách từ cần tìm
    # Output: str — tiền tố chung dài nhất, '' nếu không có
    # Chiến lược: Chia để trị (Chương 4) — T(n) = 2T(n/2) + O(m)
    # Ví dụ: ["python","pytorch","pytest"] → "py"
    # Ví dụ: ["tìm kiếm","tìm kiếm tiếng việt"] → "tìm kiếm"

    def size(self) -> int
    # Trả về tổng số từ đang lưu trong Trie.
    # Output: int
```

---

## Module 3: `database.py` — TV3

**Mô tả:** Quản lý SQLite — lưu lịch sử tìm kiếm và tần suất từ khóa.

```python
class DatabaseManager:

    def __init__(self, db_path: Path = DB_PATH) -> None
    # Khởi tạo kết nối SQLite, tự động tạo bảng nếu chưa có.
    # Input : db_path — đường dẫn file .db
    #                   mặc định: DB/search_history.db

    def add_keyword(self, keyword: str) -> None
    # Thêm từ khóa mới vào DB với frequency = 1.
    # Nếu từ đã tồn tại thì bỏ qua (INSERT OR IGNORE).
    # Input : keyword — từ cần thêm

    def save_search(self, keyword: str) -> None
    # Gọi khi người dùng chọn 1 gợi ý.
    # Nếu từ chưa có → INSERT frequency = 1.
    # Nếu từ đã có   → UPDATE frequency += 1, cập nhật last_searched.
    # Input : keyword — từ người dùng vừa chọn

    def get_frequency(self, keyword: str) -> int
    # Lấy số lần tìm kiếm của 1 từ.
    # Input : keyword — từ cần kiểm tra
    # Output: int — trả về 0 nếu từ chưa có trong DB

    def get_last_searched(self, keyword: str) -> str | None
    # Lấy thời điểm tìm kiếm gần nhất của 1 từ.
    # Input : keyword
    # Output: str (ISO format timestamp) hoặc None nếu chưa có

    def load_all_keywords(self) -> list[str]
    # Đọc toàn bộ từ khóa từ DB, dùng để nạp vào Trie khi khởi động.
    # Output: list[str] — sắp xếp theo frequency giảm dần

    def get_all_data(self, keywords: list[str]) -> list[dict]
    # Lấy thông tin frequency + last_searched của nhiều từ cùng lúc.
    # Dùng bởi AppController để chuẩn bị dữ liệu cho Ranker.
    # Input : keywords — danh sách từ cần lấy dữ liệu
    # Output: list[dict], mỗi phần tử có dạng:
    #         { "keyword": str, "frequency": int, "last_searched": str }

    def get_history(self, limit: int = 10) -> list[dict]
    # Lấy lịch sử tìm kiếm gần nhất.
    # Input : limit — số bản ghi tối đa cần lấy
    # Output: list[dict] — sắp xếp theo last_searched giảm dần
    #         mỗi phần tử: { "keyword": str, "frequency": int, "last_searched": str }

    def import_from_file(self, filepath: str) -> int
    # Đọc file keywords.txt (1 từ mỗi dòng) rồi INSERT vào DB.
    # Dùng khi DB còn trống lần đầu chạy chương trình.
    # Input : filepath — đường dẫn tới file txt
    # Output: int — số từ đã import thành công

    def export_history(self, filepath: str) -> None
    # Xuất lịch sử tìm kiếm ra file CSV.
    # Input : filepath — đường dẫn file CSV cần ghi

    def reset(self) -> None
    # Xóa toàn bộ dữ liệu trong bảng search_history.
    # Dùng khi cần reset lại cho demo.
```

---

## Module 4: `ranker.py` — TV4

**Mô tả:** Xếp hạng danh sách gợi ý theo tần suất và độ mới.

```python
class SuggestionRanker:

    def __init__(self, w_freq: float = 0.7, w_rec: float = 0.3) -> None
    # Khởi tạo Ranker với 2 trọng số.
    # w_freq : trọng số cho tần suất (mặc định 70%)
    # w_rec  : trọng số cho độ mới   (mặc định 30%)
    # Yêu cầu: w_freq + w_rec = 1.0
    # Công thức: score = w_freq × freq_score + w_rec × recency_score

    def rank(self, words: list[str], db_data: list[dict]) -> list[str]
    # Xếp hạng toàn bộ danh sách từ theo weighted score.
    # Input : words   — danh sách gợi ý lấy từ Trie.starts_with()
    #         db_data — list[dict] từ DatabaseManager.get_all_data()
    #                   mỗi dict: { "keyword": str, "frequency": int, "last_searched": str }
    # Output: list[str] — danh sách đã sắp xếp theo score giảm dần

    def get_top(self, words: list[str], db_data: list[dict], top_k: int = 5) -> list[str]
    # Xếp hạng rồi trả về top_k từ tốt nhất.
    # Input : words, db_data — giống hàm rank()
    #         top_k          — số gợi ý muốn lấy
    # Output: list[str] — tối đa top_k phần tử

    def explain(self, word: str, db_data: list[dict]) -> str
    # Giải thích điểm của 1 từ — dùng khi debug hoặc demo.
    # Input : word    — từ cần xem điểm
    #         db_data — dữ liệu từ DB
    # Output: str — ví dụ: "python: score=0.85 (freq=0.70, rec=0.45)"
```

---

## Module 5: `gui.py` — TV2

**Mô tả:** Giao diện người dùng bằng CustomTkinter.

```python
class MainWindow(ctk.CTk):

    def __init__(
        self,
        search_callback  : Callable[[str], list[str]],
        select_callback  : Callable[[str], None],
        stats_callback   : Callable[[], dict] | None = None,
        history_callback : Callable[[], list[dict]] | None = None
    ) -> None
    # Tạo cửa sổ chính, nhận các callback từ AppController.
    # search_callback  : nhận prefix → trả về list gợi ý đã xếp hạng
    # select_callback  : nhận word   → lưu vào DB (tăng frequency)
    # stats_callback   : không tham số → trả về {"total_words": int, "top_k": int}
    # history_callback : không tham số → trả về list[dict] lịch sử tìm kiếm

    # Các hàm nội bộ (TV2 tự implement, các TV khác không cần gọi):
    def _build_ui(self) -> None
    # Dựng toàn bộ widget: tiêu đề, ô nhập, frame gợi ý, status bar.

    def _on_key_release(self, event) -> None
    # Gọi mỗi khi người dùng nhả phím trong ô nhập.
    # Lấy prefix từ ô nhập → gọi search_callback → hiển thị kết quả.

    def _update_suggestions(self, suggestions: list[str], prefix: str) -> None
    # Xóa danh sách cũ và render danh sách gợi ý mới.
    # Input : suggestions — list từ gợi ý
    #         prefix      — tiền tố hiện tại để highlight

    def _on_select(self, word: str) -> None
    # Gọi khi người dùng click chọn 1 gợi ý.
    # Điền từ vào ô nhập, gọi select_callback(word).

    def _clear_input(self) -> None
    # Xóa ô nhập và reset danh sách gợi ý.

    def _update_status(self) -> None
    # Cập nhật status bar: hiển thị tổng số từ và top_k.
```

---

## Module 6: `app_controller.py` — TV5

**Mô tả:** Điều phối toàn bộ luồng — kết nối Trie, DB, Ranker với GUI.

```python
class AppController:

    def __init__(self, top_k: int = 5, data_path: Path = DATA_PATH) -> None
    # Khởi tạo theo thứ tự: DB → Trie → Ranker → load dữ liệu.
    # top_k     : số gợi ý tối đa trả về cho GUI
    # data_path : đường dẫn file keywords.txt làm từ điển mặc định

    def search(self, prefix: str) -> list[str]
    # Hàm tìm kiếm chính — GUI gọi hàm này mỗi khi người dùng gõ.
    # Input : prefix — tiền tố người dùng đang nhập
    # Output: list[str] — top_k từ đã được xếp hạng
    # Luồng bên trong:
    #   1. Trie.prefix_search(prefix, max=50)     → candidates
    #   2. DB.get_all_data(candidates)           → db_data
    #   3. Ranker.get_top(candidates, db_data)   → top_k kết quả

    def on_select(self, word: str) -> None
    # Gọi khi người dùng chọn 1 gợi ý từ danh sách.
    # Input : word — từ người dùng vừa chọn
    # Bên trong: DB.save_search(word) — tăng frequency lên 1.

    def get_lcp(self, prefix: str) -> str
    # Tìm tiền tố chung dài nhất của tất cả gợi ý hiện tại.
    # Input : prefix — tiền tố đang gõ
    # Output: str — LCP tính bằng Chia để trị (Trie.longest_common_prefix)

    def get_history(self, limit: int = 10) -> list[dict]
    # Lấy lịch sử tìm kiếm gần nhất để GUI hiển thị.
    # Input : limit — số bản ghi tối đa
    # Output: list[dict] từ DB.get_history()

    def stats(self) -> dict
    # Trả về thông tin thống kê cho status bar của GUI.
    # Output: dict — { "total_words": int, "top_k": int }
```

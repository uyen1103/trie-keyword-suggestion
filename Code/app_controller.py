# app_controller.py
# Controller logic for trie keyword suggestion app

from pathlib import Path

from .trie import Trie
from .database import DatabaseManager
from .ranker import SuggestionRanker

DATA_PATH = Path("Data/keywords.txt")


class AppController:

    def __init__(self, top_k: int = 5, data_path: Path = DATA_PATH):
        self.top_k = top_k

        self.db = DatabaseManager()
        self.trie = Trie()
        self.ranker = SuggestionRanker()

        # Load từ khóa từ DB vào Trie khi khởi động
        keywords = self.db.load_all_keywords()
        self.trie.load_from_list(keywords)

        # Nếu DB còn trống, import từ file keywords.txt
        if not keywords and data_path.exists():
            self.db.import_from_file(str(data_path))
            keywords = self.db.load_all_keywords()
            self.trie.load_from_list(keywords)

    def search(self, prefix: str) -> list[str]:
        # Tìm kiếm và xếp hạng kết quả
        if not prefix or not prefix.strip():
            return []
        candidates = self.trie.prefix_search(prefix, max_results=50)
        db_data = self.db.get_all_data(candidates)
        return self.ranker.get_top(candidates, db_data, top_k=self.top_k)

    def on_select(self, word: str) -> None:
        # Cập nhật tần suất khi người dùng chọn từ khóa
        self.db.save_search(word)

    def get_lcp(self, prefix: str) -> str:
        # Tìm tiền tố chung dài nhất của tất cả gợi ý hiện tại
        # Dùng Trie.longest_common_prefix (Chia để trị)
        candidates = self.trie.prefix_search(prefix, max_results=50)
        if not candidates:
            return prefix
        return self.trie.longest_common_prefix(candidates)

    def get_history(self, limit: int = 10) -> list[dict]:
        # Lấy lịch sử tìm kiếm gần nhất để GUI hiển thị
        return self.db.get_history(limit=limit)

    def stats(self) -> dict:
        # Trả về thông tin thống kê cho status bar của GUI
        return {
            "total_words": self.trie.size(),
            "top_k": self.top_k
        }
    def close(self) -> None:
        """Đóng kết nối DB khi tắt app."""
        self.db.close()
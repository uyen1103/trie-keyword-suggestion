import sqlite3
import csv
from pathlib import Path
from datetime import datetime

class DatabaseManager:

    def __init__(self, db_path: Path = Path('DB/search_history.db')) -> None:
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        try:
            self.cursor.execute(''' CREATE TABLE IF NOT EXISTS search_history(
                id INTEGER PRIMARY KEY,
                keyword TEXT NOT NULL UNIQUE,
                frequency INTEGER DEFAULT 1,
                last_searched DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"DB error in _create_table: {e}")

    def add_keyword(self, keyword: str) -> None:
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO search_history (keyword)
                VALUES (?)
            """, (keyword,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"DB error in add_keyword: {e}")

    def get_frequency(self, keyword: str) -> int:
        try:
            self.cursor.execute(
                "SELECT frequency FROM search_history WHERE keyword = ?",
                (keyword,)
            )
            result = self.cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"DB error in get_frequency: {e}")
            return 0

    def get_last_searched(self, keyword: str) -> str | None:
        try:
            self.cursor.execute(
                "SELECT last_searched FROM search_history WHERE keyword = ?",
                (keyword,)
            )
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"DB error in get_last_searched: {e}")
            return None

    def save_search(self, keyword: str) -> None:
        try:
            self.cursor.execute("""
                INSERT INTO search_history (keyword, frequency, last_searched)
                VALUES (?, 1, CURRENT_TIMESTAMP)
                ON CONFLICT(keyword) DO UPDATE SET
                    frequency = frequency + 1,
                    last_searched = CURRENT_TIMESTAMP
            """, (keyword,))
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"DB error in save_search: {e}")

    def load_all_keywords(self) -> list[str]:
        try:
            self.cursor.execute(
                "SELECT keyword FROM search_history ORDER BY frequency DESC"
            )
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"DB error in load_all_keywords: {e}")
            return []

    def get_all_data(self, keywords: list[str]) -> list[dict]:
        if not keywords:
            return []
        try:
            placeholders = ",".join(["?" for _ in keywords])
            self.cursor.execute(
                f"SELECT keyword, frequency, last_searched FROM search_history WHERE keyword IN ({placeholders})",
                keywords
            )
            return [
                {
                    "keyword": row[0], 
                    "frequency": row[1], 
                    "last_searched": datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S") if row[2] else datetime.now()
                }
                for row in self.cursor.fetchall()
            ]
        except sqlite3.Error as e:
            print(f"DB error in get_all_data: {e}")
            return []

    def get_history(self, limit: int = 10) -> list[dict]:
        try:
            self.cursor.execute(
                "SELECT keyword, frequency, last_searched FROM search_history ORDER BY last_searched DESC LIMIT ?",
                (limit,)
            )
            return [
                {"keyword": row[0], "frequency": row[1], "last_searched": row[2]}
                for row in self.cursor.fetchall()
            ]
        except sqlite3.Error as e:
            print(f"DB error in get_history: {e}")
            return []

    def import_from_file(self, filepath: str) -> int:
        count = 0
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    keyword = line.strip()
                    if not keyword or keyword.startswith("#"):
                        continue
                    self.add_keyword(keyword)
                    count += 1
        except OSError as e:
            print(f"File error in import_from_file: {e}")
        except sqlite3.Error as e:
            print(f"DB error in import_from_file: {e}")
        return count
    
    def export_history(self, filepath: str) -> None:
        """Xuất lịch sử tìm kiếm ra file CSV."""
        try:
            rows = self.get_history(limit=10000)
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["keyword", "frequency", "last_searched"]
                )
                writer.writeheader()
                writer.writerows(rows)
        except Exception as e:
            print(f"Error in export_history: {e}")
 
    def reset(self) -> None:
        """Xóa toàn bộ dữ liệu trong bảng search_history."""
        try:
            self.cursor.execute("DELETE FROM search_history")
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"DB error in reset: {e}")
 
    def close(self) -> None:
        """Đóng kết nối SQLite."""
        try:
            self.connection.close()
        except Exception as e:
            print(f"Error in close: {e}")

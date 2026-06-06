import sqlite3
from pathlib import Path
class DatabaseManager:

    def __init__(self, db_path: Path = Path('DB/search_history.db')) -> None:
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    # tạo bảng
    def _create_table(self):
        self.cursor.execute(''' CREATE TABLE IF NOT EXISTS search_history(
    id INTEGER PRIMARY KEY,
    keyword TEXT NOT NULL UNIQUE,                     
    frequency INTEGER DEFAULT 1,                      
    last_searched DATETIME DEFAULT CURRENT_TIMESTAMP, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP     
    )''');
        self.connection.commit()
    
    def add_keyword(self, keyword: str) -> None:
        self.cursor.execute("""
            INSERT OR IGNORE INTO search_history (keyword) 
            VALUES (?)                           
            """, (keyword,))

        self.connection.commit()

    def get_frequency(self, keyword: str) -> int:
        self.cursor.execute("SELECT frequency FROM search_history WHERE keyword = ?", (keyword,))
        result = self.cursor.fetchone()

        return result[0] if result else 0

    def save_search(self, keyword: str) -> None:
        self.cursor.execute("""
            INSERT INTO search_history (keyword, frequency, last_searched)
            VALUES (?, 1, CURRENT_TIMESTAMP)
            ON CONFLICT(keyword) DO UPDATE SET
                frequency = frequency + 1,
                last_searched = CURRENT_TIMESTAMP
        """, (keyword,))

        self.connection.commit()

    def load_all_keywords(self) -> list[str]:
        self.cursor.execute("SELECT keyword FROM search_history ORDER BY frequency DESC")
        return [row[0] for row in self.cursor.fetchall()]

    def get_all_data(self, keywords: list[str]) -> list[dict]:
        if not keywords:
            return []
    
        placeholders = ",".join(["?" for _ in keywords])
        self.cursor.execute(
            f"SELECT keyword, frequency, last_searched FROM search_history WHERE keyword IN ({placeholders})",
        keywords
        )
    
        return [
            {"keyword": row[0], "frequency": row[1], "last_searched": row[2]}
            for row in self.cursor.fetchall()
        ]
    
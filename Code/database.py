import sqlite3
from pathlib import Path
class DatabaseManager:

    def __init__(self, db_path: Path = Path('DB/search_history.db')):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def add_keyword(self, keyword: str):
        self.cursor.execute("""
            INSERT OR IGNORE INTO search_history (keyword) 
            VALUES (?)                           
            """, (keyword,))

        self.connection.commit()
        
    def get_frequency(self, keyword: str):
        self.cursor.execute("SELECT frequency FROM search_history WHERE keyword = ?", (keyword,))
        result = self.cursor.fetchone()

        return result[0] if result else 0
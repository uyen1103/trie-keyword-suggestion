import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Code.database import DatabaseManager

# chạy test case trong RAM
def get_test_db():
    return DatabaseManager(db_path=":memory:")


def test_add_keyword_no_duplicate():
    db = get_test_db()
    db.add_keyword("python")
    db.add_keyword("python")

    result = db.get_frequency("python")
    print("Frequency after 2 add_keyword:", result)

    assert result == 1


def test_save_search_increases_frequency():
    db = get_test_db()
    db.save_search("python")
    db.save_search("python")
    db.save_search("python")

    result = db.get_frequency("python")
    print("Frequency after 3 save_search:", result)

    assert result == 3


def test_get_frequency_correct():
    db = get_test_db()
    db.save_search("python")
    db.save_search("python")
    db.save_search("java")

    freq_python = db.get_frequency("python")
    freq_java = db.get_frequency("java")
    print("Frequency python:", freq_python, "| java:", freq_java)

    assert freq_python == 2
    assert freq_java == 1


def test_load_all_keywords_order():
    db = get_test_db()
    db.save_search("python")
    db.save_search("python")
    db.save_search("java")
    db.save_search("c++")
    db.save_search("c++")
    db.save_search("c++")

    keywords = db.load_all_keywords()
    print("Keywords order:", keywords)

    assert keywords == ["c++", "python", "java"]


def test_get_all_data_format():
    db = get_test_db()
    db.save_search("python")

    result = db.get_all_data(["python"])
    print("Result:", result)

    assert len(result) == 1
    assert result[0]["keyword"] == "python"
    assert result[0]["frequency"] == 1
    assert "last_searched" in result[0]


# Test trên DB thật — mỗi test xóa sạch trước, giữ data sau

# gỡ comment từ dưới xuống cùng và comment ở phía trên
#
# import sqlite3
# from pathlib import Path

# REAL_DB = Path(__file__).resolve().parent.parent / "DB" / "search_history.db"

# SQL_CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS search_history(
#     id INTEGER PRIMARY KEY,
#     keyword TEXT NOT NULL UNIQUE,
#     frequency INTEGER DEFAULT 1,
#     last_searched DATETIME DEFAULT CURRENT_TIMESTAMP,
#     created_at DATETIME DEFAULT CURRENT_TIMESTAMP
# )'''

# def get_real_db():
#     conn = sqlite3.connect(REAL_DB)
#     cur = conn.cursor()
#     cur.execute(SQL_CREATE_TABLE)
#     conn.commit()

#     class DB:
#         pass

#     db = DB()
#     db.connection = conn
#     db.cursor = cur
#     return db


# def test_real_add_keyword_no_duplicate():
#     db = get_real_db()
#     db.cursor.execute("DELETE FROM search_history")
#     db.connection.commit()

#     db.cursor.execute("INSERT OR IGNORE INTO search_history (keyword) VALUES (?)", ("python",))
#     db.connection.commit()
#     db.cursor.execute("INSERT OR IGNORE INTO search_history (keyword) VALUES (?)", ("python",))
#     db.connection.commit()

#     db.cursor.execute("SELECT COUNT(*) FROM search_history WHERE keyword = 'python'")
#     count = db.cursor.fetchone()[0]
#     print("Count python:", count)

#     assert count == 1
#     db.connection.close()


# def test_real_save_search_increases_frequency():
#     db = get_real_db()
#     db.cursor.execute("DELETE FROM search_history")
#     db.connection.commit()

#     for _ in range(3):
#         db.cursor.execute("""
#             INSERT INTO search_history (keyword, frequency, last_searched)
#             VALUES (?, 1, CURRENT_TIMESTAMP)
#             ON CONFLICT(keyword) DO UPDATE SET
#                 frequency = frequency + 1,
#                 last_searched = CURRENT_TIMESTAMP
#         """, ("python",))
#     db.connection.commit()

#     db.cursor.execute("SELECT frequency FROM search_history WHERE keyword = 'python'")
#     freq = db.cursor.fetchone()[0]
#     print("Frequency:", freq)

#     assert freq == 3
#     db.connection.close()


# def test_real_get_frequency_correct():
#     db = get_real_db()
#     db.cursor.execute("DELETE FROM search_history")
#     db.connection.commit()

#     db.cursor.execute("INSERT OR IGNORE INTO search_history (keyword) VALUES (?)", ("python",))
#     db.cursor.execute("INSERT OR IGNORE INTO search_history (keyword) VALUES (?)", ("java",))
#     db.connection.commit()

#     db.cursor.execute("""
#         INSERT INTO search_history (keyword, frequency, last_searched)
#         VALUES ('python', 1, CURRENT_TIMESTAMP)
#         ON CONFLICT(keyword) DO UPDATE SET frequency = frequency + 1
#     """)
#     db.connection.commit()

#     db.cursor.execute("SELECT frequency FROM search_history WHERE keyword = 'python'")
#     freq_python = db.cursor.fetchone()[0]

#     db.cursor.execute("SELECT frequency FROM search_history WHERE keyword = 'java'")
#     freq_java = db.cursor.fetchone()[0]

#     print("Frequency python:", freq_python, "| java:", freq_java)

#     assert freq_python == 2
#     assert freq_java == 1
#     db.connection.close()


# def test_real_load_all_keywords_order():
#     db = get_real_db()
#     db.cursor.execute("DELETE FROM search_history")
#     db.connection.commit()

#     for kw in ["python", "python", "java", "c++", "c++", "c++"]:
#         db.cursor.execute("""
#             INSERT INTO search_history (keyword, frequency, last_searched)
#             VALUES (?, 1, CURRENT_TIMESTAMP)
#             ON CONFLICT(keyword) DO UPDATE SET
#                 frequency = frequency + 1,
#                 last_searched = CURRENT_TIMESTAMP
#         """, (kw,))
#     db.connection.commit()

#     db.cursor.execute("SELECT keyword FROM search_history ORDER BY frequency DESC")
#     keywords = [row[0] for row in db.cursor.fetchall()]
#     print("Keywords order:", keywords)

#     assert keywords == ["c++", "python", "java"]
#     db.connection.close()


# def test_real_get_all_data_format():
#     db = get_real_db()
#     db.cursor.execute("DELETE FROM search_history")
#     db.connection.commit()

#     db.cursor.execute("""
#         INSERT INTO search_history (keyword, frequency, last_searched)
#         VALUES (?, 1, CURRENT_TIMESTAMP)
#     """, ("python",))
#     db.connection.commit()

#     db.cursor.execute("SELECT keyword, frequency, last_searched FROM search_history WHERE keyword = 'python'")
#     row = db.cursor.fetchone()
#     result = {"keyword": row[0], "frequency": row[1], "last_searched": row[2]}
#     print("Result:", result)

#     assert result["keyword"] == "python"
#     assert result["frequency"] == 1
#     assert result["last_searched"] is not None
#     db.connection.close()

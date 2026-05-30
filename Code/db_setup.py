import sqlite3

connect = sqlite3.connect('DB/search_history.db')

cursor = connect.cursor()

# Tạo bảng search_history nếu chưa tồn tại
cursor.execute(''' CREATE TABLE IF NOT EXISTS search_history(
    id INTEGER PRIMARY KEY,
    keyword TEXT NOT NULL UNIQUE,                     
    frequency INTEGER DEFAULT 1,                      
    last_searched DATETIME DEFAULT CURRENT_TIMESTAMP, 
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP     
)''');
# Tạo UNIQUE để phục vụ UPSERT
# Mặc định là 1 lần tìm kiếm
# Cập nhật mỗi khi tìm lại
# Chỉ lưu thời gian tạo lần đầu

connect.commit()

# INSERT
sample_keyword = ['iphone', 'ipad', 'imac', 'iphone']
for word in sample_keyword:
    cursor.execute("""
        INSERT INTO search_history (keyword) 
        VALUES (?)                           
        ON CONFLICT(keyword) DO UPDATE SET   
            frequency = frequency + 1,
            last_searched = CURRENT_TIMESTAMP;
        """, (word,))
    
    # chỉ định chính xác cột keyword 
    # sử dụng placeholder để tránh SQL injection
    # UPSERT: nếu keyword đã tồn tại thì cập nhật frequency và last_searched

    connect.commit()

# QUERY
cursor.execute("SELECT id, keyword, frequency, last_searched FROM search_history")
records = cursor.fetchall()

#test print
for row in records:
        print(f" - ID: {row[0]} | Từ khóa: '{row[1]}' | Số lần tìm: {row[2]} | Thời gian: {row[3]}")

# DROP TABLE 
# cursor.execute("DROP TABLE IF EXISTS search_history")
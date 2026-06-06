# Nghiên cứu SQLite và module SQLite3 của python

## 1. SQLite là gì?

SQLite là một hệ quản trị cơ sở dữ liệu quan hệ (Relational Database Management System - RDBMS) mã nguồn mở được phát triển bởi Richard Hipp vào năm 2000. Khác với các hệ quản trị cơ sở dữ liệu truyền thống hoạt động theo mô hình client-server, SQLite sử dụng kiến trúc serverless, trong đó toàn bộ dữ liệu được lưu trữ trong một tệp duy nhất trên hệ thống.

---

### Đặc điểm nổi bật của SQLite

- Không cần cài đặt hoặc cấu hình máy chủ.
- Kích thước nhỏ gọn và tiêu thụ ít tài nguyên.
- Hỗ trợ hầu hết các câu lệnh SQL chuẩn.
- Tính di động cao do dữ liệu được lưu trong một tệp duy nhất.
- Hiệu suất tốt đối với các ứng dụng quy mô nhỏ và trung bình.
- Hoạt động ổn định trên nhiều hệ điều hành khác nhau.

### Ưu điểm

- Dễ sử dụng và triển khai.
- Miễn phí và mã nguồn mở.
- Thích hợp cho các ứng dụng nhúng, ứng dụng desktop và thiết bị di động.
- Không yêu cầu quản trị cơ sở dữ liệu chuyên nghiệp.

### Hạn chế

- Khả năng xử lý đồng thời nhiều kết nối còn hạn chế.
- Không phù hợp với hệ thống có lượng truy cập lớn.
- Thiếu một số tính năng nâng cao của các DBMS doanh nghiệp.

## 2. Module sqlite3 trong Python

Module `SQLite3` là thư viện chuẩn được cung cấp trong **Python** nhằm hỗ trợ kết nối và thao tác với cơ sở dữ liệu SQLite. Thông qua module này, lập trình viên có thể tạo cơ sở dữ liệu, xây dựng bảng dữ liệu, thực hiện các thao tác **CRUD**(Create, Read, Update, Delete) và quản lý giao dịch một cách thuận tiện.

### Các thành phần chính

```python
# Kết nối cơ sở dữ liệu

import sqlite3

    connect = sqlite3.connect("database.db") # Lệnh trên tạo hoặc mở tệp cơ sở dữ liệu SQLite.

# Đối tượng Cursor

    cursor = connect.cursor() # Cursor được sử dụng để thực thi các câu lệnh SQL.

# Thực thi câu lệnh SQL

    cursor.execute()

# Lưu thay đổi

    connect.commit()

#Đóng kết nối

    connect.close()
```

## 3. Các thao tác cơ bản với sqlite3

```python
# tạo bảng
Thực thi câu lệnh SQL
    cursor.execute("""CREATE TABLE IF NOT EXISTS Student( Student_id INTEGER PRIMARY KEY, Name TEXT, Age INTEGER)""")

# Xóa bảng
    cursor.execute("DROP TABLE IF EXISTS Student")

# Thêm dữ liệu
    cursor.execute("INSERT INTO Student(id, name, age) VALUES (Student_id=?, Name=?, Age=?) # nhập thông tin cần nhập vào hàm VALUES
## ví dụ
    cursor.execute("INSERT INTO Student VALUES (001, "Nguyen Van A", 20))
    cursor.execute("INSERT INTO Student VALUES (002, "Nguyen Van B", 18))
    cursor.execute("INSERT INTO Student VALUES (003, "Nguyen Van C", 29))
    connect.commit()

# Truy vấn dữ liệu
    cursor.execute("SELECT * FROM Student")
    result = cursor.fetchall()

    print(result) # [(001, "Nguyen Van A", 20), (002, "Nguyen Van B", 18), (003, "Nguyen Van C", 29)]

# Cập nhật dữ liệu
    cursor.execute("UPDATE Student SET age=? WHERE id=?") # cập nhật dữ liệu cần thay đổi
## ví dụ
    cursor.execute("UPDATE Student SET age=20 WHERE id=002")
    # result [(002, "Nguyen Van B", 18)] => [(002, "Nguyen Van B", 20)]

#Xóa dữ liệu
    cursor.execute("DELETE FROM Student WHERE id=?") # xóa dữ liệu không cần thiết hoặc không còn tồn tại
## ví dụ
    cursor.execute("DELETE FROM Student WHERE id=003")
    # result dữ liệu Student(003, "Nguyen Van C", 29) đã được xóa
```

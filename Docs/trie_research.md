# Trie Research

## 1. Nghiên cứu cấu trúc Trie: Node, Edge, Prefix

### Trie là gì?

Trie (Prefix Tree) là cấu trúc dữ liệu dạng cây được sử dụng để lưu trữ và tìm kiếm chuỗi ký tự hiệu quả, đặc biệt phù hợp cho các hệ thống gợi ý từ khóa tìm kiếm (Autocomplete).

Mỗi đường đi từ node gốc đến một node bất kỳ biểu diễn một tiền tố (prefix), còn đường đi đến node kết thúc biểu diễn một từ hoàn chỉnh.

---

### Node

Node là thành phần cơ bản của Trie.

Mỗi node gồm:

* `children`: lưu các node con.
* `is_end_of_word`: đánh dấu đây có phải là node kết thúc một từ hay không.

Ví dụ:

```text
(root)
 |
 c
 |
 a
 / \
 t   r
```

Trong ví dụ trên:

* Node `c` là con của root.
* Node `a` là con của `c`.
* Node `t` và `r` là các node con của `a`.

---

### Edge

Edge là cạnh nối giữa hai node.

Ví dụ:

```text
root -> c
c -> a
a -> t
```

Mỗi edge tương ứng với một ký tự trong từ.

---

### Prefix

Prefix là tiền tố chung của một hoặc nhiều từ.

Ví dụ:

```text
cat
car
camera
camp
call
```

Các từ trên đều có chung tiền tố:

```text
ca
```

Do đó `ca` là một prefix.

---

## 2. Tìm hiểu các thao tác cơ bản

### Insert (Chèn từ)

Chức năng:

* Thêm một từ mới vào Trie.
* Nếu node tương ứng chưa tồn tại thì tạo mới.
* Đánh dấu node cuối là kết thúc từ.

Ví dụ chèn từ:

```text
cat
```

Trie sẽ có dạng:

```text
(root)
 |
 c
 |
 a
 |
 t*
```

Dấu `*` biểu thị kết thúc một từ hoàn chỉnh.

#### Độ phức tạp

```text
O(m)
```

Trong đó:

* `m` là độ dài từ cần chèn.

---

### Search (Tìm kiếm từ)

Chức năng:

* Kiểm tra một từ có tồn tại trong Trie hay không.

Ví dụ:

```python
search("cat")
```

Kết quả:

```python
True
```

Ví dụ:

```python
search("dog")
```

Kết quả:

```python
False
```

#### Nguyên lý

* Duyệt từng ký tự từ node gốc.
* Nếu không tồn tại cạnh tương ứng thì trả về `False`.
* Nếu đến node cuối và node đó được đánh dấu kết thúc từ thì trả về `True`.

#### Độ phức tạp

```text
O(m)
```

---

### Prefix Search (Gợi ý theo tiền tố)

Chức năng:

* Liệt kê tất cả các từ bắt đầu bằng một tiền tố.

Ví dụ:

```python
prefix_search("ca")
```

Kết quả:

```text
cat
car
camera
camp
call
```

#### Nguyên lý

Bước 1:

Tìm node đại diện cho tiền tố `"ca"`.

Bước 2:

Duyệt toàn bộ các node con bằng DFS đệ quy.

Bước 3:

Thu thập các từ hoàn chỉnh.

#### Độ phức tạp

```text
O(m + k)
```

Trong đó:

* `m`: độ dài tiền tố.
* `k`: số node được duyệt để sinh gợi ý.

---

## Ứng dụng trong đồ án

Trie được sử dụng để:

* Lưu trữ từ điển từ khóa.
* Hỗ trợ Autocomplete.
* Gợi ý từ khóa tìm kiếm.
* Tìm kiếm nhanh theo tiền tố.
* Hỗ trợ thuật toán tìm tiền tố chung dài nhất (Longest Common Prefix).

## Kết luận

Trie là cấu trúc dữ liệu phù hợp cho hệ thống gợi ý từ khóa tìm kiếm nhờ:

* Tốc độ tìm kiếm nhanh.
* Hỗ trợ tìm kiếm theo prefix hiệu quả.
* Dễ kết hợp với DFS đệ quy trên cây.
* Có thể kết hợp chiến lược Chia để trị để tìm Longest Common Prefix.

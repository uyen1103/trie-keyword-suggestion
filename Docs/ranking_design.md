# Ranking Algorithm
## 1. Ranking Algorithm là gì?
Là một phương pháp tính toán hoặc tập hợp các quy tắc được sử dụng để đánh giá, gán điểm và sắp xếp thông tin dựa trên các tiêu chí từ đó sắp xếp thông tin sao cho phù hợp, ở đây là việc tìm kiếm thông tin thông qua từ.

Mục tiêu của thuật toán ranking là:

* Ưu tiên các từ được sử dụng nhiều lần.
* Ưu tiên các từ được sử dụng gần đây.
* Chuẩn bị khả năng mở rộng cho các tiêu chí khác như độ dài từ, cá nhân hóa và hành vi người dùng.

---

## 2. Các yếu tố xếp hạng

### 2.1 Frequency (Tần suất sử dụng)

Frequency biểu thị số lần từ khóa được sử dụng hoặc được tìm kiếm.

Ví dụ:

| Word    | Frequency |
| ------- | --------- |
| python  | 100       |
| pycharm | 60        |
| pytorch | 80        |

Từ có frequency cao hơn thường được xem là có độ phổ biến cao hơn.

Chuẩn hóa:

```text
frequency_score = frequency / max_frequency
```

Giá trị nằm trong khoảng:

```text
0 ≤ frequency_score ≤ 1
```

---

### 2.2 Recency (Thời gian sử dụng gần nhất)

Recency phản ánh mức độ mới của dữ liệu.

Giả sử:

```text
days_old = số ngày kể từ lần sử dụng cuối cùng
```

Điểm recency được tính:

```text
recency_score = 1 / (1 + days_old)
```

Ví dụ:

| Days Old | Recency Score |
| -------- | ------------- |
| 0        | 1.000         |
| 1        | 0.500         |
| 2        | 0.333         |
| 7        | 0.125         |
| 30       | 0.032         |

Từ được sử dụng gần đây sẽ có điểm cao hơn.

---

### 2.3 Word Length (Độ dài từ)

Độ dài từ được nghiên cứu như một tiêu chí bổ sung.

Ví dụ:

| Word       | Length |
| ---------- | ------ |
| py         | 2      |
| python     | 6      |
| tensorflow | 10     |

Trong phiên bản hiện tại, độ dài từ chưa được đưa vào công thức xếp hạng chính nhưng được giữ lại để mở rộng trong tương lai.

Ví dụ:

```text
length_score = word_length / max_length
```

---

## 3. Công thức xếp hạng

Phần mềm hiện tại sử dụng:

```text
score =
0.7 × frequency_score + 0.3 × recency_score
```

Trong đó:

* Frequency Weight = 0.7
* Recency Weight = 0.3

Lý do:

* Frequency phản ánh độ phổ biến nên được ưu tiên hơn.
* Recency phản ánh tính mới nên có trọng số thấp hơn.

---

## 4. Ví dụ tính toán

### Word: python

```text
frequency = 100
days_old = 1
```

Tính:

```text
frequency_score = 100 / 100 = 1.0

recency_score = 1 / (1 + 1)
              = 0.5
```

Điểm cuối:

```text
score =
0.7 × 1.0 +
0.3 × 0.5

score = 0.85
```

---

## 5. Quy trình hoạt động

```text
User Input
      │
      ▼
Trie Search
      │
      ▼
Candidate Words
      │
      ▼
SuggestionRanker
      │
      ▼
Sorted Suggestions
```

Ví dụ:

```text
Input: py

Trie Result:
[
    python,
    pycharm,
    pytorch
]

Ranking:
[
    python,
    pytorch,
    pycharm
]
```

---

## 6. Độ phức tạp

### Trie Search

```text
O(k)
```

Trong đó:

```text
k = độ dài prefix
```

### Ranking

```text
O(n log n)
```

Trong đó:

```text
n = số lượng từ gợi ý
```

### Tổng

```text
O(k + n log n)
```

---

## 7. Kiểm thử

Các trường hợp kiểm thử:

1. Danh sách rỗng.
2. Một phần tử.
3. Frequency khác nhau.
4. Frequency bằng nhau.
5. Recency khác nhau.
6. Từ rất cũ.
7. Frequency bằng 0.
8. Prefix không tồn tại.
9. Dataset lớn.
10. Prefix search kết hợp ranking.

-----

## 8. Kết luận

Thuật toán ranking sử dụng Frequency và Recency giúp cải thiện chất lượng gợi ý từ khóa sau khi truy vấn bằng Trie. Từ đó đưa ra các gợi ý phù hợp với thông tin mà người dùng muốn tìm kiếm.

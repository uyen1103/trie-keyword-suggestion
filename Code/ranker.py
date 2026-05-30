# ranker.py
# Ranking logic for suggested keywords
# ranker.py
# Ranking logic for suggested keywords
from datetime import datetime, timedelta
import string


class SuggestionRanker:
    FREQ_WEIGHT = 0.7
    RECENCY_WEIGHT = 0.3

    def rank(self, words, db_data):
        """
        words: prefix người dùng nhập
        db_data: list dict
        """

        if not db_data:
            return []

        # lọc theo prefix
        filtered = [
            item for item in db_data
            if item["word"].lower().startswith(words.lower())
        ]

        if not filtered:
            return []

        max_freq = max(item["frequency"] for item in filtered)

        ranked = []

        for item in filtered:
            freq = item["frequency"]

            days_old = (
                datetime.now() - item["last_used"]
            ).days

            frequency_score = (
                freq / max_freq
                if max_freq > 0
                else 0
            )

            recency_score = 1 / (1 + days_old)

            score = (
                self.FREQ_WEIGHT * frequency_score
                + self.RECENCY_WEIGHT * recency_score
            )

            ranked.append({
                "word": item["word"],
                "frequency": freq,
                "days_old": days_old,
                "score": round(score, 4)
            })

        ranked.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked


# =====================
# MOCK DATA
# =====================

mock_data = [
    {
        "word": "python",
        "frequency": 100,
        "last_used": datetime.now() - timedelta(days=10)
    },
    {
        "word": "pycharm",
        "frequency": 60,
        "last_used": datetime.now() - timedelta(days=30)
    },
    {
        "word": "pytorch",
        "frequency": 80,
        "last_used": datetime.now() - timedelta(days=3)
    },
    {
        "word": "java",
        "frequency": 90,
        "last_used": datetime.now() - timedelta(days=2)
    },
    {
        "word": "javascript",
        "frequency": 70,
        "last_used": datetime.now() - timedelta(days=5)
    }
]


# =====================
# DEMO
# =====================

ranker = SuggestionRanker()

result = ranker.rank("py", mock_data)

# print("=== Ranking Result ===")
# for item in result:
#     print(item)

# // Hand Test input //
# ===== INPUT =====

n = int(input("Nhập số từ khóa: "))

data = []

for i in range(n):
    print(f"\nTừ khóa {i+1}")

    word = input("Word: ")
    frequency = int(input("Frequency: "))
    days_old = int(input("Số ngày từ lần dùng gần nhất: "))

    data.append({
        "word": word,
        "frequency": frequency,
        "last_used": datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - __import__("datetime").timedelta(days=days_old)
    })

# ===== RANK =====

ranker = SuggestionRanker()
result = ranker.rank("",data)

print("\n=== KẾT QUẢ XẾP HẠNG ===")

for idx, item in enumerate(result, start=1):
    print(f"{idx}. {item['word']} - Score: {item['score']}")

# # =====================
# # AI MANUAL TESTS
# # =====================

# print("\n=== TEST CASES ===")

# # Test 1
# assert ranker.rank("", []) == []
# print("Test 1 Passed")

# # Test 2
# single = [{
#     "word": "test",
#     "frequency": 10,
#     "last_used": datetime.now()
# }]
# assert ranker.rank("t", single)[0]["word"] == "test"
# print("Test 2 Passed")

# # Test 3
# result = ranker.rank("py", mock_data)
# assert result[0]["word"] == "python"
# print("Test 3 Passed")

# # Test 4
# same_freq = [
#     {
#         "word": "new",
#         "frequency": 100,
#         "last_used": datetime.now()
#     },
#     {
#         "word": "old",
#         "frequency": 100,
#         "last_used": datetime.now() - timedelta(days=10)
#     }
# ]

# res = ranker.rank("", same_freq)
# assert res[0]["word"] == "new"
# print("Test 4 Passed")

# # Test 5
# old_data = [{
#     "word": "legacy",
#     "frequency": 100,
#     "last_used": datetime.now() - timedelta(days=365)
# }]
# res = ranker.rank("", old_data)
# assert res[0]["score"] < 1
# print("Test 5 Passed")

# # Test 6
# mix = [
#     {
#         "word": "highfreq",
#         "frequency": 100,
#         "last_used": datetime.now() - timedelta(days=30)
#     },
#     {
#         "word": "recent",
#         "frequency": 70,
#         "last_used": datetime.now()
#     }
# ]

# res = ranker.rank("", mix)
# print("Test 6 Result:", res)

# # Test 7
# equal = [
#     {
#         "word": "a",
#         "frequency": 50,
#         "last_used": datetime.now()
#     },
#     {
#         "word": "b",
#         "frequency": 50,
#         "last_used": datetime.now()
#     }
# ]

# res = ranker.rank("", equal)
# assert len(res) == 2
# print("Test 7 Passed")

# # Test 8
# zero_freq = [
#     {
#         "word": "zero",
#         "frequency": 0,
#         "last_used": datetime.now()
#     }
# ]

# res = ranker.rank("", zero_freq)
# assert res[0]["score"] == 0.3
# print("Test 8 Passed")

# # Test 9
# large_dataset = []

# for i in range(1000):
#     large_dataset.append({
#         "word": f"word{i}",
#         "frequency": i + 1,
#         "last_used": datetime.now()
#     })

# res = ranker.rank("word", large_dataset)

# assert len(res) == 1000
# print("Test 9 Passed")

# # Test 10
# res = ranker.rank("py", mock_data)

# for item in res:
#     assert item["word"].startswith("py")

# print("Test 10 Passed")

# print("\nAll tests passed!")

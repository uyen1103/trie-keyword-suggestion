import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from Code.ranker import SuggestionRanker
from datetime import datetime, timedelta
from code.ranker import SuggestionRanker

# case1
def test_rank_returns_list_of_str():
    now = datetime.now()
    db = [{"keyword": "apple", "frequency": 1, "last_searched": now}]
    ranker = SuggestionRanker()
    res = ranker.rank(["app"], db)
    assert isinstance(res, list)
    assert all(isinstance(x, str) for x in res)
    assert res == ["apple"]

# case2
def test_order_by_frequency():
    now = datetime.now()
    db = [
        {"keyword": "a_high", "frequency": 10, "last_searched": now},
        {"keyword": "a_low", "frequency": 2, "last_searched": now},
    ]
    ranker = SuggestionRanker()
    res = ranker.rank(["a"], db)
    assert res == ["a_high", "a_low"]

# case3
def test_order_by_recency():
    now = datetime.now()
    db = [
        {"keyword": "b_recent", "frequency": 5, "last_searched": now},
        {"keyword": "b_old", "frequency": 5, "last_searched": now - timedelta(days=30)},
    ]
    ranker = SuggestionRanker()
    res = ranker.rank(["b"], db)
    assert res == ["b_recent", "b_old"]

# case4
def test_nonexistent_prefix_returns_empty():
    now = datetime.now()
    db = [{"keyword": "c1", "frequency": 1, "last_searched": now}]
    ranker = SuggestionRanker()
    res = ranker.rank(["zzz"], db)
    assert res == []

# case5
def test_get_top_returns_top_k():
    now = datetime.now()
    db = []
    for i in range(10):
        db.append({
            "keyword": f"t{i}",
            "frequency": 10 - i,
            "last_searched": now - timedelta(days=i),
        })

    ranker = SuggestionRanker()
    top3 = ranker.get_top(["t"], db, top_k=3)
    expected = ranker.rank(["t"], db)[:3]
    assert top3 == expected
    assert len(top3) == 3


def test_explain_handles_empty_db_and_missing_word():
    now = datetime.now()
    ranker = SuggestionRanker()

    # empty db_data shouldn't crash and should report zero scores
    res_empty = ranker.explain("missing", [])
    assert "score=0.00" in res_empty

    # db_data present but word missing and max frequency 0 -> fallback to 0
    db_zero = [{"keyword": "x", "frequency": 0, "last_searched": now - timedelta(days=1)}]
    res_missing = ranker.explain("missing", db_zero)
    assert "score=0.00" in res_missing

# ranker.py
# Ranking logic for suggested keywords
from datetime import datetime, timedelta
import string


class SuggestionRanker:
	def __init__(self, w_freq: float = 0.7, w_rec: float = 0.3):
		self.FREQ_WEIGHT = w_freq
		self.RECENCY_WEIGHT = w_rec

	def _get_days_old(self, last_searched) -> int:
		"""Tính số ngày kể từ lần tìm kiếm cuối cùng, nếu lỗi thì trả về 0."""
		if not last_searched:
			return 0
	
		try:
			if isinstance(last_searched, str):
				dt = datetime.fromisoformat(last_searched.replace("Z", "+00:00"))
			else:
				dt = last_searched
	
			if dt.tzinfo is not None:
				dt = dt.astimezone().replace(tzinfo=None)
	
			return max(0, (datetime.now() - dt).days)
	
		except (ValueError, TypeError):
			return 0

	def rank(self, words: list[str], db_data):
		"""
		words: list of prefixes user typed (list[str])
		db_data: list of dicts with keys: 'keyword', 'frequency', 'last_searched'
		Returns: list[str] of keywords ordered by descending score
		"""

		if not db_data:
			return []

		# lọc theo prefix list
		if not isinstance(words, (list, tuple)):
			prefixes = [str(words)]
		else:
			prefixes = [str(p) for p in words]

		prefixes = [p.lower() for p in prefixes]

		filtered = [
			item for item in db_data
			if any(
				item["keyword"].lower().startswith(prefix)
				for prefix in prefixes
			)
		]

		if not filtered:
			return []

		max_freq = max(item["frequency"] for item in filtered)

		ranked = []

		for item in filtered:
			freq = item["frequency"]

			days_old = self._get_days_old(item.get("last_searched"))

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
				"keyword": item["keyword"],
				"frequency": freq,
				"days_old": days_old,
				"score": round(score, 4)
			})

		ranked.sort(
			key=lambda x: x["score"],
			reverse=True
		)

		# return only the keywords in ranked order
		return [r["keyword"] for r in ranked]

	def get_top(self, words: list[str], db_data, top_k: int = 5) -> list[str]:
		"""Return top_k keywords for the given prefixes.

		Delegates to `rank` and slices the result.
		"""
		return self.rank(words, db_data)[:top_k]

	def explain(self, word: str, db_data: list[dict]) -> str:
		"""Compute score for a single keyword and return a formatted string.

		Example: 'python: score=0.85 (freq=1.00, rec=0.50)'
		"""
		if not db_data:
			return f"{word}: score=0.00 (freq=0.00, rec=0.00)"

		# find the item matching the keyword
		item = next((it for it in db_data if it.get("keyword") == word), None)
		if item is None:
			return f"{word}: score=0.00 (freq=0.00, rec=0.00)"

		max_freq = max((it.get("frequency", 0) for it in db_data), default=0)
		freq = item.get("frequency", 0)

		days_old = self._get_days_old(item.get("last_searched", datetime.now()))

		frequency_score = (freq / max_freq) if max_freq > 0 else 0.0
		recency_score = 1 / (1 + days_old)

		score = self.FREQ_WEIGHT * frequency_score + self.RECENCY_WEIGHT * recency_score

		return f"{word}: score={score:.2f} (freq={frequency_score:.2f}, rec={recency_score:.2f})"

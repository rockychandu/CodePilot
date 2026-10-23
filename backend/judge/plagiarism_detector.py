"""
Code Token N-Gram Similarity & Plagiarism Detector
"""
import re

class PlagiarismDetector:
    @staticmethod
    def tokenize(code: str) -> list:
        # Strip comments and normalize whitespace
        clean = re.sub(r"#.*|//.*|/\*.*?\*/", "", code or "", flags=re.DOTALL)
        tokens = re.findall(r"\w+|[^\w\s]", clean)
        return tokens

    @classmethod
    def get_ngrams(cls, tokens: list, n: int = 3) -> set:
        if len(tokens) < n:
            return set(tuple(tokens)) if tokens else set()
        return {tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)}

    @classmethod
    def calculate_similarity(cls, code_a: str, code_b: str, n: int = 3) -> float:
        t_a = cls.tokenize(code_a)
        t_b = cls.tokenize(code_b)
        ng_a = cls.get_ngrams(t_a, n)
        ng_b = cls.get_ngrams(t_b, n)

        if not ng_a or not ng_b:
            return 0.0

        intersection = len(ng_a.intersection(ng_b))
        union = len(ng_a.union(ng_b))
        return round(intersection / union, 3)

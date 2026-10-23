"""
Problem Categorization & Tag Taxonomy
"""
TAXONOMY = {
    "Algorithms": ["Dynamic Programming", "Greedy", "Binary Search", "Two Pointers", "Sorting", "Graph Theory"],
    "Data Structures": ["Arrays", "Hash Tables", "Trees", "Heaps", "Trie", "Disjoint Set Union"],
    "Mathematics": ["Number Theory", "Combinatorics", "Geometry", "Bit Manipulation"],
    "Systems": ["Concurrency", "Memory Management", "Socket I/O", "File Systems"]
}

class ProblemTagTaxonomy:
    @staticmethod
    def normalize_tag(tag: str) -> str:
        return " ".join((tag or "").strip().title().split())

    @staticmethod
    def get_category_for_tag(tag: str) -> str:
        norm = ProblemTagTaxonomy.normalize_tag(tag)
        for cat, tags in TAXONOMY.items():
            if norm.lower() in [t.lower() for t in tags]:
                return cat
        return "General"

    @classmethod
    def list_all_tags(cls) -> list:
        all_t = []
        for tags in TAXONOMY.values():
            all_t.extend(tags)
        return sorted(all_t)

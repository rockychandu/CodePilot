"""
Multi-File Source Code Bundler & Module Packager
"""
import os

class SourceBundler:
    @staticmethod
    def pack(files: list) -> dict:
        bundle = {}
        for f in files:
            name = f.get("filename") or f.get("name")
            content = f.get("content", "")
            if name:
                clean_name = name.replace(chr(92), "/").lstrip("/")
                bundle[clean_name] = content
        return bundle

    @staticmethod
    def find_entrypoint(bundle: dict, language: str) -> str:
        lang = (language or "python").lower()
        candidates = {
            "python": ["main.py", "app.py", "solution.py"],
            "javascript": ["index.js", "main.js", "solution.js"],
            "cpp": ["main.cpp", "solution.cpp"],
            "java": ["Main.java", "Solution.java"],
            "go": ["main.go"],
            "rust": ["main.rs", "lib.rs"]
        }.get(lang, ["main.py"])

        for cand in candidates:
            if cand in bundle:
                return cand
        return list(bundle.keys())[0] if bundle else ""

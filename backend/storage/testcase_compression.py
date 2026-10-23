"""
Test Case Large Payload Compression Utility
"""
import zlib
import base64

class TestCaseCompressor:
    THRESHOLD_BYTES = 1024  # Compress payloads > 1KB

    @classmethod
    def compress_if_needed(cls, text: str) -> tuple:
        raw = (text or "").encode("utf-8")
        if len(raw) <= cls.THRESHOLD_BYTES:
            return text, False

        compressed = zlib.compress(raw, level=6)
        encoded = base64.b64encode(compressed).decode("ascii")
        return encoded, True

    @staticmethod
    def decompress(payload: str, is_compressed: bool) -> str:
        if not is_compressed:
            return payload
        raw_b64 = base64.b64decode(payload.encode("ascii"))
        decompressed = zlib.decompress(raw_b64)
        return decompressed.decode("utf-8")

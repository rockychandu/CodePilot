"""
Process Output Buffer Multiplexer & Clamping
"""
class PipeMultiplexer:
    DEFAULT_MAX_BYTES = 512 * 1024  # 512 KB

    @classmethod
    def clamp_output(cls, output: str, max_bytes: int = None) -> tuple:
        limit = max_bytes or cls.DEFAULT_MAX_BYTES
        raw = (output or "").encode("utf-8")
        if len(raw) <= limit:
            return output, False

        clamped = raw[:limit].decode("utf-8", errors="ignore")
        truncated_msg = f"\n\n[Output truncated at {round(limit / 1024)} KB limit]"
        return clamped + truncated_msg, True

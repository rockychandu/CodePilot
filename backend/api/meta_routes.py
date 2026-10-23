"""
API Version Metadata & Runtime Compilers Catalog
"""
class APIMetadataService:
    VERSION = "2.1.0"
    API_PREFIX = "/api/v1"

    SUPPORTED_RUNTIMES = [
        {"language": "python", "version": "3.12+", "standard": "PEP-8"},
        {"language": "javascript", "version": "Node.js 20 LTS", "standard": "ES2024"},
        {"language": "cpp", "version": "GCC 13 / Clang 17", "standard": "C++20"},
        {"language": "c", "version": "GCC 13", "standard": "C17"},
        {"language": "java", "version": "OpenJDK 21 LTS", "standard": "Java SE 21"},
        {"language": "go", "version": "Go 1.22", "standard": "Go Toolchain"},
        {"language": "rust", "version": "Rustc 1.76", "standard": "Edition 2021"}
    ]

    @classmethod
    def get_metadata(cls) -> dict:
        return {
            "version": cls.VERSION,
            "apiPrefix": cls.API_PREFIX,
            "status": "GA",
            "runtimeCount": len(cls.SUPPORTED_RUNTIMES),
            "runtimes": cls.SUPPORTED_RUNTIMES
        }

"""
CodePilot Database Seeder
Populates database with initial languages, problems, test cases, contests,
courses, lessons, skills, and admin accounts.
"""

import json
from datetime import datetime, timezone, timedelta
from codepilot.db.connection import db_session, init_db
from codepilot.db.models import (
    User, Profile, Problem, TestCase, Contest, Course, Module, Lesson,
    Skill, UserSkill, RuntimeConfig, Notification, Project, ProjectFile
)
from codepilot.utils.security import hash_password


def seed_database():
    init_db()
    db = db_session()

    # 1. Seed Runtimes
    runtimes = [
        {"language_id": "python", "display_name": "Python 3.12+", "file_extension": "py", "compiler_cmd": "", "execution_cmd": "python", "version_cmd": "python --version", "default_timeout_seconds": 5.0, "memory_limit_mb": 128.0},
        {"language_id": "javascript", "display_name": "JavaScript (Node.js)", "file_extension": "js", "compiler_cmd": "", "execution_cmd": "node", "version_cmd": "node -v", "default_timeout_seconds": 5.0, "memory_limit_mb": 128.0},
        {"language_id": "typescript", "display_name": "TypeScript", "file_extension": "ts", "compiler_cmd": "tsc", "execution_cmd": "node", "version_cmd": "tsc -v", "default_timeout_seconds": 5.0, "memory_limit_mb": 128.0},
        {"language_id": "c", "display_name": "C (GCC 13+)", "file_extension": "c", "compiler_cmd": "gcc -O2 -Wall", "execution_cmd": "./main", "version_cmd": "gcc --version", "default_timeout_seconds": 3.0, "memory_limit_mb": 64.0},
        {"language_id": "cpp", "display_name": "C++ (G++ 13+ / C++20)", "file_extension": "cpp", "compiler_cmd": "g++ -O3 -std=c++20", "execution_cmd": "./main", "version_cmd": "g++ --version", "default_timeout_seconds": 3.0, "memory_limit_mb": 64.0},
        {"language_id": "java", "display_name": "Java (OpenJDK 21)", "file_extension": "java", "compiler_cmd": "javac", "execution_cmd": "java Main", "version_cmd": "java -version", "default_timeout_seconds": 5.0, "memory_limit_mb": 256.0},
        {"language_id": "go", "display_name": "Go (1.22+)", "file_extension": "go", "compiler_cmd": "go build", "execution_cmd": "./main", "version_cmd": "go version", "default_timeout_seconds": 4.0, "memory_limit_mb": 128.0},
        {"language_id": "rust", "display_name": "Rust (2021 Edition)", "file_extension": "rs", "compiler_cmd": "rustc -O", "execution_cmd": "./main", "version_cmd": "rustc --version", "default_timeout_seconds": 4.0, "memory_limit_mb": 128.0},
        {"language_id": "php", "display_name": "PHP 8.3+", "file_extension": "php", "compiler_cmd": "", "execution_cmd": "php", "version_cmd": "php -v", "default_timeout_seconds": 5.0, "memory_limit_mb": 128.0},
        {"language_id": "ruby", "display_name": "Ruby 3.3+", "file_extension": "rb", "compiler_cmd": "", "execution_cmd": "ruby", "version_cmd": "ruby -v", "default_timeout_seconds": 5.0, "memory_limit_mb": 128.0},
        {"language_id": "csharp", "display_name": "C# (.NET 8)", "file_extension": "cs", "compiler_cmd": "csc", "execution_cmd": "dotnet", "version_cmd": "dotnet --version", "default_timeout_seconds": 5.0, "memory_limit_mb": 256.0},
    ]

    for rt in runtimes:
        if not db.query(RuntimeConfig).filter_by(language_id=rt["language_id"]).first():
            config = RuntimeConfig(**rt)
            db.add(config)

    # 2. Seed Users
    if not db.query(User).filter_by(username="admin").first():
        pw_hash, salt = hash_password("Admin@123456")
        admin_user = User(
            username="admin",
            email="admin@codepilot.dev",
            password_hash=pw_hash,
            salt=salt,
            role="ADMIN",
            is_active=True,
            is_verified=True
        )
        db.add(admin_user)
        db.flush()

        admin_profile = Profile(
            user_id=admin_user.id,
            display_name="CodePilot System Administrator",
            bio="Lead architect & infrastructure administrator at CodePilot.",
            primary_language="Python",
            preferred_languages=json.dumps(["Python", "C++", "Rust", "TypeScript"]),
            xp=9850,
            level=42,
            rank_title="Grandmaster Engineer",
            streak_days=120,
            problems_solved=340,
            contest_rating=2450
        )
        db.add(admin_profile)

    if not db.query(User).filter_by(username="pilot_dev").first():
        pw_hash, salt = hash_password("Pilot@123456")
        dev_user = User(
            username="pilot_dev",
            email="dev@codepilot.dev",
            password_hash=pw_hash,
            salt=salt,
            role="USER",
            is_active=True,
            is_verified=True
        )
        db.add(dev_user)
        db.flush()

        dev_profile = Profile(
            user_id=dev_user.id,
            display_name="Alex River (Pilot Dev)",
            bio="Full-stack engineer solving algorithmic challenges & mastering distributed systems.",
            primary_language="Python",
            preferred_languages=json.dumps(["Python", "JavaScript", "Go"]),
            xp=2450,
            level=12,
            rank_title="Senior Algorithmist",
            streak_days=18,
            problems_solved=48,
            contest_rating=1620
        )
        db.add(dev_profile)

    # 3. Seed Skills
    skills_data = [
        {"slug": "python", "title": "Python Core & Advanced", "category": "Programming", "description": "Master Python syntax, generators, decorators, AST manipulation, and concurrency.", "icon_name": "python", "prerequisites_json": "[]", "max_level": 5},
        {"slug": "data-structures", "title": "Data Structures", "category": "Algorithms", "description": "Trees, Graphs, Heaps, Hash Tables, Segment Trees, and Disjoint Sets.", "icon_name": "layers", "prerequisites_json": "[\"python\"]", "max_level": 5},
        {"slug": "algorithms", "title": "Algorithms & Optimization", "category": "Algorithms", "description": "Dynamic Programming, Greedy Strategies, Graph Traversals, and Backtracking.", "icon_name": "cpu", "prerequisites_json": "[\"data-structures\"]", "max_level": 5},
        {"slug": "cpp-systems", "title": "C++ Systems Programming", "category": "Systems", "description": "Memory management, RAII, pointers, templates, and low-latency programming.", "icon_name": "terminal", "prerequisites_json": "[]", "max_level": 5},
        {"slug": "web-architecture", "title": "Web Architecture & APIs", "category": "Web Development", "description": "RESTful services, WebSockets, microservices, auth, and state machines.", "icon_name": "globe", "prerequisites_json": "[]", "max_level": 5},
        {"slug": "cloud-devops", "title": "Cloud, Docker & DevOps", "category": "DevOps", "description": "Containerization, CI/CD pipelines, Kubernetes, telemetry, and observability.", "icon_name": "cloud", "prerequisites_json": "[\"web-architecture\"]", "max_level": 5},
    ]

    for s in skills_data:
        if not db.query(Skill).filter_by(slug=s["slug"]).first():
            db.add(Skill(**s))

    # 4. Seed Problems
    problems_data = [
        {
            "slug": "two-sum",
            "title": "Two Sum",
            "difficulty": "Easy",
            "category": "Algorithms",
            "tags": json.dumps(["Array", "Hash Table"]),
            "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.",
            "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9",
            "hints": json.dumps(["A brute force approach checks all pairs in O(n^2) time.", "Can you use a hash map to look up complements in O(1) time?"]),
            "editorial": "By mapping each value to its index during a single pass, we can verify if `target - num` already exists in O(N) time and O(N) space.",
            "starter_templates": json.dumps({
                "python": "def two_sum(nums: list[int], target: int) -> list[int]:\n    # Write your solution here\n    pass\n",
                "javascript": "function twoSum(nums, target) {\n    // Write your solution here\n}\n",
                "cpp": "#include <vector>\n#include <unordered_map>\n\nstd::vector<int> twoSum(std::vector<int>& nums, int target) {\n    // Write your solution here\n}\n"
            }),
            "time_limit_seconds": 2.0,
            "memory_limit_mb": 128.0,
            "total_submissions": 45120,
            "accepted_submissions": 38400,
            "test_cases": [
                {"input_data": "[2, 7, 11, 15]\n9", "expected_output": "[0, 1]", "is_hidden": False, "explanation": "nums[0] + nums[1] == 9, so return [0, 1]"},
                {"input_data": "[3, 2, 4]\n6", "expected_output": "[1, 2]", "is_hidden": False, "explanation": "nums[1] + nums[2] == 6, so return [1, 2]"},
                {"input_data": "[3, 3]\n6", "expected_output": "[0, 1]", "is_hidden": True, "explanation": "Hidden case duplicates"},
                {"input_data": "[1, 5, 8, 12, 19, 23]\n31", "expected_output": "[3, 4]", "is_hidden": True, "explanation": "Hidden larger array"}
            ]
        },
        {
            "slug": "valid-parentheses",
            "title": "Valid Parentheses",
            "difficulty": "Easy",
            "category": "Data Structures",
            "tags": json.dumps(["String", "Stack"]),
            "description": "Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.\n\nAn input string is valid if open brackets are closed by the same type of brackets in the correct order.",
            "constraints": "1 <= s.length <= 10^4\ns consists of parentheses only '()[]{}'.",
            "hints": json.dumps(["Use a stack to keep track of opening brackets.", "Whenever you encounter a closing bracket, check if it matches the top of stack."]),
            "editorial": "Push open brackets onto a stack. When a close bracket appears, pop and verify it matches.",
            "starter_templates": json.dumps({
                "python": "def is_valid(s: str) -> bool:\n    # Write your solution here\n    pass\n",
                "javascript": "function isValid(s) {\n    // Write your solution here\n}\n"
            }),
            "time_limit_seconds": 2.0,
            "memory_limit_mb": 128.0,
            "total_submissions": 28900,
            "accepted_submissions": 21500,
            "test_cases": [
                {"input_data": "()", "expected_output": "True", "is_hidden": False, "explanation": "Single pair matches"},
                {"input_data": "()[]{}", "expected_output": "True", "is_hidden": False, "explanation": "All types matched"},
                {"input_data": "(]", "expected_output": "False", "is_hidden": False, "explanation": "Mismatched closing"},
                {"input_data": "([{}])", "expected_output": "True", "is_hidden": True, "explanation": "Nested brackets"},
                {"input_data": "(((((", "expected_output": "False", "is_hidden": True, "explanation": "Unclosed brackets"}
            ]
        },
        {
            "slug": "longest-substring-without-repeating-characters",
            "title": "Longest Substring Without Repeating Characters",
            "difficulty": "Medium",
            "category": "Algorithms",
            "tags": json.dumps(["Hash Table", "String", "Sliding Window"]),
            "description": "Given a string `s`, find the length of the **longest substring** without duplicate characters.",
            "constraints": "0 <= s.length <= 5 * 10^4\ns consists of English letters, digits, symbols and spaces.",
            "hints": json.dumps(["Maintain a sliding window [left, right] with character frequency table."]),
            "editorial": "A two-pointer sliding window tracks unique characters in O(N) time.",
            "starter_templates": json.dumps({
                "python": "def length_of_longest_substring(s: str) -> int:\n    # Write your solution here\n    pass\n"
            }),
            "time_limit_seconds": 2.0,
            "memory_limit_mb": 128.0,
            "total_submissions": 19400,
            "accepted_submissions": 12100,
            "test_cases": [
                {"input_data": "abcabcbb", "expected_output": "3", "is_hidden": False, "explanation": "The answer is 'abc', length 3"},
                {"input_data": "bbbbb", "expected_output": "1", "is_hidden": False, "explanation": "The answer is 'b', length 1"},
                {"input_data": "pwwkew", "expected_output": "3", "is_hidden": False, "explanation": "The answer is 'wke', length 3"},
                {"input_data": " ", "expected_output": "1", "is_hidden": True, "explanation": "Single space"},
                {"input_data": "abcdefghijklmnopqrstuvwxyz", "expected_output": "26", "is_hidden": True, "explanation": "Full alphabet"}
            ]
        }
    ]

    for p_data in problems_data:
        test_cases_list = p_data.pop("test_cases")
        existing_p = db.query(Problem).filter_by(slug=p_data["slug"]).first()
        if not existing_p:
            prob = Problem(**p_data)
            db.add(prob)
            db.flush()
            for idx, tc in enumerate(test_cases_list):
                db.add(TestCase(
                    problem_id=prob.id,
                    input_data=tc["input_data"],
                    expected_output=tc["expected_output"],
                    is_hidden=tc["is_hidden"],
                    explanation=tc.get("explanation", ""),
                    order_index=idx
                ))

    # 5. Seed Contests
    now = datetime.now(timezone.utc)
    if not db.query(Contest).filter_by(slug="biweekly-contest-42").first():
        contest_42 = Contest(
            slug="biweekly-contest-42",
            title="CodePilot Biweekly Algorithmic Arena #42",
            description="Compete against thousands of global developers across 4 algorithmic challenges in 90 minutes.",
            start_time=now - timedelta(hours=24),
            end_time=now + timedelta(days=6),
            duration_minutes=90,
            problem_ids_json=json.dumps([1, 2, 3]),
            penalty_minutes_per_wrong=10,
            is_published=True
        )
        db.add(contest_42)

    # 6. Seed Courses
    if not db.query(Course).filter_by(slug="python-mastery-2026").first():
        py_course = Course(
            slug="python-mastery-2026",
            title="Modern Python 3.12+ Systems & Architecture",
            description="Deep-dive into metaprogramming, AST parsing, asynchronous event loops, C-extensions, and production design patterns.",
            category="Programming",
            difficulty="Intermediate",
            thumbnail_url="frontend/assets/logo.svg",
            estimated_hours=14.5,
            is_published=True
        )
        db.add(py_course)
        db.flush()

        m1 = Module(course_id=py_course.id, title="Module 1: Advanced Object-Oriented & AST Core", order_index=0)
        db.add(m1)
        db.flush()

        l1 = Lesson(
            module_id=m1.id,
            title="Lesson 1.1: AST Syntax Inspection & Dynamic Sandboxes",
            lesson_type="VIDEO",
            content_url="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
            content_text="Learn how to parse Python syntax trees using Python standard ast module.",
            video_chapters_json=json.dumps([
                {"time": 0, "title": "Introduction to ASTs"},
                {"time": 180, "title": "AST Node Visitors & Transformers"},
                {"time": 420, "title": "Security Sandboxing via AST Rules"}
            ]),
            duration_minutes=25,
            order_index=0
        )
        l2 = Lesson(
            module_id=m1.id,
            title="Lesson 1.2: Architecture Whitepaper (PDF)",
            lesson_type="PDF",
            content_url="docs/ARCHITECTURE.md",
            content_text="Detailed whitepaper on distributed code execution engines.",
            duration_minutes=15,
            order_index=1
        )
        db.add_all([l1, l2])

    # 7. Seed Initial Projects for pilot_dev & admin
    from backend.repositories.project_repository import ProjectRepository
    dev_user = db.query(User).filter_by(username="pilot_dev").first()
    if dev_user and not db.query(Project).filter_by(user_id=dev_user.id).first():
        ProjectRepository.create_project(
            user_id=dev_user.id,
            title="codepilot-api",
            description="Python & Flask REST microservice for cloud code compilation and telemetry.",
            language="python",
            template="web"
        )
        ProjectRepository.create_project(
            user_id=dev_user.id,
            title="algorithm-lab",
            description="C++ competitive programming solution templates, graph routines, and segment trees.",
            language="cpp",
            template="algorithm"
        )

    admin_user = db.query(User).filter_by(username="admin").first()
    if admin_user and not db.query(Project).filter_by(user_id=admin_user.id).first():
        ProjectRepository.create_project(
            user_id=admin_user.id,
            title="kernel-runtime-monitor",
            description="High-performance Go agent monitoring execution sandbox memory and CPU bounds.",
            language="go",
            template="cli"
        )

    db.commit()
    db.close()
    print("CodePilot database seeded successfully!")


if __name__ == "__main__":
    seed_database()

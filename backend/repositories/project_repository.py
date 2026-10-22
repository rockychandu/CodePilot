"""
Project Workspaces Repository & Scaffolding Engine
Supports multi-language templates, file tree operations, duplicate, rename, export, and delete.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from codepilot.db.connection import get_db_session
from codepilot.db.models import Project, ProjectFile, User


def get_template_scaffolding(language: str, template: str, project_title: str) -> List[Dict[str, str]]:
    """
    Generate authentic multi-file developer scaffolding tailored to language and template.
    """
    lang = (language or "python").lower()
    tmpl = (template or "cli").lower().replace(" ", "_").replace("-", "_")

    files = []

    # Map main filenames and extensions
    ext_map = {
        "python": "py", "javascript": "js", "typescript": "ts",
        "cpp": "cpp", "c": "c", "java": "java", "go": "go",
        "rust": "rs", "csharp": "cs", "php": "php", "ruby": "rb", "kotlin": "kt"
    }
    ext = ext_map.get(lang, "py")

    # 1. Blank Project
    if tmpl == "blank_project" or tmpl == "blank":
        main_name = f"Main.{ext}" if lang in ["java", "csharp", "kotlin"] else f"main.{ext}"
        if lang == "python":
            code = "# Blank Python Project\n\ndef main():\n    pass\n\nif __name__ == '__main__':\n    main()\n"
        elif lang in ["javascript", "typescript"]:
            code = "// Blank Project Entrypoint\nconsole.log('Project initialized.');\n"
        elif lang in ["c", "cpp"]:
            code = f"#include <iostream>\n\nint main() {{\n    // Entrypoint\n    return 0;\n}}\n" if lang == "cpp" else "#include <stdio.h>\n\nint main() {\n    return 0;\n}\n"
        elif lang == "java":
            code = "public class Main {\n    public static void main(String[] args) {\n        // Blank project\n    }\n}\n"
        elif lang == "go":
            code = "package main\n\nfunc main() {\n    // Blank project\n}\n"
        elif lang == "rust":
            code = "fn main() {\n    // Blank project\n}\n"
        else:
            code = f"// CodePilot {project_title}\n"
        files.append({"filename": main_name, "content": code})
        files.append({"filename": "README.md", "content": f"# {project_title}\n\nA blank {language.capitalize()} developer workspace on CodePilot.\n"})
        return files

    # 2. Web Application / REST API
    if "web" in tmpl or "api" in tmpl or "rest" in tmpl:
        if lang == "python":
            files.append({
                "filename": "app.py",
                "content": "from flask import Flask, jsonify, request\n\napp = Flask(__name__)\n\n@app.route('/api/v1/health', methods=['GET'])\ndef health():\n    return jsonify({\"status\": \"UP\", \"service\": \"" + project_title + "\"})\n\n@app.route('/api/v1/items', methods=['GET'])\ndef get_items():\n    return jsonify([{\"id\": 1, \"name\": \"Pilot Core Engine\"}, {\"id\": 2, \"name\": \"Execution Sandbox\"}])\n\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=8000, debug=True)\n"
            })
            files.append({
                "filename": "requirements.txt",
                "content": "flask>=3.0.0\ngunicorn>=21.0.0\npytest>=8.0.0\n"
            })
            files.append({
                "filename": "tests.py",
                "content": "import unittest\nfrom app import app\n\nclass ApiTestCase(unittest.TestCase):\n    def setUp(self):\n        self.client = app.test_client()\n\n    def test_health(self):\n        res = self.client.get('/api/v1/health')\n        self.assertEqual(res.status_code, 200)\n\nif __name__ == '__main__':\n    unittest.main()\n"
            })
        elif lang in ["javascript", "typescript"]:
            files.append({
                "filename": f"server.{ext}",
                "content": f"// {project_title} — Express REST API\nconst express = require('express');\nconst app = express();\nconst PORT = process.env.PORT || 3000;\n\napp.use(express.json());\n\napp.get('/health', (req, res) => {{\n    res.json({{ status: 'OK', uptime: process.uptime() }});\n}});\n\napp.get('/api/v1/data', (req, res) => {{\n    res.json({{ message: 'Hello from CodePilot Cloud API', timestamp: new Date() }});\n}});\n\napp.listen(PORT, () => {{\n    console.log(`Server listening on port ${{PORT}}`);\n}});\n"
            })
            files.append({
                "filename": "package.json",
                "content": '{\n  "name": "' + project_title.lower().replace(" ", "-") + '",\n  "version": "1.0.0",\n  "main": "server.' + ext + '",\n  "dependencies": {\n    "express": "^4.19.2"\n  }\n}\n'
            })
        elif lang == "go":
            files.append({
                "filename": "main.go",
                "content": 'package main\n\nimport (\n\t"encoding/json"\n\t"log"\n\t"net/http"\n)\n\ntype HealthResponse struct {\n\tStatus  string `json:"status"`\n\tService string `json:"service"`\n}\n\nfunc healthHandler(w http.ResponseWriter, r *http.Request) {\n\tw.Header().Set("Content-Type", "application/json")\n\tjson.NewEncoder(w).Encode(HealthResponse{Status: "ONLINE", Service: "' + project_title + '"})\n}\n\nfunc main() {\n\thttp.HandleFunc("/health", healthHandler)\n\tlog.Println("Server starting on :8080...")\n\tlog.Fatal(http.ListenAndServe(":8080", nil))\n}\n'
            })
            files.append({"filename": "go.mod", "content": f"module {project_title.lower().replace(' ', '-')}\n\ngo 1.22\n"})
        else:
            files.append({
                "filename": f"main.{ext}",
                "content": f"// {project_title} REST API Service\n"
            })

        files.append({"filename": "README.md", "content": f"# {project_title}\n\nREST API & Microservice backend written in {language.capitalize()}.\n\n### Endpoints\n- `GET /health` — Service readiness\n- `GET /api/v1/data` — Primary collection\n"})
        return files

    # 3. Algorithm Workspace / Competitive Programming
    if "algo" in tmpl:
        if lang == "python":
            files.append({
                "filename": "solution.py",
                "content": '"""\nAlgorithmic Problem Solution Template\nTime Complexity: O(N log N)\nSpace Complexity: O(N)\n"""\nimport sys\n\ndef solve():\n    input_data = sys.stdin.read().split()\n    if not input_data:\n        print("Ready for competitive inputs.")\n        return\n    n = int(input_data[0])\n    nums = [int(x) for x in input_data[1:n+1]]\n    nums.sort()\n    print(f"Processed {len(nums)} elements: {nums[:5]}")\n\nif __name__ == "__main__":\n    solve()\n'
            })
            files.append({
                "filename": "test_cases.txt",
                "content": "5\n42 17 99 1 23\n"
            })
        elif lang == "cpp":
            files.append({
                "filename": "solution.cpp",
                "content": '#include <iostream>\n#include <vector>\n#include <algorithm>\n\nusing namespace std;\n\nvoid solve() {\n    int n;\n    if (!(cin >> n)) return;\n    vector<int> a(n);\n    for (int i = 0; i < n; ++i) cin >> a[i];\n    sort(a.begin(), a.end());\n    cout << "Sorted: ";\n    for (int x : a) cout << x << " ";\n    cout << "\\n";\n}\n\nint main() {\n    ios_base::sync_with_stdio(false);\n    cin.tie(NULL);\n    solve();\n    return 0;\n}\n'
            })
            files.append({
                "filename": "input.txt",
                "content": "5\n8 3 19 2 77\n"
            })
        elif lang == "java":
            files.append({
                "filename": "Solution.java",
                "content": 'import java.util.*;\n\npublic class Solution {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        if (!sc.hasNextInt()) {\n            System.out.println("No input provided.");\n            return;\n        }\n        int n = sc.nextInt();\n        int[] arr = new int[n];\n        for (int i = 0; i < n; i++) arr[i] = sc.nextInt();\n        Arrays.sort(arr);\n        System.out.println("Result: " + Arrays.toString(arr));\n    }\n}\n'
            })
        else:
            files.append({"filename": f"solution.{ext}", "content": f"// Algorithm Solver in {language.capitalize()}\n"})

        files.append({"filename": "README.md", "content": f"# {project_title}\n\nAlgorithmic playground & competitive programming workspace.\n"})
        return files

    # 4. Data Science
    if "data" in tmpl or "science" in tmpl:
        files.append({
            "filename": "pipeline.py" if lang == "python" else f"analysis.{ext}",
            "content": '"""\nData Science Analysis Pipeline & Feature Extractor\n"""\nimport math\n\ndef analyze_dataset(data):\n    n = len(data)\n    mean = sum(data) / n\n    variance = sum((x - mean) ** 2 for x in data) / n\n    std_dev = math.sqrt(variance)\n    return {"count": n, "mean": round(mean, 2), "std_dev": round(std_dev, 2)}\n\nif __name__ == "__main__":\n    sample = [23.4, 45.1, 12.8, 67.9, 34.2, 89.0, 52.3]\n    metrics = analyze_dataset(sample)\n    print("Pipeline Execution Metrics:", metrics)\n'
        })
        files.append({
            "filename": "dataset.csv",
            "content": "id,timestamp,value,label\n1,2026-09-01T12:00:00Z,23.4,train\n2,2026-09-01T12:01:00Z,45.1,train\n3,2026-09-01T12:02:00Z,12.8,eval\n4,2026-09-01T12:03:00Z,67.9,train\n5,2026-09-01T12:04:00Z,34.2,eval\n"
        })
        files.append({"filename": "README.md", "content": f"# {project_title}\n\nData ingestion, statistical analysis, and feature engineering workspace.\n"})
        return files

    # 5. CLI Application & General Default (CLI, Learning Project, etc.)
    if lang == "python":
        files.append({
            "filename": "main.py",
            "content": '"""\nCodePilot CLI Application Entrypoint\n"""\nimport sys\nimport argparse\n\ndef main():\n    parser = argparse.ArgumentParser(description="' + project_title + ' CLI")\n    parser.add_argument("--name", default="Engineer", help="User name")\n    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")\n    args = parser.parse_args()\n    \n    print(f"CodePilot [{project_title}] running.")\n    print(f"Welcome, {args.name}! System initialized.")\n\nif __name__ == "__main__":\n    main()\n'
        })
        files.append({
            "filename": "utils.py",
            "content": '"""Utility functions and formatting helpers."""\n\ndef format_bytes(size_bytes: int) -> str:\n    if size_bytes < 1024:\n        return f"{size_bytes} B"\n    return f"{size_bytes / 1024:.1f} KB"\n'
        })
    elif lang == "javascript":
        files.append({
            "filename": "index.js",
            "content": '/**\n * ' + project_title + ' CLI Application\n */\nconst readline = require("readline");\n\nfunction main() {\n  console.log("==========================================");\n  console.log("  ' + project_title + ' — Node.js CLI");\n  console.log("==========================================");\n  console.log("Running in CodePilot Isolated Runtime.");\n}\n\nmain();\n'
        })
    elif lang == "typescript":
        files.append({
            "filename": "main.ts",
            "content": 'interface AppConfig {\n  name: string;\n  version: string;\n  debug: boolean;\n}\n\nconst config: AppConfig = {\n  name: "' + project_title + '",\n  version: "1.0.0",\n  debug: true\n};\n\nconsole.log(`[CodePilot] Initialized ${config.name} v${config.version}`);\n'
        })
    elif lang == "cpp":
        files.append({
            "filename": "main.cpp",
            "content": '#include <iostream>\n#include <string>\n\nint main(int argc, char* argv[]) {\n    std::cout << "========================================\\n";\n    std::cout << "  ' + project_title + ' (C++20 CLI Engine)\\n";\n    std::cout << "========================================\\n";\n    std::cout << "Status: Healthy\\n";\n    return 0;\n}\n'
        })
    elif lang == "c":
        files.append({
            "filename": "main.c",
            "content": '#include <stdio.h>\n\nint main() {\n    printf("CodePilot C Application: %s\\n", "' + project_title + '");\n    return 0;\n}\n'
        })
    elif lang == "java":
        files.append({
            "filename": "Main.java",
            "content": 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("CodePilot Java Workspace: ' + project_title + '");\n        System.out.println("Runtime: OpenJDK 21");\n    }\n}\n'
        })
    elif lang == "go":
        files.append({
            "filename": "main.go",
            "content": 'package main\n\nimport "fmt"\n\nfunc main() {\n\tfmt.Println("CodePilot Go CLI: ' + project_title + '")\n\tfmt.Println("Ready for execution.")\n}\n'
        })
    elif lang == "rust":
        files.append({
            "filename": "main.rs",
            "content": 'fn main() {\n    println!("CodePilot Rust Workspace: {} ready.", "' + project_title + '");\n}\n'
        })
    elif lang == "csharp":
        files.append({
            "filename": "Program.cs",
            "content": 'using System;\n\nclass Program {\n    static void Main() {\n        Console.WriteLine("CodePilot .NET C# Workspace: ' + project_title + '");\n    }\n}\n'
        })
    elif lang == "php":
        files.append({
            "filename": "index.php",
            "content": '<?php\n\necho "CodePilot PHP 8.3 Workspace: ' + project_title + '\\n";\n'
        })
    elif lang == "ruby":
        files.append({
            "filename": "main.rb",
            "content": '# CodePilot Ruby Workspace\nputs "CodePilot Ruby Workspace: ' + project_title + '"\n'
        })
    elif lang == "kotlin":
        files.append({
            "filename": "Main.kt",
            "content": 'fun main() {\n    println("CodePilot Kotlin Workspace: ' + project_title + '")\n}\n'
        })
    else:
        files.append({
            "filename": f"main.{ext}",
            "content": f"// CodePilot Workspace: {project_title}\n"
        })

    files.append({
        "filename": "README.md",
        "content": f"# {project_title}\n\nA professional developer workspace built on **CodePilot**.\n\n- **Language**: `{language}`\n- **Template**: `{template}`\n- **Created**: `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}`\n"
    })
    return files


class ProjectRepository:
    @staticmethod
    def get_user_projects(user_id: int) -> List[Dict[str, Any]]:
        with get_db_session() as db:
            projects = db.query(Project).filter(Project.user_id == user_id).order_by(Project.updated_at.desc()).all()
            return [p.to_dict(include_files=False) for p in projects]

    @staticmethod
    def get_project_details(project_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            project = db.query(Project).filter(
                Project.id == project_id,
                ((Project.user_id == user_id) | (Project.is_public == True))
            ).first()
            if not project:
                return None
            return project.to_dict(include_files=True)

    @staticmethod
    def create_project(user_id: int, title: str, description: str = "", language: str = "python", template: str = "cli") -> Dict[str, Any]:
        with get_db_session() as db:
            proj = Project(
                user_id=user_id,
                title=title.strip() or "Untitled Project",
                description=description.strip(),
                primary_language=language.lower(),
                is_public=False
            )
            db.add(proj)
            db.flush()

            # Generate multi-file scaffolding
            scaffold_files = get_template_scaffolding(language, template, title)
            for sf in scaffold_files:
                pfile = ProjectFile(
                    project_id=proj.id,
                    filename=sf["filename"],
                    file_path=f"/{sf['filename']}",
                    content=sf["content"]
                )
                db.add(pfile)

            db.commit()
            db.refresh(proj)
            return proj.to_dict(include_files=True)

    @staticmethod
    def rename_project(project_id: int, user_id: int, title: str, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            proj = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
            if not proj:
                return None
            if title:
                proj.title = title.strip()
            if description is not None:
                proj.description = description.strip()
            proj.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(proj)
            return proj.to_dict(include_files=False)

    @staticmethod
    def duplicate_project(project_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        with get_db_session() as db:
            orig = db.query(Project).filter(
                Project.id == project_id,
                ((Project.user_id == user_id) | (Project.is_public == True))
            ).first()
            if not orig:
                return None

            new_proj = Project(
                user_id=user_id,
                title=f"{orig.title} (Copy)",
                description=orig.description,
                primary_language=orig.primary_language,
                is_public=False
            )
            db.add(new_proj)
            db.flush()

            # Copy all files
            for of in orig.files:
                nf = ProjectFile(
                    project_id=new_proj.id,
                    filename=of.filename,
                    file_path=of.file_path,
                    content=of.content,
                    is_directory=of.is_directory
                )
                db.add(nf)

            db.commit()
            db.refresh(new_proj)
            return new_proj.to_dict(include_files=True)

    @staticmethod
    def delete_project(project_id: int, user_id: int) -> bool:
        with get_db_session() as db:
            proj = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
            if not proj:
                return False
            db.delete(proj)
            db.commit()
            return True

    @staticmethod
    def update_file(project_id: int, user_id: int, filename: str, content: str) -> bool:
        with get_db_session() as db:
            proj = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
            if not proj:
                return False

            pfile = db.query(ProjectFile).filter(
                ProjectFile.project_id == project_id,
                ProjectFile.filename == filename
            ).first()

            if pfile:
                pfile.content = content
                pfile.updated_at = datetime.now(timezone.utc)
            else:
                pfile = ProjectFile(
                    project_id=project_id,
                    filename=filename,
                    file_path=f"/{filename}",
                    content=content
                )
                db.add(pfile)

            proj.updated_at = datetime.now(timezone.utc)
            db.commit()
            return True

    @staticmethod
    def delete_file(project_id: int, user_id: int, filename: str) -> bool:
        with get_db_session() as db:
            proj = db.query(Project).filter(Project.id == project_id, Project.user_id == user_id).first()
            if not proj:
                return False

            pfile = db.query(ProjectFile).filter(
                ProjectFile.project_id == project_id,
                ProjectFile.filename == filename
            ).first()

            if not pfile:
                return False

            db.delete(pfile)
            proj.updated_at = datetime.now(timezone.utc)
            db.commit()
            return True

/* Multi-Language IDE Editor Component (Python, C, C++, Java, JS, R, SQL) */
import { store } from '../state/store.js';
import { ExecutionService } from '../services/ExecutionService.js';
import { NotificationService } from '../services/NotificationService.js';

export const LANGUAGE_TEMPLATES = {
  python: {
    filename: 'main.py',
    language: 'python',
    label: '🐍 Python 3',
    code: `# Python 3 Code Execution\ndef main():\n    nums = [10, 20, 30, 40, 50]\n    print(f"Python Array Sum: {sum(nums)}")\n    print("Execution completed successfully!")\n\nif __name__ == '__main__':\n    main()`
  },
  c: {
    filename: 'main.c',
    language: 'c',
    label: '⚡ C (GCC)',
    code: `/* C Language Execution */\n#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    printf("Hello from C Execution Engine!\\n");\n    int sum = 0;\n    for (int i = 1; i <= 10; i++) {\n        sum += i;\n    }\n    printf("Sum of 1 to 10 = %d\\n", sum);\n    return 0;\n}`
  },
  cpp: {
    filename: 'main.cpp',
    language: 'cpp',
    label: '🚀 C++ 20 (GCC)',
    code: `// C++ 20 Language Execution\n#include <iostream>\n#include <vector>\n#include <numeric>\nusing namespace std;\n\nint main() {\n    vector<int> data = {5, 15, 25, 35, 45};\n    int total = accumulate(data.begin(), data.end(), 0);\n    cout << "C++ Vector Total: " << total << endl;\n    return 0;\n}`
  },
  java: {
    filename: 'Main.java',
    language: 'java',
    label: '☕ Java 21',
    code: `// Java 21 Execution\nimport java.util.*;\n\npublic class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello from Java 21 Execution Engine!");\n        List<String> langs = Arrays.asList("Python", "C", "C++", "Java", "JavaScript", "R", "SQL");\n        System.out.println("Supported Languages: " + langs);\n    }\n}`
  },
  javascript: {
    filename: 'script.js',
    language: 'javascript',
    label: '🟨 JavaScript (Node.js)',
    code: `// JavaScript Node.js Execution\nfunction calculateFactorial(n) {\n    if (n <= 1) return 1;\n    return n * calculateFactorial(n - 1);\n}\n\nconsole.log("JavaScript Execution:");\nconsole.log("Factorial(5) =", calculateFactorial(5));`
  },
  r: {
    filename: 'analysis.R',
    language: 'r',
    label: '📊 R Language',
    code: `# R Language Data Processing\ncat("R Execution Engine Active\\n")\nvector_data <- c(12.5, 18.2, 24.9, 31.0, 45.6)\ncat("Vector Mean:", mean(vector_data), "\\n")\ncat("Vector Standard Deviation:", sd(vector_data), "\\n")`
  },
  sql: {
    filename: 'query.sql',
    language: 'sql',
    label: '🗄️ SQL Database',
    code: `-- SQL Relational Query Execution\nCREATE TABLE developers (\n    id INTEGER PRIMARY KEY,\n    name TEXT,\n    language TEXT,\n    score INTEGER\n);\n\nINSERT INTO developers VALUES (1, 'Alex', 'Python', 98);\nINSERT INTO developers VALUES (2, 'Sarah', 'C++', 95);\nINSERT INTO developers VALUES (3, 'Elena', 'R', 92);\n\nSELECT * FROM developers WHERE score >= 95;`
  }
};

export class IdeEditorComponent {
  constructor(containerId, initialLanguage = 'python') {
    this.containerId = containerId;
    this.selectedLanguage = initialLanguage;
    this.files = Object.values(LANGUAGE_TEMPLATES).map(t => ({
      name: t.filename,
      language: t.language,
      content: t.code
    }));
    this.activeFileIndex = this.files.findIndex(f => f.language === initialLanguage);
    if (this.activeFileIndex === -1) this.activeFileIndex = 0;
    
    this.customInput = '';
    this.executionResult = null;
    this.isExecuting = false;
  }

  render() {
    const activeFile = this.files[this.activeFileIndex];
    const linesCount = activeFile.content.split('\n').length;
    const lineNumbersHtml = Array.from({ length: Math.max(linesCount, 15) }, (_, i) => i + 1).join('<br>');

    return `
      <div class="ide-workspace w-full">
        <!-- Top Language Bar & Controls -->
        <div class="ide-toolbar">
          <div class="ide-toolbar-left">
            <label style="font-size: var(--fs-xs); font-weight: 600; color: var(--text-muted);">Select Language:</label>
            <select id="ide-language-select" class="btn btn-secondary btn-sm" style="padding: 3px 10px; font-weight: 600;">
              ${Object.keys(LANGUAGE_TEMPLATES).map(key => {
                const t = LANGUAGE_TEMPLATES[key];
                return `<option value="${t.language}" ${t.language === activeFile.language ? 'selected' : ''}>${t.label}</option>`;
              }).join('')}
            </select>

            <button id="btn-ide-reset" class="btn btn-secondary btn-sm" title="Reset starter code">🔄 Reset Template</button>
          </div>

          <div class="ide-toolbar-right">
            <button id="btn-ide-run" class="btn btn-primary btn-sm">
              <span>▶ Execute Code (${activeFile.language.toUpperCase()})</span>
            </button>
          </div>
        </div>

        <!-- Main Workspace Grid -->
        <div class="ide-main-container">
          <!-- Left File Sidebar -->
          <div class="ide-sidebar">
            <div class="ide-sidebar-header">
              <span>Language Files</span>
            </div>
            <ul class="file-tree">
              ${this.files.map((file, idx) => `
                <li class="file-item ${idx === this.activeFileIndex ? 'active' : ''}" data-index="${idx}">
                  <span>📄</span>
                  <span>${file.name}</span>
                </li>
              `).join('')}
            </ul>
          </div>

          <!-- Code Editor Center Area -->
          <div class="ide-editor-area">
            <div class="editor-tabs">
              ${this.files.map((file, idx) => `
                <div class="editor-tab ${idx === this.activeFileIndex ? 'active' : ''}" data-index="${idx}">
                  <span>${file.name}</span>
                </div>
              `).join('')}
            </div>

            <div class="code-editor-wrapper">
              <div class="line-numbers">${lineNumbersHtml}</div>
              <textarea id="ide-textarea" class="code-textarea" spellcheck="false">${activeFile.content}</textarea>
              <div class="editor-minimap">${activeFile.content.replace(/\n/g, '<br>')}</div>
            </div>

            <!-- Console Output Panel -->
            <div class="ide-console-panel">
              <div class="console-header">
                <div class="flex items-center gap-3">
                  <strong style="font-size: var(--fs-xs); text-transform: uppercase;">Execution Output Console</strong>
                  ${this.executionResult ? `
                    <span class="output-status-pill ${this.executionResult.status === 'Accepted' ? 'status-accepted' : 'status-error'}">
                      ${this.executionResult.status}
                    </span>
                    <span class="text-muted" style="font-size: var(--fs-xs);">Runtime: ${this.executionResult.runtime} | Memory: ${this.executionResult.memory}</span>
                  ` : ''}
                </div>
                <button id="btn-clear-console" class="btn btn-secondary btn-sm" style="padding: 1px 6px; font-size: 11px;">Clear Output</button>
              </div>
              <div id="console-output-body" class="console-body">
                ${this.isExecuting ? `<div style="color: var(--accent-cyan);">Preparing environment & running ${activeFile.language.toUpperCase()} execution worker...</div>` : (this.executionResult ? `<pre>${this.executionResult.output}</pre>` : '<div class="text-muted">Click "Execute Code" above to compile and run your program.</div>')}
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  attachEvents() {
    const container = document.getElementById(this.containerId);
    if (!container) return;

    const textarea = container.querySelector('#ide-textarea');
    if (textarea) {
      textarea.addEventListener('input', (e) => {
        this.files[this.activeFileIndex].content = e.target.value;
      });
    }

    // Language selector change
    const langSelect = container.querySelector('#ide-language-select');
    if (langSelect) {
      langSelect.addEventListener('change', (e) => {
        const lang = e.target.value;
        const targetIndex = this.files.findIndex(f => f.language === lang);
        if (targetIndex !== -1) {
          this.activeFileIndex = targetIndex;
          container.innerHTML = this.render();
          this.attachEvents();
        }
      });
    }

    // Reset template
    const resetBtn = container.querySelector('#btn-ide-reset');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        const activeFile = this.files[this.activeFileIndex];
        const template = LANGUAGE_TEMPLATES[activeFile.language];
        if (template) {
          activeFile.content = template.code;
          container.innerHTML = this.render();
          this.attachEvents();
          NotificationService.showToast(`Reset ${template.label} template`, 'info');
        }
      });
    }

    // File item click
    container.querySelectorAll('.file-item, .editor-tab').forEach(item => {
      item.addEventListener('click', () => {
        const index = parseInt(item.getAttribute('data-index'), 10);
        if (!isNaN(index)) {
          this.activeFileIndex = index;
          container.innerHTML = this.render();
          this.attachEvents();
        }
      });
    });

    // Execute Code
    const runBtn = container.querySelector('#btn-ide-run');
    if (runBtn) {
      runBtn.addEventListener('click', async () => {
        const activeFile = this.files[this.activeFileIndex];
        this.isExecuting = true;
        container.innerHTML = this.render();
        this.attachEvents();

        this.executionResult = await ExecutionService.run({
          language: activeFile.language,
          sourceCode: activeFile.content
        });

        this.isExecuting = false;
        container.innerHTML = this.render();
        this.attachEvents();
        NotificationService.showToast(`Executed ${activeFile.language.toUpperCase()}: ${this.executionResult.status}`, this.executionResult.status === 'Accepted' ? 'success' : 'error');
      });
    }
  }
}

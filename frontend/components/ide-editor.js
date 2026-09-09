/* Professional 3-Column + Bottom Dock Developer IDE Component */
import { store } from '../state/store.js';
import { ExecutionService } from '../services/ExecutionService.js';
import { AIService } from '../services/AIService.js';
import { NotificationService } from '../services/NotificationService.js';

export const LANGUAGE_TEMPLATES = {
  python: {
    filename: 'main.py',
    language: 'python',
    label: 'Python 3',
    icon: '🐍',
    code: `def solve():\n    \"\"\"CodePilot Solution Runner\"\"\"\n    import sys\n    data = sys.stdin.read().split()\n    if data:\n        print(f"Read {len(data)} tokens from stdin.")\n    else:\n        print("Hello from CodePilot Enterprise Python Engine!")\n\nif __name__ == '__main__':\n    solve()\n`
  },
  javascript: {
    filename: 'index.js',
    language: 'javascript',
    label: 'JavaScript (Node.js)',
    icon: '🟨',
    code: `function solve() {\n    const fs = require('fs');\n    const input = fs.readFileSync(0, 'utf-8').trim();\n    console.log("Hello from CodePilot JavaScript Engine!");\n    if (input) console.log("Stdin Input:", input);\n}\nsolve();\n`
  },
  java: {
    filename: 'Main.java',
    language: 'java',
    label: 'Java 21',
    icon: '☕',
    code: `import java.util.Scanner;\n\npublic class Main {\n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        System.out.println("Hello from CodePilot Java Engine!");\n        if (sc.hasNext()) {\n            System.out.println("Received: " + sc.next());\n        }\n    }\n}\n`
  },
  cpp: {
    filename: 'main.cpp',
    language: 'cpp',
    label: 'C++ 20',
    icon: '🚀',
    code: `#include <iostream>\n#include <vector>\n#include <string>\n\nusing namespace std;\n\nint main() {\n    ios_base::sync_with_stdio(false);\n    cin.tie(NULL);\n    cout << "Hello from CodePilot C++20 Engine!" << endl;\n    string s;\n    if (cin >> s) {\n        cout << "Stdin: " << s << endl;\n    }\n    return 0;\n}\n`
  },
  c: {
    filename: 'main.c',
    language: 'c',
    label: 'C (GCC)',
    icon: '⚡',
    code: `#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    printf("Hello from CodePilot C Engine!\\n");\n    char buf[128];\n    if (scanf("%127s", buf) == 1) {\n        printf("Stdin: %s\\n", buf);\n    }\n    return 0;\n}\n`
  },
  go: {
    filename: 'main.go',
    language: 'go',
    label: 'Go',
    icon: '🐹',
    code: `package main\n\nimport (\n    \"fmt\"\n    \"os\"\n    \"io\"\n)\n\nfunc main() {\n    fmt.Println(\"Hello from CodePilot Go Engine!\")\n    b, _ := io.ReadAll(os.Stdin)\n    if len(b) > 0 {\n        fmt.Printf(\"Stdin: %s\\n\", string(b))\n    }\n}\n`
  },
  rust: {
    filename: 'main.rs',
    language: 'rust',
    label: 'Rust',
    icon: '🦀',
    code: `use std::io::{self, Read};\n\nfn main() {\n    println!(\"Hello from CodePilot Rust Engine!\");\n    let mut buffer = String::new();\n    if io::stdin().read_to_string(&mut buffer).is_ok() && !buffer.trim().is_empty() {\n        println!(\"Stdin: {}\", buffer.trim());\n    }\n}\n`
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

    this.activeBottomTab = 'output'; // output, stdin, terminal
    this.stdinInput = '';
    this.executionResult = null;
    this.isExecuting = false;
    this.aiPanelVisible = true;
    this.aiReport = null;
    this.isAiAnalyzing = false;
  }

  render() {
    const activeFile = this.files[this.activeFileIndex];
    const lines = activeFile.content.split('\n');
    const linesCount = lines.length;
    const lineNumbersHtml = Array.from({ length: Math.max(linesCount, 20) }, (_, i) => i + 1).join('<br>');

    return `
      <div class="ide-workspace w-full h-full">
        <!-- Top IDE Header Bar -->
        <div class="ide-toolbar">
          <div class="ide-toolbar-left">
            <div class="ide-breadcrumb">
              <span>workspace</span>
              <span>/</span>
              <span>src</span>
              <span>/</span>
              <span class="active-file">${activeFile.name}</span>
            </div>

            <select id="ide-language-select" class="btn btn-secondary btn-sm" style="font-size: 11px; padding: 2px 8px; margin-left: 8px;">
              ${Object.keys(LANGUAGE_TEMPLATES).map(k => {
                const t = LANGUAGE_TEMPLATES[k];
                return `<option value="${t.language}" ${t.language === activeFile.language ? 'selected' : ''}>${t.icon} ${t.label}</option>`;
              }).join('')}
            </select>

            <button id="btn-ide-format" class="btn btn-secondary btn-sm" title="Auto-Format">⚡ Format</button>
            <button id="btn-ide-reset" class="btn btn-secondary btn-sm" title="Reset starter code">🔄 Reset</button>
          </div>

          <div class="ide-toolbar-right">
            <button id="btn-toggle-ai" class="btn btn-secondary btn-sm ${this.aiPanelVisible ? 'active' : ''}">
              ✨ Pilot AI
            </button>

            <button id="btn-ide-run" class="btn btn-primary btn-sm" ${this.isExecuting ? 'disabled' : ''}>
              <span>${this.isExecuting ? '⏳ Running...' : '▶ Run Code (Ctrl+Enter)'}</span>
            </button>
          </div>
        </div>

        <!-- 3-Column Main Workspace -->
        <div class="ide-main-container">
          <!-- Left Column: File Explorer -->
          <div class="ide-sidebar">
            <div class="ide-sidebar-header">
              <span>Project Explorer</span>
              <span style="font-size: 10px; color: var(--text-muted);">${this.files.length} Files</span>
            </div>
            <ul class="file-tree">
              ${this.files.map((file, idx) => `
                <li class="file-item ${idx === this.activeFileIndex ? 'active' : ''}" data-index="${idx}">
                  <span>${LANGUAGE_TEMPLATES[file.language]?.icon || '📄'}</span>
                  <span>${file.name}</span>
                </li>
              `).join('')}
            </ul>
          </div>

          <!-- Center Column: Multi-Tab Editor Area -->
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
            </div>

            <!-- Status Bar -->
            <div class="editor-status-bar">
              <div class="editor-status-bar-group">
                <span>Ln ${linesCount}, Col 1</span>
                <span>Spaces: 4</span>
                <span>UTF-8</span>
              </div>
              <div class="editor-status-bar-group">
                <span>${activeFile.language.toUpperCase()}</span>
                <span>Ready</span>
              </div>
            </div>

            <!-- Bottom Console / Output / Terminal Dock -->
            <div class="ide-console-panel">
              <div class="console-header">
                <div class="console-tabs">
                  <div class="console-tab ${this.activeBottomTab === 'output' ? 'active' : ''}" data-bottom-tab="output">
                    Console Output
                  </div>
                  <div class="console-tab ${this.activeBottomTab === 'stdin' ? 'active' : ''}" data-bottom-tab="stdin">
                    Stdin Input
                  </div>
                  <div class="console-tab ${this.activeBottomTab === 'terminal' ? 'active' : ''}" data-bottom-tab="terminal">
                    Terminal
                  </div>
                </div>

                <div class="flex items-center gap-2">
                  ${this.executionResult ? `
                    <span class="output-status-pill ${this.executionResult.status === 'Accepted' || this.executionResult.status === 'ACCEPTED' ? 'status-accepted' : 'status-error'}">
                      ${this.executionResult.status}
                    </span>
                    <span style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">
                      ${this.executionResult.runtime || this.executionResult.runtimeSeconds + 's'} | ${this.executionResult.memory || this.executionResult.memoryMb + ' MB'}
                    </span>
                  ` : ''}
                  <button id="btn-clear-console" class="btn btn-secondary btn-sm" style="font-size: 10px; padding: 1px 6px;">Clear</button>
                </div>
              </div>

              <div class="console-body">
                ${this.activeBottomTab === 'stdin' ? `
                  <textarea id="ide-stdin-input" class="w-full h-full" style="background: transparent; color: var(--accent-primary); border: none; outline: none; font-family: var(--font-mono); resize: none;" placeholder="Type custom stdin input here (passed to input(), scanf, cin >>, etc)...">${this.stdinInput}</textarea>
                ` : (this.activeBottomTab === 'terminal' ? `
                  <div style="font-family: var(--font-mono); line-height: 1.6;">
                    <div style="color: var(--text-muted);">$ codepilot run ${activeFile.name}</div>
                    <div style="color: var(--text-primary);">${this.executionResult ? (this.executionResult.stdout || this.executionResult.output || this.executionResult.stderr || '[No Output]') : '[Ready for execution]'}</div>
                  </div>
                ` : `
                  ${this.isExecuting ? `
                    <div style="color: var(--accent-primary); font-family: var(--font-mono);">
                      ⏳ Executing in isolated sandbox environment...
                    </div>
                  ` : (this.executionResult ? `
                    <pre style="margin: 0; white-space: pre-wrap; word-break: break-all;">${this.executionResult.stdout || this.executionResult.output || this.executionResult.stderr || '[Execution finished with no output]'}</pre>
                  ` : `
                    <div style="color: var(--text-muted);">Click "Run Code" (or Ctrl+Enter) to compile and execute program.</div>
                  `)}
                `)}
              </div>
            </div>
          </div>

          <!-- Right Column: Pilot AI Assistant Panel -->
          ${this.aiPanelVisible ? `
            <div class="ide-ai-panel">
              <div class="ide-ai-header">
                <div class="flex items-center gap-1">
                  <span>✨</span>
                  <span>Pilot AI Assistant</span>
                </div>
                <button id="btn-close-ai" class="btn btn-icon btn-sm" style="width: 20px; height: 20px; font-size: 11px;">✕</button>
              </div>

              <div class="ide-ai-body">
                <div class="ai-action-grid">
                  <button id="btn-ai-review" class="btn btn-secondary btn-sm">🔍 Code Review</button>
                  <button id="btn-ai-complexity" class="btn btn-secondary btn-sm">📊 Complexity</button>
                  <button id="btn-ai-tests" class="btn btn-secondary btn-sm">🧪 Unit Tests</button>
                  <button id="btn-ai-bug" class="btn btn-secondary btn-sm">🐞 Find Bugs</button>
                </div>

                ${this.isAiAnalyzing ? `
                  <div style="text-align: center; padding: 20px; color: var(--text-muted); font-size: 12px;">
                    <div>✨ Analyzing AST & code patterns...</div>
                  </div>
                ` : (this.aiReport ? `
                  <div class="ai-card-result">
                    <div class="ai-card-result-title">${this.aiReport.title || 'Analysis Result'}</div>
                    <div style="color: var(--text-secondary); line-height: 1.5; font-size: 12px;">
                      ${this.aiReport.content}
                    </div>
                  </div>
                ` : `
                  <div style="text-align: center; padding: 24px 8px; color: var(--text-muted); font-size: 12px;">
                    <div>Ready to assist. Click any AI tool above to analyze the current editor buffer.</div>
                  </div>
                `)}
              </div>
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }

  attachEvents() {
    const container = document.getElementById(this.containerId);
    if (!container) return;

    // Code textarea input
    const textarea = container.querySelector('#ide-textarea');
    if (textarea) {
      textarea.addEventListener('input', (e) => {
        this.files[this.activeFileIndex].content = e.target.value;
      });

      // Keyboard Shortcut Ctrl+Enter to Run
      textarea.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
          e.preventDefault();
          this.executeActiveCode();
        }
      });
    }

    // Stdin textarea input
    const stdinEl = container.querySelector('#ide-stdin-input');
    if (stdinEl) {
      stdinEl.addEventListener('input', (e) => {
        this.stdinInput = e.target.value;
      });
    }

    // Language Selector
    const langSelect = container.querySelector('#ide-language-select');
    if (langSelect) {
      langSelect.addEventListener('change', (e) => {
        const lang = e.target.value;
        const targetIndex = this.files.findIndex(f => f.language === lang);
        if (targetIndex !== -1) {
          this.activeFileIndex = targetIndex;
          this.refresh();
        }
      });
    }

    // File selection
    container.querySelectorAll('.file-item, .editor-tab').forEach(item => {
      item.addEventListener('click', () => {
        const index = parseInt(item.getAttribute('data-index'), 10);
        if (!isNaN(index)) {
          this.activeFileIndex = index;
          this.refresh();
        }
      });
    });

    // Reset button
    const resetBtn = container.querySelector('#btn-ide-reset');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        const activeFile = this.files[this.activeFileIndex];
        const t = LANGUAGE_TEMPLATES[activeFile.language];
        if (t) {
          activeFile.content = t.code;
          this.refresh();
          NotificationService.showToast(`Reset ${t.label} code`, 'info');
        }
      });
    }

    // Auto-Format
    const formatBtn = container.querySelector('#btn-ide-format');
    if (formatBtn) {
      formatBtn.addEventListener('click', () => {
        const activeFile = this.files[this.activeFileIndex];
        activeFile.content = activeFile.content.split('\n').map(l => l.trimRight()).join('\n');
        this.refresh();
        NotificationService.showToast('Formatted buffer', 'success');
      });
    }

    // Toggle AI Panel
    const toggleAiBtn = container.querySelector('#btn-toggle-ai');
    if (toggleAiBtn) {
      toggleAiBtn.addEventListener('click', () => {
        this.aiPanelVisible = !this.aiPanelVisible;
        this.refresh();
      });
    }

    const closeAiBtn = container.querySelector('#btn-close-ai');
    if (closeAiBtn) {
      closeAiBtn.addEventListener('click', () => {
        this.aiPanelVisible = false;
        this.refresh();
      });
    }

    // Bottom Console Tabs
    container.querySelectorAll('.console-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        this.activeBottomTab = tab.getAttribute('data-bottom-tab');
        this.refresh();
      });
    });

    // Clear Console
    const clearBtn = container.querySelector('#btn-clear-console');
    if (clearBtn) {
      clearBtn.addEventListener('click', () => {
        this.executionResult = null;
        this.refresh();
      });
    }

    // Run Code
    const runBtn = container.querySelector('#btn-ide-run');
    if (runBtn) {
      runBtn.addEventListener('click', () => this.executeActiveCode());
    }

    // AI Tools Event Handlers
    const reviewBtn = container.querySelector('#btn-ai-review');
    if (reviewBtn) {
      reviewBtn.addEventListener('click', async () => {
        const activeFile = this.files[this.activeFileIndex];
        this.isAiAnalyzing = true;
        this.refresh();
        const res = await AIService.review(activeFile.language, activeFile.content);
        this.isAiAnalyzing = false;
        this.aiReport = {
          title: `Code Review (${res.qualityScore || 90}/100)`,
          content: res.output || res.review || 'No issues detected. Code adheres to standard conventions.'
        };
        this.refresh();
      });
    }

    const complexityBtn = container.querySelector('#btn-ai-complexity');
    if (complexityBtn) {
      complexityBtn.addEventListener('click', async () => {
        const activeFile = this.files[this.activeFileIndex];
        this.isAiAnalyzing = true;
        this.refresh();
        const res = await AIService.complexity(activeFile.language, activeFile.content);
        this.isAiAnalyzing = false;
        this.aiReport = {
          title: 'Complexity Estimation',
          content: `Time Complexity: <strong>${res.timeComplexity || 'O(N)'}</strong><br>Space Complexity: <strong>${res.spaceComplexity || 'O(1)'}</strong>`
        };
        this.refresh();
      });
    }

    const testsBtn = container.querySelector('#btn-ai-tests');
    if (testsBtn) {
      testsBtn.addEventListener('click', async () => {
        const activeFile = this.files[this.activeFileIndex];
        this.isAiAnalyzing = true;
        this.refresh();
        const res = await AIService.generateTests(activeFile.language, activeFile.content);
        this.isAiAnalyzing = false;
        this.aiReport = {
          title: 'Generated Unit Tests',
          content: `<pre style="font-size: 11px; max-height: 200px; overflow-y: auto;">${res.tests || res.output || '// Generated test suite'}</pre>`
        };
        this.refresh();
      });
    }

    const bugBtn = container.querySelector('#btn-ai-bug');
    if (bugBtn) {
      bugBtn.addEventListener('click', async () => {
        const activeFile = this.files[this.activeFileIndex];
        this.isAiAnalyzing = true;
        this.refresh();
        const res = await AIService.explainBug(activeFile.language, activeFile.content, this.executionResult?.stderr || '');
        this.isAiAnalyzing = false;
        this.aiReport = {
          title: 'Bug Analysis & Diagnostics',
          content: res.explanation || res.output || 'No critical bugs or syntax errors detected in current buffer.'
        };
        this.refresh();
      });
    }
  }

  async executeActiveCode() {
    const activeFile = this.files[this.activeFileIndex];
    this.isExecuting = true;
    this.activeBottomTab = 'output';
    this.refresh();

    this.executionResult = await ExecutionService.run({
      language: activeFile.language,
      sourceCode: activeFile.content,
      stdin: this.stdinInput
    });

    this.isExecuting = false;
    this.refresh();
    const isSuccess = this.executionResult.status === 'Accepted' || this.executionResult.status === 'ACCEPTED';
    NotificationService.showToast(`Executed ${activeFile.language.toUpperCase()}: ${this.executionResult.status}`, isSuccess ? 'success' : 'error');
  }

  refresh() {
    const container = document.getElementById(this.containerId);
    if (container) {
      container.innerHTML = this.render();
      this.attachEvents();
    }
  }
}

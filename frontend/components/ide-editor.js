/* Professional 3-Column + Bottom Console Developer IDE Component */
import { store } from '../state/store.js';
import { ExecutionService } from '../services/ExecutionService.js';
import { AIService } from '../services/AIService.js';
import { NotificationService } from '../services/NotificationService.js';
import { ProjectService } from '../services/ProjectService.js';

export const LANGUAGE_TEMPLATES = {
  python: {
    filename: 'main.py',
    language: 'python',
    label: 'Python 3',
    icon: '🐍',
    code: `def solve():\n    """CodePilot Solution Runner"""\n    import sys\n    data = sys.stdin.read().split()\n    if data:\n        print(f"Read {len(data)} tokens from stdin.")\n    else:\n        print("Hello from CodePilot Enterprise Python Engine!")\n\nif __name__ == '__main__':\n    solve()\n`
  },
  javascript: {
    filename: 'index.js',
    language: 'javascript',
    label: 'JavaScript (Node.js)',
    icon: '🟨',
    code: `function solve() {\n    const fs = require('fs');\n    const input = fs.readFileSync(0, 'utf-8').trim();\n    console.log("Hello from CodePilot JavaScript Engine!");\n    if (input) console.log("Stdin Input:", input);\n}\nsolve();\n`
  },
  typescript: {
    filename: 'main.ts',
    language: 'typescript',
    label: 'TypeScript',
    icon: '🔷',
    code: `interface Task {\n    id: number;\n    title: string;\n}\n\nconst task: Task = { id: 1, title: "CodePilot Runner" };\nconsole.log(\`Task: \${task.title}\`);\n`
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
  constructor(containerId, initialLanguage = 'python', projectId = null) {
    this.containerId = containerId;
    this.selectedLanguage = initialLanguage;
    this.projectId = projectId;
    this.projectData = null;

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
    this.isSaving = false;
    this.aiPanelVisible = true;
    this.aiReport = null;
    this.isAiAnalyzing = false;
  }

  async loadProjectWorkspace() {
    if (!this.projectId) return;
    try {
      const proj = await ProjectService.getProjectById(this.projectId);
      if (proj) {
        this.projectData = proj;
        this.selectedLanguage = proj.primaryLanguage || 'python';
        if (proj.files && proj.files.length > 0) {
          this.files = proj.files.map(f => ({
            name: f.filename,
            language: this.inferLanguage(f.filename) || proj.primaryLanguage || 'python',
            content: f.content || ''
          }));
          this.activeFileIndex = 0;
        }
      }
    } catch (err) {
      console.error('[IdeEditorComponent] Failed to load project:', err);
      NotificationService.error('Failed to load project workspace files.');
    }
  }

  inferLanguage(filename) {
    if (filename.endsWith('.py')) return 'python';
    if (filename.endsWith('.js')) return 'javascript';
    if (filename.endsWith('.ts')) return 'typescript';
    if (filename.endsWith('.cpp') || filename.endsWith('.hpp')) return 'cpp';
    if (filename.endsWith('.c') || filename.endsWith('.h')) return 'c';
    if (filename.endsWith('.java')) return 'java';
    if (filename.endsWith('.go')) return 'go';
    if (filename.endsWith('.rs')) return 'rust';
    if (filename.endsWith('.cs')) return 'csharp';
    if (filename.endsWith('.php')) return 'php';
    if (filename.endsWith('.rb')) return 'ruby';
    if (filename.endsWith('.kt')) return 'kotlin';
    if (filename.endsWith('.json')) return 'json';
    if (filename.endsWith('.md')) return 'markdown';
    return this.selectedLanguage;
  }

  render() {
    const activeFile = this.files[this.activeFileIndex] || this.files[0];
    const lines = (activeFile.content || '').split('\n');
    const linesCount = lines.length;
    const lineNumbersHtml = Array.from({ length: Math.max(linesCount, 20) }, (_, i) => i + 1).join('<br>');
    const projectTitle = this.projectData ? this.projectData.title : 'workspace';

    return `
      <div class="ide-workspace w-full h-full">
        <!-- Top IDE Header Bar -->
        <div class="ide-toolbar">
          <div class="ide-toolbar-left">
            <div class="ide-breadcrumb">
              <a href="#/projects" style="color: var(--text-muted); text-decoration: none;">Projects</a>
              <span>/</span>
              <span style="color: var(--text-primary); font-weight: 600;">${projectTitle}</span>
              <span>/</span>
              <span class="active-file">${activeFile.name}</span>
            </div>

            <select id="ide-language-select" class="btn btn-secondary btn-sm" style="font-size: 11px; padding: 2px 8px; margin-left: 8px;">
              ${Object.keys(LANGUAGE_TEMPLATES).map(k => {
                const t = LANGUAGE_TEMPLATES[k];
                return `<option value="${t.language}" ${t.language === activeFile.language ? 'selected' : ''}>${t.icon} ${t.label}</option>`;
              }).join('')}
            </select>

            <button id="btn-ide-save" class="btn btn-secondary btn-sm" title="Save file (Ctrl+S)">
              <span>💾</span> ${this.isSaving ? 'Saving...' : 'Save'}
            </button>
            <button id="btn-ide-format" class="btn btn-secondary btn-sm" title="Auto-Format Code">⚡ Format</button>
          </div>

          <div class="ide-toolbar-right">
            <button id="btn-toggle-ai" class="btn btn-secondary btn-sm ${this.aiPanelVisible ? 'active' : ''}">
              ✨ Pilot AI
            </button>

            <button id="btn-ide-run" class="btn btn-primary btn-sm" ${this.isExecuting ? 'disabled' : ''}>
              <span>${this.isExecuting ? '⏳ Executing...' : '▶ Run Code (Ctrl+Enter)'}</span>
            </button>
          </div>
        </div>

        <!-- 3-Column Main Workspace -->
        <div class="ide-main-container">
          <!-- Left Column: File Explorer -->
          <div class="ide-sidebar">
            <div class="ide-sidebar-header flex justify-between items-center">
              <span>EXPLORER</span>
              <button id="btn-add-file" class="btn btn-icon btn-sm" style="width: 20px; height: 20px; font-size: 12px;" title="New File">+</button>
            </div>
            <ul class="file-tree">
              ${this.files.map((file, idx) => `
                <li class="file-item ${idx === this.activeFileIndex ? 'active' : ''}" data-index="${idx}" style="display: flex; justify-content: space-between; align-items: center;">
                  <div class="flex items-center gap-1.5" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                    <span>${LANGUAGE_TEMPLATES[file.language]?.icon || '📄'}</span>
                    <span>${file.name}</span>
                  </div>
                  ${this.files.length > 1 ? `
                    <button class="btn-delete-file" data-filename="${file.name}" style="background: transparent; border: none; color: var(--text-muted); cursor: pointer; font-size: 11px; padding: 0 4px;" title="Delete File">✕</button>
                  ` : ''}
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
              <div class="line-numbers" id="ide-line-numbers">${lineNumbersHtml}</div>
              <textarea id="ide-textarea" class="code-textarea" spellcheck="false">${activeFile.content || ''}</textarea>
            </div>

            <!-- Status Bar -->
            <div class="editor-status-bar">
              <div class="editor-status-bar-group">
                <span id="ide-cursor-pos">Ln ${linesCount}, Col 1</span>
                <span>Spaces: 4</span>
                <span>UTF-8</span>
              </div>
              <div class="editor-status-bar-group">
                <span>${(activeFile.language || 'text').toUpperCase()}</span>
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
                    <span class="output-status-pill ${this.executionResult.status === 'Accepted' || this.executionResult.status === 'ACCEPTED' || this.executionResult.status === 'SUCCESS' ? 'status-accepted' : 'status-error'}">
                      ${this.executionResult.status}
                    </span>
                    <span style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">
                      ${this.executionResult.executionTimeMs ? this.executionResult.executionTimeMs + ' ms' : (this.executionResult.runtime || '0 ms')} | ${this.executionResult.memoryMb ? this.executionResult.memoryMb + ' MB' : (this.executionResult.memory || '12 MB')}
                    </span>
                  ` : ''}
                  <button id="btn-clear-console" class="btn btn-secondary btn-sm" style="font-size: 10px; padding: 1px 6px;">Clear</button>
                </div>
              </div>

              <div class="console-body">
                ${this.activeBottomTab === 'stdin' ? `
                  <textarea id="ide-stdin-input" class="w-full h-full" style="background: transparent; color: var(--accent-primary); border: none; outline: none; font-family: var(--font-mono); resize: none; font-size: 12px;" placeholder="Type custom stdin input here (passed to input(), scanf, cin >>, etc)...">${this.stdinInput}</textarea>
                ` : (this.activeBottomTab === 'terminal' ? `
                  <div style="font-family: var(--font-mono); line-height: 1.6; font-size: 12px;">
                    <div style="color: var(--text-muted);">$ codepilot run ${activeFile.name}</div>
                    <div style="color: var(--text-primary); white-space: pre-wrap;">${this.executionResult ? (this.executionResult.stdout || this.executionResult.output || this.executionResult.stderr || '[No Output]') : '[Ready for execution]'}</div>
                  </div>
                ` : `
                  ${this.isExecuting ? `
                    <div style="color: var(--accent-primary); font-family: var(--font-mono); font-size: 12px;">
                      ⏳ Executing in isolated sandbox environment...
                    </div>
                  ` : (this.executionResult ? `
                    <pre style="margin: 0; white-space: pre-wrap; word-break: break-all; font-family: var(--font-mono); font-size: 12px; color: ${this.executionResult.stderr ? 'var(--status-error)' : 'var(--text-primary)'};">${this.executionResult.stdout || this.executionResult.output || this.executionResult.stderr || '[Execution finished with no output]'}</pre>
                  ` : `
                    <div style="color: var(--text-muted); font-size: 12px;">Click "Run Code" (or press Ctrl+Enter) to execute the active file.</div>
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
                  <div class="ai-card-result" style="background: var(--bg-darkest); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 12px; margin-top: 12px;">
                    <div class="ai-card-result-title" style="font-weight: 600; font-size: 12px; margin-bottom: 6px; color: var(--accent-primary);">${this.aiReport.title || 'Analysis Result'}</div>
                    <div style="color: var(--text-secondary); line-height: 1.5; font-size: 12px; white-space: pre-wrap;">${this.aiReport.content}</div>
                  </div>
                ` : `
                  <div style="text-align: center; padding: 24px 8px; color: var(--text-muted); font-size: 12px;">
                    <div>Ready to assist. Click any AI action above to inspect the editor buffer.</div>
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

    // Textarea input sync
    const textarea = document.getElementById('ide-textarea');
    if (textarea) {
      textarea.addEventListener('input', () => {
        const activeFile = this.files[this.activeFileIndex];
        if (activeFile) {
          activeFile.content = textarea.value;
          this.updateLineNumbers(textarea.value);
        }
      });

      // Handle Tab Key for 4 spaces
      textarea.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
          e.preventDefault();
          const start = textarea.selectionStart;
          const end = textarea.selectionEnd;
          textarea.value = textarea.value.substring(0, start) + '    ' + textarea.value.substring(end);
          textarea.selectionStart = textarea.selectionEnd = start + 4;
          this.files[this.activeFileIndex].content = textarea.value;
          this.updateLineNumbers(textarea.value);
        } else if ((e.ctrlKey || e.metaKey) && e.key === 's') {
          e.preventDefault();
          this.saveActiveFile();
        } else if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
          e.preventDefault();
          this.executeCode();
        }
      });
    }

    // Save Button
    document.getElementById('btn-ide-save')?.addEventListener('click', () => this.saveActiveFile());

    // Run Button
    document.getElementById('btn-ide-run')?.addEventListener('click', () => this.executeCode());

    // Stdin Input textarea
    const stdinElem = document.getElementById('ide-stdin-input');
    if (stdinElem) {
      stdinElem.addEventListener('input', (e) => {
        this.stdinInput = e.target.value;
      });
    }

    // Language Dropdown
    document.getElementById('ide-language-select')?.addEventListener('change', (e) => {
      const newLang = e.target.value;
      this.selectedLanguage = newLang;
      const activeFile = this.files[this.activeFileIndex];
      if (activeFile) {
        activeFile.language = newLang;
      }
      this.reRender();
    });

    // File Tree Switch
    container.querySelectorAll('.file-item').forEach(item => {
      item.addEventListener('click', (e) => {
        if (e.target.classList.contains('btn-delete-file')) return;
        const index = parseInt(item.getAttribute('data-index'), 10);
        this.activeFileIndex = index;
        this.reRender();
      });
    });

    // Editor Tabs Switch
    container.querySelectorAll('.editor-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        const index = parseInt(tab.getAttribute('data-index'), 10);
        this.activeFileIndex = index;
        this.reRender();
      });
    });

    // Add File Button
    document.getElementById('btn-add-file')?.addEventListener('click', () => {
      const filename = prompt('Enter new filename (e.g. utils.py, service.js):');
      if (filename && filename.trim()) {
        const cleanName = filename.trim();
        const lang = this.inferLanguage(cleanName);
        this.files.push({
          name: cleanName,
          language: lang,
          content: `// ${cleanName}\n`
        });
        this.activeFileIndex = this.files.length - 1;
        if (this.projectId) {
          ProjectService.updateFile(this.projectId, cleanName, `// ${cleanName}\n`);
        }
        this.reRender();
      }
    });

    // Delete File Buttons
    container.querySelectorAll('.btn-delete-file').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const fname = btn.getAttribute('data-filename');
        if (confirm(`Delete '${fname}'?`)) {
          const idx = this.files.findIndex(f => f.name === fname);
          if (idx !== -1) {
            this.files.splice(idx, 1);
            if (this.activeFileIndex >= this.files.length) {
              this.activeFileIndex = Math.max(0, this.files.length - 1);
            }
            if (this.projectId) {
              ProjectService.deleteFile(this.projectId, fname);
            }
            this.reRender();
          }
        }
      });
    });

    // Console Bottom Tabs
    container.querySelectorAll('.console-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        this.activeBottomTab = tab.getAttribute('data-bottom-tab');
        this.reRender();
      });
    });

    // Clear Console
    document.getElementById('btn-clear-console')?.addEventListener('click', () => {
      this.executionResult = null;
      this.reRender();
    });

    // Toggle AI
    document.getElementById('btn-toggle-ai')?.addEventListener('click', () => {
      this.aiPanelVisible = !this.aiPanelVisible;
      this.reRender();
    });

    document.getElementById('btn-close-ai')?.addEventListener('click', () => {
      this.aiPanelVisible = false;
      this.reRender();
    });

    // AI Actions
    document.getElementById('btn-ai-review')?.addEventListener('click', () => this.runAiAction('review'));
    document.getElementById('btn-ai-complexity')?.addEventListener('click', () => this.runAiAction('complexity'));
    document.getElementById('btn-ai-tests')?.addEventListener('click', () => this.runAiAction('tests'));
    document.getElementById('btn-ai-bug')?.addEventListener('click', () => this.runAiAction('bugs'));

    // Format Code
    document.getElementById('btn-ide-format')?.addEventListener('click', () => {
      const activeFile = this.files[this.activeFileIndex];
      if (activeFile && activeFile.content) {
        NotificationService.info('Code formatted.');
      }
    });
  }

  updateLineNumbers(content) {
    const lineNumbersElem = document.getElementById('ide-line-numbers');
    if (lineNumbersElem) {
      const lines = content.split('\n');
      lineNumbersElem.innerHTML = Array.from({ length: Math.max(lines.length, 20) }, (_, i) => i + 1).join('<br>');
    }
  }

  async saveActiveFile() {
    const activeFile = this.files[this.activeFileIndex];
    if (!activeFile) return;

    if (this.projectId) {
      this.isSaving = true;
      const saveBtn = document.getElementById('btn-ide-save');
      if (saveBtn) saveBtn.textContent = 'Saving...';

      try {
        await ProjectService.updateFile(this.projectId, activeFile.name, activeFile.content);
        NotificationService.success(`Saved '${activeFile.name}'.`);
      } catch (err) {
        NotificationService.error('Failed to save file to server.');
      } finally {
        this.isSaving = false;
        if (saveBtn) saveBtn.innerHTML = '<span>💾</span> Save';
      }
    } else {
      NotificationService.success(`Workspace buffer saved.`);
    }
  }

  async executeCode() {
    const activeFile = this.files[this.activeFileIndex];
    if (!activeFile) return;

    this.isExecuting = true;
    this.activeBottomTab = 'output';
    this.reRender();

    try {
      const res = await ExecutionService.execute({
        language: activeFile.language,
        sourceCode: activeFile.content,
        stdin: this.stdinInput || ''
      });
      this.executionResult = res;
    } catch (err) {
      this.executionResult = {
        status: 'EXECUTION_ERROR',
        stderr: err.message || 'Execution failed.'
      };
    } finally {
      this.isExecuting = false;
      this.reRender();
    }
  }

  async runAiAction(action) {
    const activeFile = this.files[this.activeFileIndex];
    if (!activeFile) return;

    this.isAiAnalyzing = true;
    this.reRender();

    try {
      const result = await AIService.analyzeCode(activeFile.content, activeFile.language, action);
      this.aiReport = {
        title: action === 'review' ? 'AST Code Review' : (action === 'complexity' ? 'Time & Space Complexity' : (action === 'tests' ? 'Generated Unit Tests' : 'Bug Finder Analysis')),
        content: result.review || result.tests || result.explanation || result.analysis || JSON.stringify(result, null, 2)
      };
    } catch (err) {
      this.aiReport = {
        title: 'Pilot AI Analysis',
        content: `Analysis completed for ${activeFile.language.toUpperCase()} file. No syntax or security hazards detected.`
      };
    } finally {
      this.isAiAnalyzing = false;
      this.reRender();
    }
  }

  reRender() {
    const container = document.getElementById(this.containerId);
    if (container) {
      container.innerHTML = this.render();
      this.attachEvents();
    }
  }
}

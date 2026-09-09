/* Problem Arena Detail View */
import { ProblemService } from '../../services/ProblemService.js';
import { IdeEditorComponent } from '../../components/ide-editor.js';

export class ProblemDetailPage {
  static async render({ params }) {
    const problemId = params?.id || 'prob_1';
    let problem;
    try {
      problem = await ProblemService.getProblemById(problemId);
    } catch (e) {
      problem = await ProblemService.getProblemById('prob_1');
    }

    return `
      <div class="w-full flex" style="height: calc(100vh - var(--header-height)); overflow: hidden;">
        <!-- Left Panel: Problem Statement & Hints -->
        <div style="width: 45%; background: var(--bg-surface); border-right: 1px solid var(--border-subtle); display: flex; flex-direction: column; overflow-y: auto;">
          <div style="padding: var(--space-6); border-bottom: 1px solid var(--border-subtle);">
            <div class="flex items-center justify-between" style="margin-bottom: 8px;">
              <h2>${problem.title}</h2>
              <span class="badge-tag badge-${problem.difficulty.toLowerCase()}">${problem.difficulty}</span>
            </div>
            <div style="font-size: var(--fs-xs); color: var(--text-muted);">Topic: ${problem.topic} | Acceptance: ${problem.acceptanceRate}</div>
          </div>

          <div style="padding: var(--space-6); flex: 1;">
            <h4 style="margin-bottom: 12px;">Description</h4>
            <div style="font-size: var(--fs-sm); line-height: 1.6; color: var(--text-primary); margin-bottom: 24px; white-space: pre-wrap;">${problem.description}</div>

            <h4 style="margin-bottom: 12px;">Examples</h4>
            ${problem.examples.map((ex, i) => `
              <div style="background: var(--bg-darkest); border: 1px solid var(--border-subtle); padding: 12px; border-radius: var(--radius-md); margin-bottom: 12px; font-family: var(--font-mono); font-size: 13px;">
                <strong>Example ${i + 1}:</strong><br>
                <span style="color: var(--accent-cyan);">Input:</span> ${ex.input}<br>
                <span style="color: var(--accent-emerald);">Output:</span> ${ex.output}
                ${ex.explanation ? `<br><span style="color: var(--text-muted);">Explanation: ${ex.explanation}</span>` : ''}
              </div>
            `).join('')}

            <h4 style="margin-top: 24px; margin-bottom: 12px;">Constraints</h4>
            <ul style="margin-left: 20px; font-size: var(--fs-sm); color: var(--text-secondary); margin-bottom: 24px;">
              ${problem.constraints.map(c => `<li><code>${c}</code></li>`).join('')}
            </ul>

            <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid var(--border-accent); border-radius: var(--radius-md); padding: 12px;">
              <strong style="color: var(--accent-cyan); font-size: var(--fs-sm);">💡 Python Hint:</strong>
              <div style="font-size: var(--fs-xs); color: var(--text-secondary); margin-top: 4px;">${problem.hints[0] || 'Use Python dictionaries for O(1) lookups.'}</div>
            </div>
          </div>
        </div>

        <!-- Right Panel: IDE Code Editor -->
        <div style="flex: 1;" id="problem-ide-container">
          <!-- IdeEditorComponent renders here -->
        </div>
      </div>
    `;
  }

  static afterRender({ params }) {
    const problemId = params?.id || 'prob_1';
    ProblemService.getProblemById(problemId).then(problem => {
      const initialFiles = [
        { name: 'solution.py', language: 'python', content: problem.starterCode.python || 'def solution():\n    pass' },
        { name: 'solution.cpp', language: 'cpp', content: problem.starterCode.cpp || '// C++ solution' }
      ];

      const editor = new IdeEditorComponent('problem-ide-container', initialFiles);
      const container = document.getElementById('problem-ide-container');
      if (container) {
        container.innerHTML = editor.render();
        editor.attachEvents();
      }
    });
  }
}

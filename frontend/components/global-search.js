/* Global Command Palette Search Modal (Ctrl+K) */
import { mockProblems } from '../mock-data/problems.js';

export class GlobalSearchComponent {
  static render() {
    return `
      <div id="command-palette-overlay" class="modal-overlay">
        <div class="modal-container command-palette-container">
          <input type="text" id="command-search-input" class="command-input" placeholder="Search problems, tools, languages... (Esc to close)" />
          <div id="command-search-results" class="command-results">
            <!-- Results rendered dynamically -->
          </div>
        </div>
      </div>
    `;
  }

  static attachEvents(router) {
    const overlay = document.getElementById('command-palette-overlay');
    const input = document.getElementById('command-search-input');
    const resultsContainer = document.getElementById('command-search-results');

    const openModal = () => {
      overlay.classList.add('active');
      input.value = '';
      input.focus();
      renderResults('');
    };

    const closeModal = () => {
      overlay.classList.remove('active');
    };

    window.addEventListener('open-command-palette', openModal);

    window.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        openModal();
      }
      if (e.key === 'Escape') closeModal();
    });

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal();
    });

    input.addEventListener('input', (e) => {
      renderResults(e.target.value.trim().toLowerCase());
    });

    function renderResults(query) {
      let html = '';

      // Match Problems
      const filteredProbs = mockProblems.filter(p => p.title.toLowerCase().includes(query) || p.topic.toLowerCase().includes(query));
      if (filteredProbs.length) {
        html += `<div style="font-size: var(--fs-xs); font-weight:700; color: var(--text-muted); padding: 8px 12px; text-transform: uppercase;">Problems</div>`;
        filteredProbs.forEach(p => {
          html += `
            <div class="command-item" data-hash="#/problems/${p.id}">
              <div>
                <strong style="color: var(--text-primary);">${p.title}</strong>
                <span class="badge-tag badge-${p.difficulty.toLowerCase()}" style="margin-left: 8px;">${p.difficulty}</span>
              </div>
              <span class="text-muted" style="font-size: var(--fs-xs);">${p.topic}</span>
            </div>
          `;
        });
      }

      // Languages Shortcuts
      html += `
        <div style="font-size: var(--fs-xs); font-weight:700; color: var(--text-muted); padding: 8px 12px; text-transform: uppercase; margin-top: 8px;">Languages Studio</div>
        <div class="command-item" data-hash="#/ide?lang=python"><span>🐍 Python 3 Workbench</span></div>
        <div class="command-item" data-hash="#/ide?lang=c"><span>⚡ C (GCC) Workbench</span></div>
        <div class="command-item" data-hash="#/ide?lang=cpp"><span>🚀 C++ 20 Workbench</span></div>
        <div class="command-item" data-hash="#/ide?lang=java"><span>☕ Java 21 Workbench</span></div>
        <div class="command-item" data-hash="#/ide?lang=javascript"><span>🟨 JavaScript Node.js</span></div>
        <div class="command-item" data-hash="#/ide?lang=r"><span>📊 R Language Data</span></div>
        <div class="command-item" data-hash="#/ide?lang=sql"><span>🗄️ SQL Database Query</span></div>
      `;

      resultsContainer.innerHTML = html;

      resultsContainer.querySelectorAll('.command-item').forEach(item => {
        item.addEventListener('click', () => {
          const hash = item.getAttribute('data-hash');
          if (hash) {
            closeModal();
            window.location.hash = hash;
          }
        });
      });
    }
  }
}

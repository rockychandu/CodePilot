/* Multi-Language Standalone & Project Developer IDE Page */
import { IdeEditorComponent } from '../components/ide-editor.js';

export class IdePage {
  static async render({ queryParams }) {
    return `
      <div class="w-full" style="height: calc(100vh - var(--header-height)); overflow: hidden;">
        <div id="standalone-ide-container" class="h-full">
          <div style="padding: 24px; color: var(--text-muted); font-family: var(--font-mono); font-size: 13px;">
            Initializing developer workspace...
          </div>
        </div>
      </div>
    `;
  }

  static async afterRender({ queryParams }) {
    const selectedLang = queryParams?.lang || 'python';
    const projectId = queryParams?.project || queryParams?.projectId || null;

    const editor = new IdeEditorComponent('standalone-ide-container', selectedLang, projectId);
    if (projectId) {
      await editor.loadProjectWorkspace();
    }
    const container = document.getElementById('standalone-ide-container');
    if (container) {
      container.innerHTML = editor.render();
      editor.attachEvents();
    }
  }
}

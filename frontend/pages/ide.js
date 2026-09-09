/* Multi-Language Standalone IDE Page */
import { IdeEditorComponent } from '../components/ide-editor.js';

export class IdePage {
  static async render({ queryParams }) {
    const lang = queryParams?.lang || 'python';
    return `
      <div class="w-full" style="height: calc(100vh - var(--header-height)); overflow: hidden;">
        <div id="standalone-ide-container" class="h-full">
          <!-- IdeEditorComponent renders here -->
        </div>
      </div>
    `;
  }

  static afterRender({ queryParams }) {
    const selectedLang = queryParams?.lang || 'python';
    const editor = new IdeEditorComponent('standalone-ide-container', selectedLang);
    const container = document.getElementById('standalone-ide-container');
    if (container) {
      container.innerHTML = editor.render();
      editor.attachEvents();
    }
  }
}

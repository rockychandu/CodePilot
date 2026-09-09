/* Standalone Terminal Page Module */
import { TerminalViewComponent } from '../components/terminal-view.js';

export class TerminalPage {
  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Standalone Terminal Workspace</h1>
            <p class="text-secondary">Execute CodePilot CLI commands, test Python scripts, and manage files.</p>
          </div>
        </div>

        <div id="standalone-terminal-container">
          <!-- TerminalViewComponent renders here -->
        </div>
      </div>
    `;
  }

  static afterRender() {
    const term = new TerminalViewComponent('standalone-terminal-container');
    const container = document.getElementById('standalone-terminal-container');
    if (container) {
      container.innerHTML = term.render();
      term.attachEvents();
    }
  }
}

/* Interactive Terminal Emulator Component */

export class TerminalViewComponent {
  constructor(containerId) {
    this.containerId = containerId;
    this.history = [
      'CodePilot Terminal Environment v2.4.0 (Python Engine Ready)',
      'Type "help" to view available commands.'
    ];
  }

  render() {
    return `
      <div class="terminal-window w-full">
        <div class="terminal-titlebar">
          <div class="terminal-dots">
            <span class="terminal-dot dot-red"></span>
            <span class="terminal-dot dot-yellow"></span>
            <span class="terminal-dot dot-green"></span>
          </div>
          <span style="font-size: var(--fs-xs); color: var(--text-muted);">bash -- codepilot-cli</span>
          <span></span>
        </div>

        <div id="terminal-content" class="terminal-content">
          ${this.history.map(line => `<div class="terminal-line">${line}</div>`).join('')}
          <div class="terminal-input-row">
            <span class="terminal-prompt">codepilot@dev:~$</span>
            <input type="text" id="terminal-input" class="terminal-input" autofocus />
          </div>
        </div>
      </div>
    `;
  }

  attachEvents() {
    const container = document.getElementById(this.containerId);
    if (!container) return;

    const input = container.querySelector('#terminal-input');
    const content = container.querySelector('#terminal-content');

    if (input) {
      input.focus();
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
          const command = input.value.trim();
          if (command) {
            this.executeCommand(command);
            input.value = '';
            container.innerHTML = this.render();
            this.attachEvents();
            content.scrollTop = content.scrollHeight;
          }
        }
      });
    }
  }

  executeCommand(cmd) {
    this.history.push(`<span class="terminal-prompt">codepilot@dev:~$</span> ${cmd}`);

    const parts = cmd.split(' ');
    const main = parts[0].toLowerCase();

    switch (main) {
      case 'help':
        this.history.push('Available Commands:\n  help        - Show this help message\n  clear       - Clear terminal output\n  python      - Run Python interpreter simulation\n  ls          - List directory files\n  whoami      - Display current user\n  version     - Show CodePilot CLI version');
        break;
      case 'clear':
        this.history = [];
        break;
      case 'ls':
        this.history.push('main.py   utils.py   solution.cpp   config.json   README.md');
        break;
      case 'whoami':
        this.history.push('alex_dev (Role: Student, Rating: 1845)');
        break;
      case 'version':
        this.history.push('CodePilot CLI v2.4.0 (Python Core Engine)');
        break;
      case 'python':
        this.history.push('Python 3.12.2 (main, Feb 2026)\nType "print(\'Hello\')" to test code execution.');
        break;
      default:
        this.history.push(`command not found: ${cmd}. Type "help" for available commands.`);
        break;
    }
  }
}

/* Footer Component */

export class FooterComponent {
  static render() {
    return `
      <footer style="background: var(--bg-surface); border-top: 1px solid var(--border-subtle); padding: var(--space-8) var(--space-6); margin-top: auto;">
        <div class="container flex justify-between items-center" style="flex-wrap: wrap; gap: var(--space-4);">
          <div class="flex items-center gap-3">
            <img src="frontend/assets/logo.svg" style="width: 24px; height: 24px;" alt="Logo" />
            <span style="font-weight: 700; font-size: var(--fs-sm);">CodePilot</span>
            <span class="text-muted" style="font-size: var(--fs-xs);">© 2026 CodePilot. Code. Build. Compete.</span>
          </div>

          <div class="flex items-center gap-6" style="font-size: var(--fs-xs); color: var(--text-secondary);">
            <a href="#/languages">Languages Studio</a>
            <a href="#/ide">Multi-Lang IDE</a>
            <a href="#/problems">Problems</a>
            <a href="#/contests">Contests</a>
            <a href="#/terminal">Terminal</a>
            <a href="#/admin">Admin Panel</a>
          </div>

          <div class="flex items-center gap-2" style="font-size: var(--fs-xs);">
            <span style="width: 8px; height: 8px; border-radius: 50%; background: var(--status-success); display: inline-block;"></span>
            <span style="color: var(--text-secondary);">Multi-Language Engine: Active (Python, C, C++, Java, JS, R, SQL)</span>
          </div>
        </div>
      </footer>
    `;
  }
}

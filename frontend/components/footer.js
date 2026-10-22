/* Minimalist Developer Footer Component */
export class FooterComponent {
  static render() {
    const isLanding = window.location.hash === '#/' || window.location.hash === '' || window.location.hash === '#/home';
    if (!isLanding) {
      return `
        <footer class="app-footer-compact">
          <div class="flex items-center gap-3">
            <span>CodePilot v2.1.0 (Production Engine)</span>
            <span>•</span>
            <span>All systems operational</span>
          </div>
          <div class="flex items-center gap-3">
            <a href="#/diagnostics" style="color: var(--text-muted); text-decoration: none;">Runtimes</a>
            <span>•</span>
            <a href="#/settings" style="color: var(--text-muted); text-decoration: none;">Settings</a>
            <span>•</span>
            <a href="#/community" style="color: var(--text-muted); text-decoration: none;">Community</a>
          </div>
        </footer>
      `;
    }

    return `
      <footer style="background: var(--bg-surface); border-top: 1px solid var(--border-subtle); padding: var(--space-8) var(--space-4); margin-top: auto;">
        <div style="max-width: var(--max-content-width); margin: 0 auto; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: var(--space-4);">
          <div class="flex items-center gap-2">
            <img src="frontend/assets/logo.svg" alt="CodePilot" style="width: 20px; height: 20px;" />
            <span style="font-weight: 700; color: var(--text-primary); font-size: 14px;">CodePilot Developer Platform</span>
          </div>
          <div class="flex items-center gap-4" style="font-size: 12px; color: var(--text-secondary);">
            <a href="#/dashboard" style="color: var(--text-secondary); text-decoration: none;">Dashboard</a>
            <a href="#/ide" style="color: var(--text-secondary); text-decoration: none;">Cloud IDE</a>
            <a href="#/problems" style="color: var(--text-secondary); text-decoration: none;">Problems</a>
            <a href="#/contests" style="color: var(--text-secondary); text-decoration: none;">Contests</a>
            <a href="#/projects" style="color: var(--text-secondary); text-decoration: none;">Projects</a>
          </div>
          <div style="font-size: 11px; color: var(--text-muted);">
            © 2026 CodePilot. Proprietary & Confidential.
          </div>
        </div>
      </footer>
    `;
  }
}

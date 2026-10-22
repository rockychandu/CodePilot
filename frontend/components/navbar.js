/* Professional Developer Navbar Component */
import { store } from '../state/store.js';
import { AuthService } from '../services/AuthService.js';

export class NavbarComponent {
  static render() {
    const user = store.get('currentUser') || AuthService.getCurrentUser();
    const isAuth = Boolean(user && AuthService.isAuthenticated());
    const currentHash = window.location.hash || '#/';

    const navItems = [
      { hash: '#/dashboard', label: 'Dashboard' },
      { hash: '#/ide', label: 'IDE' },
      { hash: '#/problems', label: 'Problems' },
      { hash: '#/contests', label: 'Contests' },
      { hash: '#/projects', label: 'Projects' },
      { hash: '#/learning', label: 'Learning' },
      { hash: '#/community', label: 'Community' }
    ];

    const isAdmin = user?.role === 'ADMIN';

    return `
      <header class="navbar">
        <div class="flex items-center gap-6">
          <a href="#/" class="nav-brand">
            <img src="frontend/assets/logo.svg" alt="CodePilot" class="nav-logo-icon" />
            <span>CodePilot</span>
          </a>

          <nav>
            <ul class="nav-links">
              ${navItems.map(item => {
                const isActive = currentHash.startsWith(item.hash) ? 'active' : '';
                return `<li><a href="${item.hash}" class="nav-link ${isActive}">${item.label}</a></li>`;
              }).join('')}
            </ul>
          </nav>
        </div>

        <div class="nav-actions">
          <button id="btn-global-search" class="btn btn-secondary btn-sm" title="Search (Ctrl+K)">
            <span>🔍</span>
            <span style="font-size: 11px;">Search</span>
            <kbd style="background: var(--bg-darkest); padding: 1px 4px; border-radius: 3px; font-size: 10px; border: 1px solid var(--border-subtle);">Ctrl K</kbd>
          </button>

          <a href="#/ai" class="btn btn-outline btn-sm" title="Pilot AI Assistant">✨ Pilot</a>

          ${isAuth ? `
            <div class="dropdown-holder">
              <button id="nav-user-menu-btn" class="btn btn-secondary btn-sm flex items-center gap-2" style="padding: 3px 8px;">
                <span class="user-avatar-initial" style="width: 20px; height: 20px; border-radius: 50%; background: var(--accent-primary); color: #fff; font-size: 11px; font-weight: 700; display: inline-flex; align-items: center; justify-content: center;">
                  ${(user.username || 'U')[0].toUpperCase()}
                </span>
                <span style="font-family: var(--font-mono); font-size: 12px; font-weight: 600;">${user.username}</span>
                <span style="font-size: 9px; opacity: 0.6;">▼</span>
              </button>

              <div id="nav-user-dropdown" class="dropdown-menu">
                <div style="padding: 6px 12px; border-bottom: 1px solid var(--border-subtle);">
                  <div style="font-weight: 600; font-size: 12px; color: var(--text-primary);">${user.profile?.displayName || user.username}</div>
                  <div style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">${user.email || user.role || 'DEVELOPER'}</div>
                </div>
                <a href="#/profile" class="dropdown-item">👤 Profile</a>
                <a href="#/projects" class="dropdown-item">📁 My Projects</a>
                <a href="#/history" class="dropdown-item">📜 Activity History</a>
                <a href="#/settings" class="dropdown-item">⚙️ Settings</a>
                ${isAdmin ? `<a href="#/admin" class="dropdown-item" style="color: var(--accent-primary); font-weight: 600;">🛡️ Admin Center</a>` : ''}
                <div class="dropdown-divider"></div>
                <button id="btn-nav-logout" class="dropdown-item danger">🚪 Sign Out</button>
              </div>
            </div>
          ` : `
            <a href="#/login" class="btn btn-secondary btn-sm">Sign In</a>
            <a href="#/register" class="btn btn-primary btn-sm">Create Account</a>
          `}
        </div>
      </header>
    `;
  }

  static attachEvents() {
    const searchBtn = document.getElementById('btn-global-search');
    if (searchBtn) {
      searchBtn.addEventListener('click', () => {
        window.dispatchEvent(new CustomEvent('open-command-palette'));
      });
    }

    const userMenuBtn = document.getElementById('nav-user-menu-btn');
    const userDropdown = document.getElementById('nav-user-dropdown');
    if (userMenuBtn && userDropdown) {
      userMenuBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        userDropdown.classList.toggle('show');
      });

      document.addEventListener('click', () => {
        userDropdown.classList.remove('show');
      });
    }

    const logoutBtn = document.getElementById('btn-nav-logout');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', async () => {
        await AuthService.logout();
        store.set('currentUser', null);
        store.set('isAuthenticated', false);
        window.location.hash = '#/login';
      });
    }
  }
}

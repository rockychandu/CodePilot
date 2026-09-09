/* Navbar Component */
import { store } from '../state/store.js';

export class NavbarComponent {
  static render() {
    const user = store.get('currentUser');
    const isAuth = store.get('isAuthenticated');

    return `
      <header class="navbar">
        <a href="#/" class="nav-brand">
          <img src="frontend/assets/logo.svg" alt="CodePilot Logo" class="nav-logo-icon" />
          <span>CodePilot</span>
        </a>

        <ul class="nav-links">
          <li><a href="#/dashboard" class="nav-link">Dashboard</a></li>
          <li><a href="#/languages" class="nav-link">Languages Studio</a></li>
          <li><a href="#/ide" class="nav-link">Multi-Lang IDE</a></li>
          <li><a href="#/problems" class="nav-link">Problems</a></li>
          <li><a href="#/contests" class="nav-link">Contests</a></li>
          <li><a href="#/projects" class="nav-link">Projects</a></li>
          <li><a href="#/community" class="nav-link">Community</a></li>
        </ul>

        <div class="nav-actions">
          <button id="btn-global-search" class="btn btn-secondary btn-sm" title="Search (Ctrl+K)">
            <span>🔍 Search</span>
            <kbd style="background: var(--bg-darkest); padding: 1px 5px; border-radius: 4px; font-size: 10px;">Ctrl K</kbd>
          </button>

          <a href="#/ai" class="btn btn-outline btn-sm">✨ Pilot AI</a>

          ${isAuth ? `
            <a href="#/profile/${user?.username || 'alex_dev'}" class="btn btn-secondary btn-sm flex items-center gap-2">
              <img src="${user?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=50&auto=format&fit=crop&q=80'}" style="width:24px; height:24px; border-radius:50%;" />
              <span>${user?.username || 'Profile'}</span>
            </a>
            <a href="#/settings" class="btn btn-icon btn-sm" title="Settings">⚙️</a>
          ` : `
            <a href="#/login" class="btn btn-secondary btn-sm">Sign In</a>
            <a href="#/register" class="btn btn-primary btn-sm">Get Started</a>
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
  }
}

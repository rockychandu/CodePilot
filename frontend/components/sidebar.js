/**
 * Compact Developer Sidebar Component for Authenticated Application Views
 */
import { store } from '../state/store.js';
import { AuthService } from '../services/AuthService.js';

export class SidebarComponent {
  static render() {
    const user = store.get('currentUser') || AuthService.getCurrentUser();
    const isAuth = Boolean(user && AuthService.isAuthenticated());
    if (!isAuth) return '';

    const currentHash = window.location.hash || '#/dashboard';
    const isAdmin = user?.role === 'ADMIN';

    const sections = [
      {
        title: 'Workspace',
        items: [
          { hash: '#/dashboard', icon: '📊', label: 'Dashboard' },
          { hash: '#/projects', icon: '📁', label: 'My Projects' },
          { hash: '#/history', icon: '📜', label: 'History' }
        ]
      },
      {
        title: 'Learn',
        items: [
          { hash: '#/problems', icon: '🧩', label: 'Problems' },
          { hash: '#/contests', icon: '🏆', label: 'Contests' },
          { hash: '#/learning', icon: '📚', label: 'Courses' }
        ]
      },
      {
        title: 'Tools',
        items: [
          { hash: '#/ide', icon: '💻', label: 'IDE' },
          { hash: '#/ai', icon: '✨', label: 'Pilot AI' },
          { hash: '#/diagnostics', icon: '⚡', label: 'Runtimes' }
        ]
      },
      {
        title: 'System',
        items: [
          { hash: '#/settings', icon: '⚙️', label: 'Settings' },
          ...(isAdmin ? [{ hash: '#/admin', icon: '🛡️', label: 'Admin Center' }] : [])
        ]
      }
    ];

    return `
      <aside class="app-sidebar" id="app-sidebar">
        ${sections.map(sec => `
          <div class="sidebar-section">
            <div class="sidebar-section-title">${sec.title}</div>
            ${sec.items.map(item => {
              const isActive = currentHash.startsWith(item.hash) ? 'active' : '';
              return `
                <a href="${item.hash}" class="sidebar-link ${isActive}">
                  <span class="sidebar-link-icon">${item.icon}</span>
                  <span>${item.label}</span>
                </a>
              `;
            }).join('')}
          </div>
        `).join('')}
      </aside>
    `;
  }
}

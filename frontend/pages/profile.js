/* Developer Profile Page Module */
import { store } from '../state/store.js';

export class ProfilePage {
  static async render({ params }) {
    const user = store.get('currentUser') || {
      name: 'Alex Developer',
      username: params?.username || 'alex_dev',
      email: 'alex.developer@codepilot.io',
      rating: 1845,
      solvedCount: 142,
      xp: 4250,
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
      bio: 'Passionate Python & Algorithms Engineer building commercial open-source projects.'
    };

    return `
      <div class="page-wrapper">
        <div class="card flex items-center gap-6" style="margin-bottom: var(--space-8);">
          <img src="${user.avatar}" style="width: 96px; height: 96px; border-radius: 50%; border: 3px solid var(--accent-cyan);" />
          <div style="flex: 1;">
            <div class="flex items-center gap-3">
              <h2>${user.name}</h2>
              <span class="badge-tag badge-medium">Level ${user.level || 12}</span>
            </div>
            <p class="text-secondary" style="margin-top: 2px;">@${user.username} • ${user.email}</p>
            <p class="text-muted" style="font-size: var(--fs-sm); margin-top: 8px;">${user.bio}</p>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-6">
          <div class="card">
            <h4>Contest Rating</h4>
            <div style="font-size: var(--fs-3xl); font-weight: 800; color: var(--accent-purple); margin-top: 8px;">${user.rating}</div>
            <div class="text-muted" style="font-size: 11px;">Top 5% Globally</div>
          </div>
          <div class="card">
            <h4>Problems Solved</h4>
            <div style="font-size: var(--fs-3xl); font-weight: 800; color: var(--accent-cyan); margin-top: 8px;">${user.solvedCount}</div>
            <div class="text-muted" style="font-size: 11px;">142 Python Submissions</div>
          </div>
          <div class="card">
            <h4>Total XP Earned</h4>
            <div style="font-size: var(--fs-3xl); font-weight: 800; color: var(--accent-emerald); margin-top: 8px;">${user.xp} XP</div>
            <div class="text-muted" style="font-size: 11px;">Next Level at 4500 XP</div>
          </div>
        </div>
      </div>
    `;
  }
}

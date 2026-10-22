/* Professional Developer Profile Page Module */
import { store } from '../state/store.js';
import { AuthService } from '../services/AuthService.js';
import { ProjectService } from '../services/ProjectService.js';

export class ProfilePage {
  static async render({ params }) {
    const authUser = store.get('currentUser') || AuthService.getCurrentUser();
    const profile = authUser?.profile || {};
    const username = params?.username || authUser?.username || 'developer';
    const displayName = profile.displayName || authUser?.displayName || username;

    let userProjects = [];
    try {
      userProjects = await ProjectService.getProjects();
    } catch (e) {
      userProjects = [];
    }

    return `
      <div class="page-wrapper">
        <div class="card" style="margin-bottom: var(--space-4);">
          <div class="flex items-center gap-4">
            <div style="width: 56px; height: 56px; border-radius: 50%; background: var(--accent-primary); color: #fff; font-size: 22px; font-weight: 700; display: flex; align-items: center; justify-content: center; font-family: var(--font-mono);">
              ${(username[0] || 'D').toUpperCase()}
            </div>
            <div style="flex: 1;">
              <div class="flex items-center gap-2">
                <h2 style="font-size: var(--fs-lg); font-weight: 700; color: var(--text-primary);">${displayName}</h2>
                <span class="badge-tag badge-easy">${authUser?.role || 'DEVELOPER'}</span>
              </div>
              <p style="font-size: 12px; color: var(--text-muted); font-family: var(--font-mono); margin-top: 2px;">
                @${username} ${authUser?.email ? `• ${authUser.email}` : ''}
              </p>
              <p style="font-size: 12px; color: var(--text-secondary); margin-top: 6px;">
                ${profile.bio || 'Full-stack software engineer building on CodePilot cloud architecture.'}
              </p>
            </div>
            <div>
              <a href="#/settings" class="btn btn-secondary btn-sm">Edit Profile</a>
            </div>
          </div>
        </div>

        <div class="metrics-row">
          <div class="metric-card">
            <div class="metric-label">Contest Rating</div>
            <div class="metric-value">${profile.contestRating || 1200}</div>
            <div class="metric-delta">Rank: ${profile.rankTitle || 'Novice Developer'}</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Problems Solved</div>
            <div class="metric-value">${profile.problemsSolved || 0}</div>
            <div class="metric-delta">Verified Test Runs</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Workspaces</div>
            <div class="metric-value">${userProjects.length}</div>
            <div class="metric-delta">Active Projects</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Login Streak</div>
            <div class="metric-value">${profile.streakDays || 1} Days</div>
            <div class="metric-delta">Active</div>
          </div>
        </div>

        <!-- Recent Workspaces by User -->
        <div class="card">
          <div class="card-header">
            <span class="card-title">User Workspaces & Sandboxes</span>
            <a href="#/projects" class="btn btn-primary btn-sm">+ New Project</a>
          </div>

          ${userProjects.length > 0 ? `
            <div style="display: flex; flex-direction: column; gap: 8px;">
              ${userProjects.map(p => `
                <div style="background: var(--bg-darkest); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 10px 12px; display: flex; justify-content: space-between; align-items: center;">
                  <div>
                    <div class="flex items-center gap-2">
                      <span class="badge-tag badge-easy">${(p.primaryLanguage || 'PYTHON').toUpperCase()}</span>
                      <a href="#/ide?project=${p.id}" style="font-family: var(--font-mono); font-size: 13px; font-weight: 600; color: var(--text-primary); text-decoration: none;">${p.title}</a>
                    </div>
                    <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">
                      ${p.description || 'No description provided.'}
                    </div>
                  </div>
                  <a href="#/ide?project=${p.id}" class="btn btn-secondary btn-sm">Open Workspace</a>
                </div>
              `).join('')}
            </div>
          ` : `
            <div class="empty-state" style="padding: 24px;">
              <div class="empty-title">No projects yet</div>
              <div class="empty-text">Create your first workspace to start writing code.</div>
            </div>
          `}
        </div>
      </div>
    `;
  }
}

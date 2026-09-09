/* Project Workspace List Module */
import { mockProjects } from '../../mock-data/projects.js';

export class ProjectListPage {
  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Developer Projects Explorer</h1>
            <p class="text-secondary">GitHub-style multi-file commercial projects built in Python and JavaScript.</p>
          </div>
          <button id="btn-create-project" class="btn btn-primary">+ Create Project</button>
        </div>

        <div class="grid grid-cols-2 gap-6">
          ${mockProjects.map(p => `
            <div class="card">
              <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                <span class="badge-tag badge-easy">${p.language}</span>
                <span class="text-muted" style="font-size: var(--fs-xs);">Updated ${p.updatedAt}</span>
              </div>

              <h3 style="font-size: var(--fs-lg); margin-bottom: 8px;">${p.title}</h3>
              <p class="text-muted" style="font-size: var(--fs-sm); margin-bottom: 16px; line-height: 1.5;">${p.description}</p>

              <div class="flex items-center justify-between">
                <div class="flex items-center gap-4" style="font-size: var(--fs-xs); color: var(--text-secondary);">
                  <span>⭐ ${p.stars} stars</span>
                  <span>🍴 ${p.forks} forks</span>
                </div>
                <a href="#/ide" class="btn btn-secondary btn-sm">Open in IDE</a>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }
}

/**
 * CodePilot Projects Page Module
 * High-density developer project workspaces explorer with search, filtering,
 * 3-dot actions (open, rename, duplicate, export, delete), and new project modal flow.
 */

import { ProjectService } from '../../services/ProjectService.js';
import { NotificationService } from '../../services/NotificationService.js';
import { store } from '../../state/store.js';
import { AuthService } from '../../services/AuthService.js';

export class ProjectListPage {
  static currentProjects = [];
  static activeFilters = {
    search: '',
    language: 'all',
    type: 'all',
    sort: 'updated_desc'
  };

  static async render() {
    return `
      <div class="page-wrapper">
        <!-- Page Header -->
        <div class="page-header">
          <div>
            <h1 class="page-title">
              <span>Projects</span>
            </h1>
            <p class="page-description">Manage cloud workspaces, isolated runtimes, and multi-file developer sandboxes.</p>
          </div>
          <div class="flex items-center gap-2">
            <button id="btn-open-new-project-modal" class="btn btn-primary">
              <span>+</span> New Project
            </button>
          </div>
        </div>

        <!-- Filter & Search Toolbar -->
        <div class="projects-toolbar">
          <input 
            type="text" 
            id="projects-search-input" 
            class="projects-search-input" 
            placeholder="Search projects by name or description..." 
            value="${ProjectListPage.activeFilters.search || ''}"
          />

          <select id="projects-filter-lang" class="projects-filter-select">
            <option value="all">All Languages</option>
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="typescript">TypeScript</option>
            <option value="cpp">C++</option>
            <option value="c">C</option>
            <option value="java">Java</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
            <option value="csharp">C#</option>
            <option value="php">PHP</option>
            <option value="ruby">Ruby</option>
            <option value="kotlin">Kotlin</option>
          </select>

          <select id="projects-filter-type" class="projects-filter-select">
            <option value="all">All Types</option>
            <option value="cli">CLI Application</option>
            <option value="web">Web Application</option>
            <option value="rest_api">REST API</option>
            <option value="algorithm">Algorithm Workspace</option>
            <option value="data_science">Data Science</option>
            <option value="blank">Blank Project</option>
          </select>

          <select id="projects-filter-sort" class="projects-filter-select">
            <option value="updated_desc">Recently Updated</option>
            <option value="updated_asc">Oldest</option>
            <option value="name_asc">Name A-Z</option>
            <option value="name_desc">Name Z-A</option>
            <option value="files_desc">Most Files</option>
          </select>
        </div>

        <!-- Projects Grid Container -->
        <div id="projects-list-container">
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px;">
            <div class="skeleton-box" style="height: 140px; border-radius: var(--radius-sm);"></div>
            <div class="skeleton-box" style="height: 140px; border-radius: var(--radius-sm);"></div>
            <div class="skeleton-box" style="height: 140px; border-radius: var(--radius-sm);"></div>
          </div>
        </div>

        <!-- Modals Holder -->
        <div id="project-modals-holder"></div>
      </div>
    `;
  }

  static async afterRender() {
    await ProjectListPage.loadProjects();
    ProjectListPage.attachToolbarEvents();

    const createBtn = document.getElementById('btn-open-new-project-modal');
    if (createBtn) {
      createBtn.addEventListener('click', () => ProjectListPage.showCreateModal());
    }
  }

  static async loadProjects() {
    const container = document.getElementById('projects-list-container');
    if (!container) return;

    try {
      const projects = await ProjectService.getProjects();
      ProjectListPage.currentProjects = projects || [];
      ProjectListPage.renderFilteredProjects();
    } catch (err) {
      console.error('[ProjectListPage] Error loading projects:', err);
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon" style="color: var(--status-error);">⚠️</div>
          <div class="empty-title">Failed to load projects</div>
          <div class="empty-text">Could not connect to the CodePilot project service. Please check your backend connection.</div>
          <button id="btn-retry-load-projects" class="btn btn-secondary">Retry</button>
        </div>
      `;
      const retryBtn = document.getElementById('btn-retry-load-projects');
      if (retryBtn) retryBtn.addEventListener('click', () => ProjectListPage.loadProjects());
    }
  }

  static renderFilteredProjects() {
    const container = document.getElementById('projects-list-container');
    if (!container) return;

    let list = [...ProjectListPage.currentProjects];
    const { search, language, type, sort } = ProjectListPage.activeFilters;

    // Filter by search
    if (search && search.trim()) {
      const q = search.toLowerCase().trim();
      list = list.filter(p => 
        (p.title && p.title.toLowerCase().includes(q)) || 
        (p.description && p.description.toLowerCase().includes(q)) ||
        (p.primaryLanguage && p.primaryLanguage.toLowerCase().includes(q))
      );
    }

    // Filter by language
    if (language && language !== 'all') {
      list = list.filter(p => (p.primaryLanguage || '').toLowerCase() === language.toLowerCase());
    }

    // Filter by template/type
    if (type && type !== 'all') {
      list = list.filter(p => {
        const desc = (p.description || '').toLowerCase();
        const title = (p.title || '').toLowerCase();
        return desc.includes(type) || title.includes(type);
      });
    }

    // Sort
    list.sort((a, b) => {
      if (sort === 'updated_asc') {
        return new Date(a.updatedAt || 0) - new Date(b.updatedAt || 0);
      }
      if (sort === 'name_asc') {
        return (a.title || '').localeCompare(b.title || '');
      }
      if (sort === 'name_desc') {
        return (b.title || '').localeCompare(a.title || '');
      }
      if (sort === 'files_desc') {
        return (b.fileCount || 0) - (a.fileCount || 0);
      }
      // default: updated_desc
      return new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0);
    });

    // Check Empty State
    if (list.length === 0) {
      const hasFilter = search || (language !== 'all') || (type !== 'all');
      container.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">📁</div>
          <div class="empty-title">${hasFilter ? 'No matching projects found' : 'No projects yet'}</div>
          <div class="empty-text">
            ${hasFilter ? 'Try adjusting your search criteria or resetting filters.' : 'Create your first workspace and start building.'}
          </div>
          <button id="btn-empty-create-project" class="btn btn-primary">
            + Create Project
          </button>
        </div>
      `;

      const emptyBtn = document.getElementById('btn-empty-create-project');
      if (emptyBtn) {
        emptyBtn.addEventListener('click', () => ProjectListPage.showCreateModal());
      }
      return;
    }

    // Render Projects Grid
    container.innerHTML = `
      <div class="projects-grid">
        ${list.map(p => {
          const langDisplay = (p.primaryLanguage || 'python').toUpperCase();
          const fileCount = p.fileCount || 1;
          const sizeKb = p.totalSizeKb || (p.totalSizeBytes ? (p.totalSizeBytes / 1024).toFixed(1) : '0.5');
          const timeAgo = ProjectListPage.formatRelativeTime(p.updatedAt || p.createdAt);
          const owner = p.owner || 'You';

          return `
            <div class="project-card" data-project-id="${p.id}">
              <div>
                <div class="project-card-header">
                  <div class="flex items-center gap-2">
                    <span class="badge-tag badge-easy">${langDisplay}</span>
                    <a href="#/ide?project=${p.id}" class="project-title-link">${p.title}</a>
                  </div>

                  <div class="dropdown-holder">
                    <button class="btn btn-icon btn-secondary btn-sm project-menu-btn" data-project-id="${p.id}" title="Project Actions">
                      ⋮
                    </button>
                    <div id="project-menu-${p.id}" class="dropdown-menu">
                      <a href="#/ide?project=${p.id}" class="dropdown-item">▶ Open Project</a>
                      <button class="dropdown-item btn-action-rename" data-project-id="${p.id}" data-project-title="${p.title}" data-project-desc="${p.description || ''}">✏️ Rename</button>
                      <button class="dropdown-item btn-action-duplicate" data-project-id="${p.id}">📑 Duplicate</button>
                      <button class="dropdown-item btn-action-export" data-project-id="${p.id}">📦 Export JSON</button>
                      <div class="dropdown-divider"></div>
                      <button class="dropdown-item danger btn-action-delete" data-project-id="${p.id}" data-project-title="${p.title}">🗑️ Delete</button>
                    </div>
                  </div>
                </div>

                <p class="project-desc">${p.description || 'No description provided.'}</p>
              </div>

              <div>
                <div class="project-meta-row">
                  <span>📄 ${fileCount} ${fileCount === 1 ? 'file' : 'files'}</span>
                  <span>💾 ${sizeKb} KB</span>
                  <span>🕒 Updated ${timeAgo}</span>
                </div>

                <div class="project-card-footer">
                  <div class="flex items-center gap-2">
                    <span style="font-size: 11px; color: var(--text-muted);">Owner: <strong style="color: var(--text-secondary);">${owner}</strong></span>
                  </div>
                  <a href="#/ide?project=${p.id}" class="btn btn-secondary btn-sm">Open Workspace</a>
                </div>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;

    ProjectListPage.attachProjectCardEvents();
  }

  static attachToolbarEvents() {
    const searchInput = document.getElementById('projects-search-input');
    const langSelect = document.getElementById('projects-filter-lang');
    const typeSelect = document.getElementById('projects-filter-type');
    const sortSelect = document.getElementById('projects-filter-sort');

    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        ProjectListPage.activeFilters.search = e.target.value;
        ProjectListPage.renderFilteredProjects();
      });
    }

    if (langSelect) {
      langSelect.value = ProjectListPage.activeFilters.language;
      langSelect.addEventListener('change', (e) => {
        ProjectListPage.activeFilters.language = e.target.value;
        ProjectListPage.renderFilteredProjects();
      });
    }

    if (typeSelect) {
      typeSelect.value = ProjectListPage.activeFilters.type;
      typeSelect.addEventListener('change', (e) => {
        ProjectListPage.activeFilters.type = e.target.value;
        ProjectListPage.renderFilteredProjects();
      });
    }

    if (sortSelect) {
      sortSelect.value = ProjectListPage.activeFilters.sort;
      sortSelect.addEventListener('change', (e) => {
        ProjectListPage.activeFilters.sort = e.target.value;
        ProjectListPage.renderFilteredProjects();
      });
    }
  }

  static attachProjectCardEvents() {
    // 3-dot dropdown triggers
    document.querySelectorAll('.project-menu-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const pid = btn.getAttribute('data-project-id');
        // Close all other dropdowns
        document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('show'));
        const menu = document.getElementById(`project-menu-${pid}`);
        if (menu) menu.classList.toggle('show');
      });
    });

    document.addEventListener('click', () => {
      document.querySelectorAll('.dropdown-menu').forEach(m => m.classList.remove('show'));
    });

    // Rename buttons
    document.querySelectorAll('.btn-action-rename').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const pid = btn.getAttribute('data-project-id');
        const title = btn.getAttribute('data-project-title');
        const desc = btn.getAttribute('data-project-desc');
        ProjectListPage.showRenameModal(pid, title, desc);
      });
    });

    // Duplicate buttons
    document.querySelectorAll('.btn-action-duplicate').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.stopPropagation();
        const pid = btn.getAttribute('data-project-id');
        try {
          NotificationService.info('Duplicating workspace...');
          await ProjectService.duplicateProject(pid);
          NotificationService.success('Project duplicated successfully.');
          await ProjectListPage.loadProjects();
        } catch (err) {
          NotificationService.error(err.message || 'Failed to duplicate project.');
        }
      });
    });

    // Export buttons
    document.querySelectorAll('.btn-action-export').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        e.stopPropagation();
        const pid = btn.getAttribute('data-project-id');
        try {
          const data = await ProjectService.exportProject(pid);
          const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `${data.project.title.toLowerCase().replace(/[^a-z0-9_-]/g, '-')}-workspace.json`;
          a.click();
          URL.revokeObjectURL(url);
          NotificationService.success('Project workspace exported as JSON.');
        } catch (err) {
          NotificationService.error('Failed to export project.');
        }
      });
    });

    // Delete buttons
    document.querySelectorAll('.btn-action-delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const pid = btn.getAttribute('data-project-id');
        const title = btn.getAttribute('data-project-title');
        ProjectListPage.showDeleteModal(pid, title);
      });
    });
  }

  // ==========================================
  // Modals Implementation
  // ==========================================

  static showCreateModal() {
    const holder = document.getElementById('project-modals-holder');
    if (!holder) return;

    holder.innerHTML = `
      <div class="modal-backdrop" id="create-modal-backdrop">
        <div class="modal-dialog">
          <div class="modal-header">
            <h3 class="modal-title">Create a new project</h3>
            <button id="btn-close-create-modal" class="btn btn-icon btn-outline btn-sm">✕</button>
          </div>

          <form id="form-create-project">
            <div class="modal-body">
              <div class="form-group">
                <label class="form-label">Project Name *</label>
                <input 
                  type="text" 
                  id="input-project-name" 
                  class="form-input" 
                  placeholder="e.g. distributed-rate-limiter" 
                  required 
                  autofocus
                />
                <span style="font-size: 11px; color: var(--text-muted);">Use alphanumeric characters, dashes, or underscores.</span>
              </div>

              <div class="form-group">
                <label class="form-label">Description (Optional)</label>
                <textarea 
                  id="input-project-desc" 
                  class="form-textarea" 
                  rows="2" 
                  placeholder="Brief summary of your project goals..."
                ></textarea>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div class="form-group">
                  <label class="form-label">Language *</label>
                  <select id="select-project-lang" class="form-select" required>
                    <option value="python">Python</option>
                    <option value="javascript">JavaScript</option>
                    <option value="typescript">TypeScript</option>
                    <option value="cpp">C++</option>
                    <option value="c">C</option>
                    <option value="java">Java</option>
                    <option value="go">Go</option>
                    <option value="rust">Rust</option>
                    <option value="csharp">C#</option>
                    <option value="php">PHP</option>
                    <option value="ruby">Ruby</option>
                    <option value="kotlin">Kotlin</option>
                  </select>
                </div>

                <div class="form-group">
                  <label class="form-label">Template *</label>
                  <select id="select-project-template" class="form-select" required>
                    <option value="cli">CLI Application</option>
                    <option value="blank">Blank Project</option>
                    <option value="web">Web Application</option>
                    <option value="rest_api">REST API</option>
                    <option value="algorithm">Algorithm Workspace</option>
                    <option value="data_science">Data Science</option>
                    <option value="learning">Learning Project</option>
                  </select>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" id="btn-cancel-create" class="btn btn-secondary">Cancel</button>
              <button type="submit" id="btn-submit-create" class="btn btn-primary">Create Project</button>
            </div>
          </form>
        </div>
      </div>
    `;

    const close = () => { holder.innerHTML = ''; };
    document.getElementById('btn-close-create-modal')?.addEventListener('click', close);
    document.getElementById('btn-cancel-create')?.addEventListener('click', close);

    const form = document.getElementById('form-create-project');
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('input-project-name').value.trim();
        const description = document.getElementById('input-project-desc').value.trim();
        const language = document.getElementById('select-project-lang').value;
        const template = document.getElementById('select-project-template').value;

        if (!title) {
          NotificationService.warning('Please enter a project name.');
          return;
        }

        const submitBtn = document.getElementById('btn-submit-create');
        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = 'Scaffolding Workspace...';
        }

        try {
          const newProj = await ProjectService.createProject({ title, description, language, template });
          NotificationService.success(`Project '${title}' created successfully.`);
          close();
          // Redirect directly to IDE with the new project
          window.location.hash = `#/ide?project=${newProj.id}`;
        } catch (err) {
          NotificationService.error(err.message || 'Failed to create project.');
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Project';
          }
        }
      });
    }
  }

  static showRenameModal(projectId, currentTitle, currentDesc) {
    const holder = document.getElementById('project-modals-holder');
    if (!holder) return;

    holder.innerHTML = `
      <div class="modal-backdrop">
        <div class="modal-dialog">
          <div class="modal-header">
            <h3 class="modal-title">Rename Project</h3>
            <button id="btn-close-rename-modal" class="btn btn-icon btn-outline btn-sm">✕</button>
          </div>

          <form id="form-rename-project">
            <div class="modal-body">
              <div class="form-group">
                <label class="form-label">Project Name *</label>
                <input type="text" id="input-rename-name" class="form-input" value="${currentTitle}" required />
              </div>

              <div class="form-group">
                <label class="form-label">Description</label>
                <textarea id="input-rename-desc" class="form-textarea" rows="2">${currentDesc}</textarea>
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" id="btn-cancel-rename" class="btn btn-secondary">Cancel</button>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    `;

    const close = () => { holder.innerHTML = ''; };
    document.getElementById('btn-close-rename-modal')?.addEventListener('click', close);
    document.getElementById('btn-cancel-rename')?.addEventListener('click', close);

    const form = document.getElementById('form-rename-project');
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('input-rename-name').value.trim();
        const description = document.getElementById('input-rename-desc').value.trim();

        try {
          await ProjectService.renameProject(projectId, { title, description });
          NotificationService.success('Project renamed.');
          close();
          await ProjectListPage.loadProjects();
        } catch (err) {
          NotificationService.error(err.message || 'Failed to rename project.');
        }
      });
    }
  }

  static showDeleteModal(projectId, projectTitle) {
    const holder = document.getElementById('project-modals-holder');
    if (!holder) return;

    holder.innerHTML = `
      <div class="modal-backdrop">
        <div class="modal-dialog">
          <div class="modal-header">
            <h3 class="modal-title" style="color: var(--status-error);">Delete Project</h3>
            <button id="btn-close-delete-modal" class="btn btn-icon btn-outline btn-sm">✕</button>
          </div>

          <div class="modal-body">
            <p style="font-size: var(--fs-sm); color: var(--text-primary); margin-bottom: 8px;">
              Are you sure you want to permanently delete <strong>${projectTitle}</strong>?
            </p>
            <p style="font-size: var(--fs-xs); color: var(--text-muted); line-height: 1.5;">
              This action cannot be undone. All files, execution logs, and workspace configuration will be deleted.
            </p>
          </div>

          <div class="modal-footer">
            <button type="button" id="btn-cancel-delete" class="btn btn-secondary">Cancel</button>
            <button type="button" id="btn-confirm-delete" class="btn btn-danger">Delete Project</button>
          </div>
        </div>
      </div>
    `;

    const close = () => { holder.innerHTML = ''; };
    document.getElementById('btn-close-delete-modal')?.addEventListener('click', close);
    document.getElementById('btn-cancel-delete')?.addEventListener('click', close);

    const confirmBtn = document.getElementById('btn-confirm-delete');
    if (confirmBtn) {
      confirmBtn.addEventListener('click', async () => {
        try {
          await ProjectService.deleteProject(projectId);
          NotificationService.success(`Deleted project '${projectTitle}'.`);
          close();
          await ProjectListPage.loadProjects();
        } catch (err) {
          NotificationService.error(err.message || 'Failed to delete project.');
        }
      });
    }
  }

  static formatRelativeTime(dateStr) {
    if (!dateStr) return 'recently';
    const date = new Date(dateStr.endsWith('Z') ? dateStr : `${dateStr}Z`);
    const now = new Date();
    const diffSecs = Math.max(0, Math.floor((now - date) / 1000));

    if (diffSecs < 60) return 'just now';
    if (diffSecs < 3600) return `${Math.floor(diffSecs / 60)} minutes ago`;
    if (diffSecs < 86400) {
      const hrs = Math.floor(diffSecs / 3600);
      return hrs === 1 ? '1 hour ago' : `${hrs} hours ago`;
    }
    const days = Math.floor(diffSecs / 86400);
    if (days === 1) return 'yesterday';
    if (days < 30) return `${days} days ago`;
    return date.toLocaleDateString();
  }
}

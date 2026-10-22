/* Persistent Developer Activity History Page */
import { AuthService } from '../services/AuthService.js';
import { NotificationService } from '../services/NotificationService.js';

export class HistoryPage {
  static currentPage = 1;
  static pageSize = 25;
  static activities = [];

  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1 class="page-title">Activity History</h1>
            <p class="page-description">Chronological execution audit trail, judge submissions, and project events.</p>
          </div>
          <button id="history-refresh-btn" class="btn btn-secondary btn-sm">🔄 Refresh Activity</button>
        </div>

        <!-- Filter Bar -->
        <div class="projects-toolbar">
          <input type="text" id="history-search-input" class="projects-search-input" placeholder="Search activity title, problem, or file..." />
          
          <select id="history-type-filter" class="projects-filter-select">
            <option value="">All Types</option>
            <option value="EXECUTION">Executions</option>
            <option value="SUBMISSION">Submissions</option>
            <option value="PROJECT">Projects</option>
            <option value="AI_REVIEW">Pilot AI</option>
            <option value="COURSE">Courses</option>
          </select>

          <select id="history-lang-filter" class="projects-filter-select">
            <option value="">All Languages</option>
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="typescript">TypeScript</option>
            <option value="cpp">C++</option>
            <option value="c">C</option>
            <option value="java">Java</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
          </select>

          <select id="history-status-filter" class="projects-filter-select">
            <option value="">All Statuses</option>
            <option value="ACCEPTED">Accepted / Success</option>
            <option value="Wrong Answer">Wrong Answer</option>
            <option value="COMPILE_ERROR">Compilation Error</option>
            <option value="RUNTIME_ERROR">Runtime Error</option>
            <option value="TIME_LIMIT_EXCEEDED">Time Limit Exceeded</option>
          </select>
        </div>

        <!-- Grouped Activity Feed -->
        <div id="history-feed-container">
          <div style="padding: 24px; text-align: center; color: var(--text-muted);">
            Loading activity history...
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex justify-between items-center" style="margin-top: 16px; font-size: var(--fs-xs); color: var(--text-secondary);">
          <span id="history-page-info">Showing page 1</span>
          <div class="flex gap-2">
            <button id="history-prev-btn" class="btn btn-secondary btn-sm" disabled>← Previous</button>
            <button id="history-next-btn" class="btn btn-secondary btn-sm" disabled>Next →</button>
          </div>
        </div>

        <!-- Activity Inspect Modal Holder -->
        <div id="history-modal-holder"></div>
      </div>
    `;
  }

  static async afterRender() {
    await HistoryPage.loadData();
    HistoryPage.attachEvents();
  }

  static async loadData() {
    const search = document.getElementById('history-search-input')?.value || '';
    const actType = document.getElementById('history-type-filter')?.value || '';
    const lang = document.getElementById('history-lang-filter')?.value || '';
    const status = document.getElementById('history-status-filter')?.value || '';

    const feed = document.getElementById('history-feed-container');
    if (!feed) return;

    const data = await AuthService.fetchHistory({
      page: HistoryPage.currentPage,
      pageSize: HistoryPage.pageSize,
      activityType: actType,
      language: lang,
      status: status,
      search: search
    });

    const activities = data.activities || data.items || [];
    HistoryPage.activities = activities;
    const total = data.total || activities.length;

    if (activities.length === 0) {
      feed.innerHTML = `
        <div class="empty-state">
          <div class="empty-icon">📜</div>
          <div class="empty-title">No activity records found</div>
          <div class="empty-text">Run code in the Cloud IDE or submit a problem solution to generate activity logs.</div>
          <a href="#/ide" class="btn btn-primary btn-sm">▶ Open Cloud IDE</a>
        </div>
      `;
      return;
    }

    // Group activities by date category (TODAY, YESTERDAY, THIS WEEK, OLDER)
    const groups = {
      'TODAY': [],
      'YESTERDAY': [],
      'THIS WEEK': [],
      'OLDER': []
    };

    const now = new Date();
    const todayStr = now.toDateString();
    const yesterday = new Date(now);
    yesterday.setDate(now.getDate() - 1);
    const yesterdayStr = yesterday.toDateString();
    const weekAgo = new Date(now.getTime() - 7 * 24 * 3600 * 1000);

    activities.forEach(act => {
      const actDate = act.createdAt ? new Date(act.createdAt.endsWith('Z') ? act.createdAt : `${act.createdAt}Z`) : now;
      const actDateStr = actDate.toDateString();

      if (actDateStr === todayStr) {
        groups['TODAY'].push(act);
      } else if (actDateStr === yesterdayStr) {
        groups['YESTERDAY'].push(act);
      } else if (actDate > weekAgo) {
        groups['THIS WEEK'].push(act);
      } else {
        groups['OLDER'].push(act);
      }
    });

    let html = '';
    for (const [groupName, items] of Object.entries(groups)) {
      if (items.length === 0) continue;

      html += `
        <div class="history-date-group">
          <div class="history-date-heading">${groupName}</div>
          <div style="display: flex; flex-direction: column; gap: 4px;">
            ${items.map(act => {
              const actDate = act.createdAt ? new Date(act.createdAt.endsWith('Z') ? act.createdAt : `${act.createdAt}Z`) : now;
              const timeStr = actDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
              const isAccepted = act.status === 'ACCEPTED' || act.status === 'Accepted' || act.status === 'SUCCESS';
              const langStr = act.language ? act.language.toUpperCase() : 'PYTHON';

              return `
                <div class="history-item" data-activity-id="${act.id}">
                  <div class="history-meta">
                    <span class="history-time">${timeStr}</span>
                    <span class="history-lang-badge">${langStr}</span>
                    <div>
                      <span style="font-weight: 600; color: var(--text-primary); font-family: var(--font-mono); font-size: 13px;">${act.title || 'Code Execution'}</span>
                      ${act.description ? `<span style="font-size: 11px; color: var(--text-muted); margin-left: 8px;">${act.description}</span>` : ''}
                    </div>
                  </div>

                  <div class="flex items-center gap-3">
                    ${act.status ? `
                      <span class="badge-tag ${isAccepted ? 'badge-easy' : 'badge-hard'}">
                        ${act.status}
                      </span>
                    ` : ''}
                    <button class="btn btn-secondary btn-sm btn-inspect-activity" data-activity-id="${act.id}" style="font-size: 11px; padding: 2px 8px;">Inspect</button>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }

    feed.innerHTML = html;

    // Pagination info
    const pageInfo = document.getElementById('history-page-info');
    if (pageInfo) {
      pageInfo.textContent = `Showing ${(HistoryPage.currentPage - 1) * HistoryPage.pageSize + 1} - ${Math.min(HistoryPage.currentPage * HistoryPage.pageSize, total)} of ${total} entries`;
    }

    const prevBtn = document.getElementById('history-prev-btn');
    const nextBtn = document.getElementById('history-next-btn');
    if (prevBtn) prevBtn.disabled = HistoryPage.currentPage <= 1;
    if (nextBtn) nextBtn.disabled = HistoryPage.currentPage * HistoryPage.pageSize >= total;

    // Attach inspect buttons
    document.querySelectorAll('.btn-inspect-activity').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const actId = parseInt(btn.getAttribute('data-activity-id'), 10);
        const act = HistoryPage.activities.find(a => a.id === actId);
        if (act) HistoryPage.showInspectModal(act);
      });
    });

    document.querySelectorAll('.history-item').forEach(item => {
      item.addEventListener('click', () => {
        const actId = parseInt(item.getAttribute('data-activity-id'), 10);
        const act = HistoryPage.activities.find(a => a.id === actId);
        if (act) HistoryPage.showInspectModal(act);
      });
    });
  }

  static attachEvents() {
    ['history-search-input', 'history-type-filter', 'history-lang-filter', 'history-status-filter'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', () => {
          HistoryPage.currentPage = 1;
          HistoryPage.loadData();
        });
        el.addEventListener('change', () => {
          HistoryPage.currentPage = 1;
          HistoryPage.loadData();
        });
      }
    });

    document.getElementById('history-refresh-btn')?.addEventListener('click', () => {
      HistoryPage.loadData();
      NotificationService.info('Activity history refreshed.');
    });

    document.getElementById('history-prev-btn')?.addEventListener('click', () => {
      if (HistoryPage.currentPage > 1) {
        HistoryPage.currentPage--;
        HistoryPage.loadData();
      }
    });

    document.getElementById('history-next-btn')?.addEventListener('click', () => {
      HistoryPage.currentPage++;
      HistoryPage.loadData();
    });
  }

  static showInspectModal(act) {
    const holder = document.getElementById('history-modal-holder');
    if (!holder) return;

    let details = {};
    if (act.detailsJson) {
      try { details = JSON.parse(act.detailsJson); } catch (e) {}
    }

    holder.innerHTML = `
      <div class="modal-backdrop">
        <div class="modal-dialog" style="max-width: 640px;">
          <div class="modal-header">
            <div class="flex items-center gap-2">
              <span class="badge-tag badge-easy">${(act.language || 'PYTHON').toUpperCase()}</span>
              <h3 class="modal-title" style="font-family: var(--font-mono);">${act.title}</h3>
            </div>
            <button id="btn-close-inspect-modal" class="btn btn-icon btn-outline btn-sm">✕</button>
          </div>

          <div class="modal-body" style="font-size: 12px;">
            <div class="grid grid-cols-2 gap-3" style="background: var(--bg-darkest); padding: 10px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); margin-bottom: 12px;">
              <div><strong>Status:</strong> <span style="color: var(--status-success);">${act.status || 'SUCCESS'}</span></div>
              <div><strong>Activity Type:</strong> ${act.activityType || 'EXECUTION'}</div>
              <div><strong>Execution Time:</strong> ${details.executionTimeMs || details.runtimeSeconds || '24'} ms</div>
              <div><strong>Memory Used:</strong> ${details.memoryMb || '12'} MB</div>
              <div style="grid-column: span 2;"><strong>Timestamp:</strong> ${act.createdAt || new Date().toISOString()}</div>
            </div>

            ${details.sourceCode ? `
              <div style="margin-bottom: 10px;">
                <label class="form-label">Source Code</label>
                <pre style="background: var(--bg-darkest); border: 1px solid var(--border-subtle); padding: 10px; border-radius: var(--radius-sm); font-family: var(--font-mono); font-size: 11px; max-height: 180px; overflow-y: auto;">${details.sourceCode}</pre>
              </div>
            ` : ''}

            ${details.stdin ? `
              <div style="margin-bottom: 10px;">
                <label class="form-label">Stdin Input</label>
                <pre style="background: var(--bg-darkest); border: 1px solid var(--border-subtle); padding: 8px; border-radius: var(--radius-sm); font-family: var(--font-mono); font-size: 11px;">${details.stdin}</pre>
              </div>
            ` : ''}

            <div>
              <label class="form-label">Output / Result</label>
              <pre style="background: var(--bg-darkest); border: 1px solid var(--border-subtle); padding: 10px; border-radius: var(--radius-sm); font-family: var(--font-mono); font-size: 11px; color: var(--accent-emerald); max-height: 140px; overflow-y: auto;">${details.stdout || details.output || act.description || 'Execution completed with return code 0.'}</pre>
            </div>
          </div>

          <div class="modal-footer">
            <a href="#/ide?lang=${(act.language || 'python').toLowerCase()}" class="btn btn-primary btn-sm">Open in IDE</a>
            <button id="btn-cancel-inspect" class="btn btn-secondary btn-sm">Close</button>
          </div>
        </div>
      </div>
    `;

    const close = () => { holder.innerHTML = ''; };
    document.getElementById('btn-close-inspect-modal')?.addEventListener('click', close);
    document.getElementById('btn-cancel-inspect')?.addEventListener('click', close);
  }
}

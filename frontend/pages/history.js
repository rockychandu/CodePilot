/* Persistent Developer Activity History Page */
import { AuthService } from '../services/AuthService.js';
import { NotificationService } from '../services/NotificationService.js';

export class HistoryPage {
  static currentPage = 1;
  static pageSize = 20;

  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1 class="page-title">Developer Activity Timeline</h1>
            <p class="page-description">Persistent audit trail of code executions, submissions, AI reviews, and course milestones.</p>
          </div>
          <button id="history-refresh-btn" class="btn btn-secondary btn-sm">🔄 Refresh Activity</button>
        </div>

        <!-- Filter Bar -->
        <div class="filter-bar">
          <input type="text" id="history-search-input" class="filter-search-input" placeholder="Search activity description, problem name..." />
          
          <select id="history-type-filter" class="filter-select">
            <option value="">All Activity Types</option>
            <option value="EXECUTION">Code Executions</option>
            <option value="SUBMISSION">Submissions</option>
            <option value="AI_REVIEW">Pilot AI Reviews</option>
            <option value="COURSE">Course Lessons</option>
            <option value="PROJECT">Projects</option>
          </select>

          <select id="history-lang-filter" class="filter-select">
            <option value="">All Languages</option>
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="cpp">C++</option>
            <option value="c">C</option>
            <option value="java">Java</option>
            <option value="go">Go</option>
            <option value="rust">Rust</option>
          </select>

          <select id="history-status-filter" class="filter-select">
            <option value="">All Statuses</option>
            <option value="ACCEPTED">Accepted / Passed</option>
            <option value="Wrong Answer">Wrong Answer</option>
            <option value="COMPILE_ERROR">Compilation Error</option>
            <option value="RUNTIME_ERROR">Runtime Error</option>
            <option value="TIME_LIMIT_EXCEEDED">Time Limit Exceeded</option>
          </select>
        </div>

        <!-- History Table -->
        <div class="table-container" style="margin-bottom: var(--space-4);">
          <table class="data-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Activity Event</th>
                <th>Type</th>
                <th>Language</th>
                <th>Status / Result</th>
                <th style="text-align: right;">Action</th>
              </tr>
            </thead>
            <tbody id="history-table-body">
              <tr>
                <td colspan="6" style="text-align: center; padding: var(--space-6); color: var(--text-muted);">
                  Loading activity timeline...
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex justify-between items-center" style="font-size: var(--fs-xs); color: var(--text-secondary);">
          <span id="history-page-info">Showing page 1</span>
          <div class="flex gap-2">
            <button id="history-prev-btn" class="btn btn-secondary btn-sm" disabled>← Previous</button>
            <button id="history-next-btn" class="btn btn-secondary btn-sm" disabled>Next →</button>
          </div>
        </div>
      </div>
    `;
  }

  static async afterRender() {
    const loadData = async () => {
      const search = document.getElementById('history-search-input')?.value || '';
      const actType = document.getElementById('history-type-filter')?.value || '';
      const lang = document.getElementById('history-lang-filter')?.value || '';
      const status = document.getElementById('history-status-filter')?.value || '';

      const tbody = document.getElementById('history-table-body');
      if (!tbody) return;

      const data = await AuthService.fetchHistory({
        page: HistoryPage.currentPage,
        pageSize: HistoryPage.pageSize,
        activityType: actType,
        language: lang,
        status: status,
        search: search
      });

      const activities = data.activities || data.items || [];
      const total = data.total || activities.length;

      if (activities.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="6" style="text-align: center; padding: var(--space-8); color: var(--text-muted);">
              No activity records found matching filters.
            </td>
          </tr>
        `;
      } else {
        tbody.innerHTML = activities.map(act => {
          const dateStr = act.createdAt ? new Date(act.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Today';
          const isAccepted = act.status === 'ACCEPTED' || act.status === 'Accepted' || act.status === 'SUCCESS';

          return `
            <tr>
              <td style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">${dateStr}</td>
              <td>
                <div style="font-weight: 500; color: var(--text-primary);">${act.title || 'Code Execution'}</div>
                <div style="font-size: 11px; color: var(--text-muted);">${act.description || ''}</div>
              </td>
              <td>
                <span class="badge-tag" style="background: var(--bg-darkest);">${act.activityType || 'EXEC'}</span>
              </td>
              <td>
                ${act.language ? `<span class="history-lang-badge">${act.language.toUpperCase()}</span>` : '<span style="color: var(--text-disabled);">-</span>'}
              </td>
              <td>
                ${act.status ? `
                  <span class="output-status-pill ${isAccepted ? 'status-accepted' : 'status-error'}">
                    ${act.status}
                  </span>
                ` : '<span style="color: var(--text-disabled);">-</span>'}
              </td>
              <td style="text-align: right;">
                <a href="#/ide?lang=${(act.language || 'python').toLowerCase()}" class="btn btn-secondary btn-sm" style="font-size: 11px; padding: 2px 6px;">Open IDE</a>
              </td>
            </tr>
          `;
        }).join('');
      }

      const pageInfo = document.getElementById('history-page-info');
      if (pageInfo) {
        pageInfo.textContent = `Showing ${(HistoryPage.currentPage - 1) * HistoryPage.pageSize + 1} - ${Math.min(HistoryPage.currentPage * HistoryPage.pageSize, total)} of ${total} entries`;
      }

      const prevBtn = document.getElementById('history-prev-btn');
      const nextBtn = document.getElementById('history-next-btn');
      if (prevBtn) prevBtn.disabled = HistoryPage.currentPage <= 1;
      if (nextBtn) nextBtn.disabled = HistoryPage.currentPage * HistoryPage.pageSize >= total;
    };

    // Attach filter listeners
    ['history-search-input', 'history-type-filter', 'history-lang-filter', 'history-status-filter'].forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener('input', () => {
          HistoryPage.currentPage = 1;
          loadData();
        });
        el.addEventListener('change', () => {
          HistoryPage.currentPage = 1;
          loadData();
        });
      }
    });

    const refreshBtn = document.getElementById('history-refresh-btn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => {
        loadData();
        NotificationService.showToast('Activity timeline refreshed', 'info');
      });
    }

    const prevBtn = document.getElementById('history-prev-btn');
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        if (HistoryPage.currentPage > 1) {
          HistoryPage.currentPage--;
          loadData();
        }
      });
    }

    const nextBtn = document.getElementById('history-next-btn');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        HistoryPage.currentPage++;
        loadData();
      });
    }

    loadData();
  }
}

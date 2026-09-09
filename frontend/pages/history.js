/**
 * CodePilot Persistent User History Page Component
 * Displays filtered, paginated user activity records (executions, submissions, AI reviews, logins)
 */

export function renderHistoryPage() {
  return `
    <div class="container" style="padding: 2.5rem 1.5rem; max-width: 1200px; margin: 0 auto;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem;">
        <div>
          <h1 style="font-size: 2rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.5rem;">
            📜 Persistent User History
          </h1>
          <p style="color: var(--text-secondary); font-size: 0.95rem;">
            Chronological audit trail of your code executions, contest submissions, AI reviews, and learning progression.
          </p>
        </div>
        <button class="btn btn-secondary" id="history-refresh-btn" style="display: flex; align-items: center; gap: 0.5rem;">
          🔄 Refresh Activity
        </button>
      </div>

      <!-- Filter Controls Bar -->
      <div class="card" style="padding: 1.25rem; margin-bottom: 1.5rem; display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; background: var(--surface-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
        <div style="flex: 1; min-width: 200px;">
          <input type="text" id="history-search-input" class="input" placeholder="Search activity title, details..." style="width: 100%; padding: 0.6rem 1rem; background: var(--surface-primary); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: var(--radius-sm);" />
        </div>
        <select id="history-type-filter" class="select" style="padding: 0.6rem 1rem; background: var(--surface-primary); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
          <option value="">All Activity Types</option>
          <option value="EXECUTION">Code Executions</option>
          <option value="SUBMISSION">Problem Submissions</option>
          <option value="AI_REVIEW">Pilot AI Reviews</option>
          <option value="COURSE">Course Lessons</option>
          <option value="LOGIN">Account Logins</option>
        </select>
        <select id="history-lang-filter" class="select" style="padding: 0.6rem 1rem; background: var(--surface-primary); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
          <option value="">All Languages</option>
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="cpp">C++</option>
          <option value="c">C</option>
          <option value="java">Java</option>
          <option value="go">Go</option>
          <option value="rust">Rust</option>
        </select>
        <select id="history-status-filter" class="select" style="padding: 0.6rem 1rem; background: var(--surface-primary); color: var(--text-primary); border: 1px solid var(--border-color); border-radius: var(--radius-sm);">
          <option value="">All Statuses</option>
          <option value="ACCEPTED">Accepted / Passed</option>
          <option value="Wrong Answer">Wrong Answer</option>
          <option value="COMPILE_ERROR">Compilation Error</option>
          <option value="RUNTIME_ERROR">Runtime Error</option>
          <option value="TIME_LIMIT_EXCEEDED">Time Limit Exceeded</option>
        </select>
      </div>

      <!-- History Table Container -->
      <div class="card" style="overflow-x: auto; background: var(--surface-primary); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
          <thead>
            <tr style="border-bottom: 1px solid var(--border-color); background: var(--surface-secondary); color: var(--text-secondary); text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em;">
              <th style="padding: 1rem 1.25rem;">Event / Title</th>
              <th style="padding: 1rem 1.25rem;">Type</th>
              <th style="padding: 1rem 1.25rem;">Language</th>
              <th style="padding: 1rem 1.25rem;">Verdict / Status</th>
              <th style="padding: 1rem 1.25rem;">Timestamp</th>
              <th style="padding: 1rem 1.25rem; text-align: right;">Action</th>
            </tr>
          </thead>
          <tbody id="history-table-body">
            <tr>
              <td colspan="6" style="padding: 3rem; text-align: center; color: var(--text-tertiary);">
                Loading persistent activity records...
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination Container -->
      <div id="history-pagination" style="display: flex; justify-content: space-between; align-items: center; margin-top: 1.5rem; color: var(--text-secondary); font-size: 0.9rem;">
        <span id="history-page-info">Showing 0 of 0 entries</span>
        <div style="display: flex; gap: 0.5rem;">
          <button class="btn btn-secondary btn-sm" id="history-prev-btn" disabled>← Previous</button>
          <button class="btn btn-secondary btn-sm" id="history-next-btn" disabled>Next →</button>
        </div>
      </div>
    </div>
  `;
}

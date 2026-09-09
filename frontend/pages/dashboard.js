/* Professional Developer-First Dashboard Page Module */
import { store } from '../state/store.js';
import { AuthService } from '../services/AuthService.js';
import { ProblemService } from '../services/ProblemService.js';
import { mockAnalytics } from '../mock-data/analytics.js';

export class DashboardPage {
  static async render() {
    const user = store.get('currentUser') || AuthService.getCurrentUser();
    const displayName = user?.profile?.displayName || user?.username || 'Developer';
    const problems = await ProblemService.getAll();
    const topProblems = (problems || []).slice(0, 4);

    return `
      <div class="page-wrapper">
        <!-- Dashboard Header -->
        <div class="page-header">
          <div>
            <h1 class="page-title">
              <span>Developer Workspace</span>
            </h1>
            <p class="page-description">Signed in as <strong>${displayName}</strong> (${user?.role || 'USER'}) | Local Workspace Connected</p>
          </div>
          <div class="flex items-center gap-2">
            <a href="#/ide" class="btn btn-primary">▶ Open Cloud IDE</a>
            <a href="#/history" class="btn btn-secondary">📜 Activity Log</a>
          </div>
        </div>

        <!-- 4 Key Developer Metrics -->
        <div class="metrics-row">
          <div class="metric-card">
            <div class="metric-label">Problems Solved</div>
            <div class="metric-value">${user?.profile?.problemsSolved || 14}</div>
            <div class="metric-delta">Rank: ${user?.profile?.rankTitle || 'Novice Developer'}</div>
          </div>

          <div class="metric-card">
            <div class="metric-label">Contest Rating</div>
            <div class="metric-value">${user?.profile?.contestRating || 1200}</div>
            <div class="metric-delta">Division II Active</div>
          </div>

          <div class="metric-card">
            <div class="metric-label">Developer XP</div>
            <div class="metric-value">${user?.profile?.xp || 350}</div>
            <div class="metric-delta">Level ${user?.profile?.level || 1} Engineer</div>
          </div>

          <div class="metric-card">
            <div class="metric-label">Daily Streak</div>
            <div class="metric-value">${user?.profile?.streakDays || 3} Days</div>
            <div class="metric-delta">Active Today</div>
          </div>
        </div>

        <!-- 2-Column Main Developer Dashboard Layout -->
        <div class="dashboard-grid">
          <!-- Left Main Column: Continue Coding & Activity Matrix -->
          <div class="flex flex-col gap-4">
            <!-- Continue Coding Card -->
            <div class="card">
              <div class="card-header">
                <span class="card-title">Recent Work & Continue Coding</span>
                <span style="font-size: 11px; color: var(--text-muted);">Auto-Saved</span>
              </div>
              <div style="background: var(--bg-darkest); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: var(--space-3); margin-bottom: var(--space-3);">
                <div class="flex justify-between items-center" style="margin-bottom: var(--space-1);">
                  <div class="flex items-center gap-2">
                    <span style="font-family: var(--font-mono); font-weight: 600; color: var(--text-primary);">main.py</span>
                    <span class="history-lang-badge">PYTHON 3</span>
                  </div>
                  <span style="font-size: 11px; color: var(--text-muted);">Edited 10m ago</span>
                </div>
                <div style="font-family: var(--font-mono); font-size: 12px; color: var(--text-secondary); line-height: 1.5;">
                  def solve(): ... # Execution Engine & Multi-case Validator
                </div>
              </div>

              <div class="flex items-center gap-2">
                <a href="#/ide?lang=python" class="btn btn-primary btn-sm">Resume Editing</a>
                <a href="#/ide?lang=javascript" class="btn btn-secondary btn-sm">Switch to JS</a>
                <a href="#/ide?lang=cpp" class="btn btn-secondary btn-sm">Switch to C++</a>
              </div>
            </div>

            <!-- 365-Day Activity Heatmap -->
            <div class="card">
              <div class="card-header">
                <span class="card-title">Coding Activity Streak</span>
                <span style="font-size: 11px; color: var(--text-muted);">Year 2026</span>
              </div>
              <div class="heatmap-container">
                ${mockAnalytics.heatmapData.map(d => {
                  let levelClass = '';
                  if (d.count > 6) levelClass = 'heatmap-level-4';
                  else if (d.count > 3) levelClass = 'heatmap-level-3';
                  else if (d.count > 1) levelClass = 'heatmap-level-2';
                  else if (d.count > 0) levelClass = 'heatmap-level-1';
                  return `<div class="heatmap-cell ${levelClass}" title="Day ${d.day}: ${d.count} commits/submissions"></div>`;
                }).join('')}
              </div>
            </div>

            <!-- Recent Submissions Table -->
            <div class="card">
              <div class="card-header">
                <span class="card-title">Recent Submissions</span>
                <a href="#/history?type=SUBMISSION" style="font-size: 11px; color: var(--accent-primary);">View All</a>
              </div>
              <div class="table-container">
                <table class="data-table">
                  <thead>
                    <tr>
                      <th>Time</th>
                      <th>Problem</th>
                      <th>Language</th>
                      <th>Status</th>
                      <th>Runtime</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td style="font-family: var(--font-mono); font-size: 11px;">14:32</td>
                      <td style="font-weight: 500;">Two Sum</td>
                      <td><span class="history-lang-badge">PYTHON</span></td>
                      <td><span class="output-status-pill status-accepted">Accepted</span></td>
                      <td style="font-family: var(--font-mono); font-size: 11px;">42 ms</td>
                    </tr>
                    <tr>
                      <td style="font-family: var(--font-mono); font-size: 11px;">13:50</td>
                      <td style="font-weight: 500;">LRU Cache</td>
                      <td><span class="history-lang-badge">CPP</span></td>
                      <td><span class="output-status-pill status-accepted">Accepted</span></td>
                      <td style="font-family: var(--font-mono); font-size: 11px;">18 ms</td>
                    </tr>
                    <tr>
                      <td style="font-family: var(--font-mono); font-size: 11px;">12:15</td>
                      <td style="font-weight: 500;">Valid Palindrome</td>
                      <td><span class="history-lang-badge">JAVA</span></td>
                      <td><span class="output-status-pill status-accepted">Accepted</span></td>
                      <td style="font-family: var(--font-mono); font-size: 11px;">65 ms</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Right Column: Problems to Solve & Upcoming Contests -->
          <div class="flex flex-col gap-4">
            <!-- Active Contest Card -->
            <div class="card" style="border-left: 3px solid var(--accent-primary);">
              <div class="card-header">
                <span class="card-title">Current & Upcoming Contest</span>
                <span class="output-status-pill status-running">Upcoming</span>
              </div>
              <h4 style="font-size: var(--fs-base); margin-bottom: var(--space-1);">CodePilot Bi-Weekly Cup #42</h4>
              <p style="font-size: var(--fs-xs); color: var(--text-muted); margin-bottom: var(--space-3);">
                4 Algorithmic Problems | 90 Minutes | Penalty 10 min
              </p>
              <div class="flex justify-between items-center">
                <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-secondary);">Starts in 4h 15m</span>
                <a href="#/contests" class="btn btn-primary btn-sm">Register Now</a>
              </div>
            </div>

            <!-- Problems To Solve -->
            <div class="card">
              <div class="card-header">
                <span class="card-title">Problems To Solve</span>
                <a href="#/problems" style="font-size: 11px; color: var(--accent-primary);">Browse All</a>
              </div>
              <div class="flex flex-col gap-2">
                ${topProblems.map(p => `
                  <div class="flex justify-between items-center" style="padding: var(--space-2) var(--space-3); background: var(--bg-darkest); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm);">
                    <div>
                      <a href="#/problems/${p.id || p.slug}" style="font-weight: 500; font-size: var(--fs-xs); color: var(--text-primary);">${p.title}</a>
                      <div style="font-size: 10px; color: var(--text-muted);">${p.category || 'Algorithms'}</div>
                    </div>
                    <span class="badge-tag badge-${(p.difficulty || 'Easy').toLowerCase()}">${p.difficulty || 'Easy'}</span>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- Learning Platform Progress -->
            <div class="card">
              <div class="card-header">
                <span class="card-title">Learning Progress</span>
                <a href="#/courses" style="font-size: 11px; color: var(--accent-primary);">Academy</a>
              </div>
              <div>
                <div class="flex justify-between items-center" style="font-size: var(--fs-xs); margin-bottom: var(--space-1);">
                  <span>Algorithms & Data Structures</span>
                  <span style="font-family: var(--font-mono); color: var(--accent-primary);">65%</span>
                </div>
                <div style="height: 6px; background: var(--bg-darkest); border-radius: var(--radius-full); overflow: hidden; margin-bottom: var(--space-3);">
                  <div style="width: 65%; height: 100%; background: var(--accent-primary); border-radius: var(--radius-full);"></div>
                </div>
                <a href="#/courses" class="btn btn-secondary btn-sm w-full">Continue Next Lesson</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

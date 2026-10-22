/* Professional Developer Dashboard Page */
import { store } from '../state/store.js';
import { AuthService } from '../services/AuthService.js';
import { ProjectService } from '../services/ProjectService.js';
import { ProblemService } from '../services/ProblemService.js';
import { CourseService } from '../services/CourseService.js';

export class DashboardPage {
  static async render() {
    const user = store.get('currentUser') || AuthService.getCurrentUser();
    const displayName = user?.profile?.displayName || user?.username || 'Developer';
    const profile = user?.profile || {};

    // Determine greeting
    const hour = new Date().getHours();
    let greeting = 'Good morning';
    if (hour >= 12 && hour < 17) greeting = 'Good afternoon';
    else if (hour >= 17) greeting = 'Good evening';

    // Fetch real data in parallel
    let projects = [];
    let problems = [];
    let courses = [];

    try {
      [projects, problems, courses] = await Promise.all([
        ProjectService.getProjects().catch(() => []),
        ProblemService.getAll().catch(() => []),
        CourseService.getAll().catch(() => [])
      ]);
    } catch (e) {
      console.warn('[DashboardPage] Non-critical fetch error:', e);
    }

    const recentProjects = (projects || []).slice(0, 3);
    const topProblems = (problems || []).slice(0, 4);
    const recentCourses = (courses || []).slice(0, 2);

    return `
      <div class="page-wrapper">
        <!-- Dashboard Header -->
        <div class="page-header">
          <div>
            <h1 class="page-title">
              <span>${greeting}, ${displayName}</span>
            </h1>
            <p class="page-description">Continue where you left off. Cloud execution engine & isolated runtimes online.</p>
          </div>
          <div class="flex items-center gap-2">
            <a href="#/ide" class="btn btn-primary">▶ Open Cloud IDE</a>
            <a href="#/projects" class="btn btn-secondary">📁 My Projects</a>
          </div>
        </div>

        <!-- Real Key Developer Metrics -->
        <div class="metrics-row">
          <div class="metric-card">
            <div class="metric-label">Problems Solved</div>
            <div class="metric-value">${profile.problemsSolved ?? 0}</div>
            <div class="metric-delta">Rank: ${profile.rankTitle || 'Novice Developer'}</div>
          </div>

          <div class="metric-card">
            <div class="metric-label">Contest Rating</div>
            <div class="metric-value">${profile.contestRating ?? 1200}</div>
            <div class="metric-delta">Global Division II</div>
          </div>

          <div class="metric-card">
            <div class="metric-label">Active Workspaces</div>
            <div class="metric-value">${projects.length}</div>
            <div class="metric-delta">Persisted in SQLite</div>
          </div>

          <div class="metric-card">
            <div class="metric-label">Daily Streak</div>
            <div class="metric-value">${profile.streakDays ?? 0} Days</div>
            <div class="metric-delta">Logged in today</div>
          </div>
        </div>

        <!-- 2-Column Main Developer Dashboard Layout -->
        <div class="dashboard-grid">
          <!-- Left Column -->
          <div class="flex flex-col gap-4">
            <!-- Recent Projects & Workspaces -->
            <div class="card">
              <div class="card-header">
                <span class="card-title">Recent Workspaces</span>
                <a href="#/projects" style="font-size: 11px; color: var(--accent-primary); text-decoration: none;">View All (${projects.length}) →</a>
              </div>

              ${recentProjects.length > 0 ? `
                <div style="display: flex; flex-direction: column; gap: 8px;">
                  ${recentProjects.map(p => `
                    <div style="background: var(--bg-darkest); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 10px 12px; display: flex; justify-content: space-between; align-items: center;">
                      <div>
                        <div class="flex items-center gap-2">
                          <span class="badge-tag badge-easy">${(p.primaryLanguage || 'PYTHON').toUpperCase()}</span>
                          <a href="#/ide?project=${p.id}" style="font-family: var(--font-mono); font-size: 13px; font-weight: 600; color: var(--text-primary); text-decoration: none;">${p.title}</a>
                        </div>
                        <div style="font-size: 11px; color: var(--text-muted); margin-top: 4px;">
                          ${p.fileCount || 1} files • ${(p.totalSizeKb || 0.5)} KB
                        </div>
                      </div>
                      <a href="#/ide?project=${p.id}" class="btn btn-secondary btn-sm">Resume</a>
                    </div>
                  `).join('')}
                </div>
              ` : `
                <div class="empty-state" style="padding: 24px 12px;">
                  <div class="empty-title" style="font-size: 13px;">No projects yet</div>
                  <div class="empty-text" style="font-size: 11px;">Create your first workspace to start writing multi-file applications.</div>
                  <a href="#/projects" class="btn btn-primary btn-sm">+ Create Workspace</a>
                </div>
              `}
            </div>

            <!-- Recommended CP Problems -->
            <div class="card">
              <div class="card-header">
                <span class="card-title">Algorithmic Problem Challenges</span>
                <a href="#/problems" style="font-size: 11px; color: var(--accent-primary); text-decoration: none;">Browse Catalog →</a>
              </div>

              <div class="cp-table-container">
                <table class="cp-table">
                  <thead>
                    <tr>
                      <th>Problem</th>
                      <th>Category</th>
                      <th>Difficulty</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${topProblems.map(prob => {
                      let diffBadge = 'badge-easy';
                      if (prob.difficulty === 'Medium') diffBadge = 'badge-medium';
                      if (prob.difficulty === 'Hard') diffBadge = 'badge-hard';

                      return `
                        <tr>
                          <td>
                            <a href="#/problems/${prob.id || prob.slug}" style="color: var(--text-primary); font-weight: 500; text-decoration: none;">
                              ${prob.title}
                            </a>
                          </td>
                          <td style="color: var(--text-secondary);">${prob.category || 'Algorithms'}</td>
                          <td><span class="badge-tag ${diffBadge}">${prob.difficulty}</span></td>
                          <td>
                            <a href="#/problems/${prob.id || prob.slug}" class="btn btn-secondary btn-sm" style="font-size: 10px; padding: 2px 6px;">Solve</a>
                          </td>
                        </tr>
                      `;
                    }).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Right Column -->
          <div class="flex flex-col gap-4">
            <!-- Active Arena Contest -->
            <div class="card">
              <div class="card-header">
                <span class="card-title">Live Algorithmic Arena</span>
                <span class="badge-tag badge-live">LIVE</span>
              </div>
              <div style="font-size: 12px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px;">
                CodePilot Biweekly Arena #42
              </div>
              <p style="font-size: 11px; color: var(--text-secondary); line-height: 1.4; margin-bottom: 12px;">
                4 algorithmic challenges in 90 minutes. Global leaderboard and rating changes active.
              </p>
              <div class="flex items-center justify-between">
                <span style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">Ends in 5d 14h</span>
                <a href="#/contests" class="btn btn-primary btn-sm">Enter Arena</a>
              </div>
            </div>

            <!-- Learning Curriculum Progress -->
            <div class="card">
              <div class="card-header">
                <span class="card-title">Continue Learning</span>
                <a href="#/learning" style="font-size: 11px; color: var(--accent-primary); text-decoration: none;">All Courses →</a>
              </div>

              ${recentCourses.map(course => `
                <div style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid var(--border-subtle);">
                  <div style="font-size: 12px; font-weight: 600; color: var(--text-primary); margin-bottom: 2px;">
                    ${course.title}
                  </div>
                  <div style="font-size: 11px; color: var(--text-muted); margin-bottom: 6px;">
                    ${course.category} • ${course.difficulty}
                  </div>
                  <div style="background: var(--bg-darkest); height: 4px; border-radius: 2px; overflow: hidden; margin-bottom: 6px;">
                    <div style="background: var(--accent-emerald); width: 35%; height: 100%;"></div>
                  </div>
                  <div class="flex justify-between items-center" style="font-size: 10px; color: var(--text-muted);">
                    <span>35% completed</span>
                    <a href="#/courses/${course.slug}" style="color: var(--accent-primary); text-decoration: none;">Resume →</a>
                  </div>
                </div>
              `).join('')}
            </div>

            <!-- System Diagnostics Quick Link -->
            <div class="card">
              <div class="flex items-center justify-between">
                <div>
                  <div style="font-size: 12px; font-weight: 600; color: var(--text-primary);">Host Runtime Diagnostics</div>
                  <div style="font-size: 11px; color: var(--text-muted);">Python, GCC, Clang, OpenJDK, Rust, Go</div>
                </div>
                <a href="#/diagnostics" class="btn btn-secondary btn-sm">Status</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

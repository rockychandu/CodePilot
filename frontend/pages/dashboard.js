/* Dashboard Page Module */
import { store } from '../state/store.js';
import { mockAnalytics } from '../mock-data/analytics.js';
import { mockProblems } from '../mock-data/problems.js';

export class DashboardPage {
  static async render() {
    const user = store.get('currentUser');

    return `
      <div class="page-wrapper">
        <!-- Dashboard Header -->
        <div class="page-header">
          <div>
            <h1>Developer Dashboard</h1>
            <p class="text-secondary">Welcome back, ${user?.name || 'Developer'}! Multi-Language Execution Studio is active.</p>
          </div>
          <a href="#/ide" class="btn btn-primary">💻 Open IDE Studio</a>
        </div>

        <!-- 4 Key Stat Cards -->
        <div class="grid grid-cols-4 gap-6" style="margin-bottom: var(--space-8);">
          <div class="stat-widget">
            <div class="stat-widget-icon icon-blue">🧩</div>
            <div>
              <div class="text-muted" style="font-size: var(--fs-xs);">Problems Solved</div>
              <div style="font-size: var(--fs-2xl); font-weight: 800; color: var(--accent-cyan);">${user?.solvedCount || 142}</div>
            </div>
          </div>

          <div class="stat-widget">
            <div class="stat-widget-icon icon-purple">🏆</div>
            <div>
              <div class="text-muted" style="font-size: var(--fs-xs);">Contest Rating</div>
              <div style="font-size: var(--fs-2xl); font-weight: 800; color: var(--accent-purple);">${user?.rating || 1845}</div>
            </div>
          </div>

          <div class="stat-widget">
            <div class="stat-widget-icon icon-emerald">⚡</div>
            <div>
              <div class="text-muted" style="font-size: var(--fs-xs);">Total XP</div>
              <div style="font-size: var(--fs-2xl); font-weight: 800; color: var(--accent-emerald);">${user?.xp || 4250}</div>
            </div>
          </div>

          <div class="stat-widget">
            <div class="stat-widget-icon icon-amber">🔥</div>
            <div>
              <div class="text-muted" style="font-size: var(--fs-xs);">Daily Streak</div>
              <div style="font-size: var(--fs-2xl); font-weight: 800; color: var(--accent-amber);">${user?.streak || 7} Days</div>
            </div>
          </div>
        </div>

        <!-- Activity Heatmap Section -->
        <div class="card" style="margin-bottom: var(--space-8);">
          <div class="flex justify-between items-center" style="margin-bottom: var(--space-4);">
            <h3 style="font-size: var(--fs-lg);">365-Day Coding Activity Heatmap</h3>
            <span class="text-muted" style="font-size: var(--fs-xs);">148 Total Submissions in 2026</span>
          </div>

          <div class="heatmap-container">
            ${mockAnalytics.heatmapData.map(d => {
              let levelClass = '';
              if (d.count > 6) levelClass = 'heatmap-level-4';
              else if (d.count > 3) levelClass = 'heatmap-level-3';
              else if (d.count > 1) levelClass = 'heatmap-level-2';
              else if (d.count > 0) levelClass = 'heatmap-level-1';
              return `<div class="heatmap-cell ${levelClass}" title="Day ${d.day}: ${d.count} submissions"></div>`;
            }).join('')}
          </div>
        </div>

        <!-- Grid: Recommended Problems & Languages Shortcuts -->
        <div class="grid grid-cols-2 gap-6">
          <div class="card">
            <h3 style="font-size: var(--fs-lg); margin-bottom: var(--space-4);">Recommended Challenges</h3>
            <div class="flex flex-col gap-3">
              ${mockProblems.map(p => `
                <div class="flex justify-between items-center" style="padding: 12px; background: var(--bg-darkest); border-radius: var(--radius-md);">
                  <div>
                    <a href="#/problems/${p.id}" style="font-weight: 600;">${p.title}</a>
                    <div style="font-size: var(--fs-xs); color: var(--text-muted);">${p.topic}</div>
                  </div>
                  <span class="badge-tag badge-${p.difficulty.toLowerCase()}">${p.difficulty}</span>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="card">
            <h3 style="font-size: var(--fs-lg); margin-bottom: var(--space-4);">Quick Language Workbenches</h3>
            <div class="grid grid-cols-2 gap-3" style="margin-bottom: 16px;">
              <a href="#/ide?lang=python" class="btn btn-secondary btn-sm" style="justify-content: flex-start;">🐍 Python 3</a>
              <a href="#/ide?lang=c" class="btn btn-secondary btn-sm" style="justify-content: flex-start;">⚡ C (GCC)</a>
              <a href="#/ide?lang=cpp" class="btn btn-secondary btn-sm" style="justify-content: flex-start;">🚀 C++ 20</a>
              <a href="#/ide?lang=java" class="btn btn-secondary btn-sm" style="justify-content: flex-start;">☕ Java 21</a>
              <a href="#/ide?lang=javascript" class="btn btn-secondary btn-sm" style="justify-content: flex-start;">🟨 JavaScript</a>
              <a href="#/ide?lang=r" class="btn btn-secondary btn-sm" style="justify-content: flex-start;">📊 R Language</a>
              <a href="#/ide?lang=sql" class="btn btn-secondary btn-sm" style="justify-content: flex-start;">🗄️ SQL Query</a>
            </div>

            <a href="#/languages" class="btn btn-primary w-full" style="margin-top: var(--space-4);">Open Languages Studio</a>
          </div>
        </div>
      </div>
    `;
  }
}

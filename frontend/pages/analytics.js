/* Skill Analytics Page Module */
import { mockAnalytics } from '../mock-data/analytics.js';
import { SkillTreeComponent } from '../components/skill-tree.js';

export class AnalyticsPage {
  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Skill Analytics & Skill Tree</h1>
            <p class="text-secondary">Track your coding progression across Python, DSA, System Design, and AI.</p>
          </div>
        </div>

        <!-- Skill Tree Section -->
        <div class="card" style="margin-bottom: var(--space-8);">
          <h3 style="margin-bottom: var(--space-4);">Interactive Skill Progression Tree</h3>
          ${SkillTreeComponent.render()}
        </div>

        <!-- Skill Breakdown Grid -->
        <div class="grid grid-cols-2 gap-6">
          <div class="card">
            <h3 style="margin-bottom: var(--space-4);">Skill Rating Radar Breakdown</h3>
            <div class="flex flex-col gap-3">
              ${mockAnalytics.skillBreakdown.map(s => `
                <div>
                  <div class="flex justify-between" style="font-size: var(--fs-sm); margin-bottom: 4px;">
                    <span>${s.label}</span>
                    <strong style="color: var(--accent-cyan);">${s.score}/100</strong>
                  </div>
                  <div style="height: 8px; background: var(--bg-darkest); border-radius: 4px; overflow: hidden;">
                    <div style="width: ${s.score}%; height: 100%; background: var(--accent-cyan);"></div>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="card flex flex-col justify-between">
            <div>
              <h3 style="margin-bottom: var(--space-4);">Difficulty Distribution</h3>
              <div style="font-size: var(--fs-sm); color: var(--text-secondary); display: flex; flex-direction: column; gap: 12px;">
                <div>🟢 Easy Solved: <strong style="color: #10B981;">75 Problems</strong></div>
                <div>🟡 Medium Solved: <strong style="color: #F59E0B;">52 Problems</strong></div>
                <div>🔴 Hard Solved: <strong style="color: #EF4444;">15 Problems</strong></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

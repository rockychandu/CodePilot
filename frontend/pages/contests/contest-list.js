/* Contests Page Module */
import { mockContests } from '../../mock-data/contests.js';

export class ContestListPage {
  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Live Coding Contests</h1>
            <p class="text-secondary">Compete biweekly with developers worldwide, earn XP, and rank on global leaderboards.</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-6">
          ${mockContests.map(c => `
            <div class="card" style="position: relative;">
              <div class="flex items-center justify-between" style="margin-bottom: 12px;">
                <span class="output-status-pill ${c.status === 'Live' ? 'status-running' : 'status-accepted'}">${c.status} Contest</span>
                <span class="text-muted" style="font-size: var(--fs-xs);">Duration: ${c.duration}</span>
              </div>

              <h3 style="font-size: var(--fs-xl); margin-bottom: 8px;">${c.title}</h3>
              <p class="text-muted" style="font-size: var(--fs-sm); margin-bottom: 16px;">Prize Pool: <strong style="color: var(--accent-amber);">${c.prizePool || 'XP & Badges'}</strong></p>

              ${c.status === 'Live' ? `
                <div style="background: var(--bg-darkest); padding: 12px; border-radius: var(--radius-md); margin-bottom: 16px;">
                  <div class="text-muted" style="font-size: 11px; text-transform: uppercase;">Live Countdown</div>
                  <div style="font-size: var(--fs-2xl); font-weight: 800; color: var(--accent-cyan); font-family: var(--font-mono);">01:42:15</div>
                </div>
              ` : ''}

              <button class="btn btn-primary w-full">${c.status === 'Live' ? 'Enter Arena' : 'View Leaderboard'}</button>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }
}

/* Professional Developer Contests & Arenas Page */
export class ContestListPage {
  static async render() {
    const liveContests = [
      {
        id: 42,
        slug: 'biweekly-contest-42',
        title: 'CodePilot Biweekly Algorithmic Arena #42',
        description: 'Compete against thousands of global developers across 4 algorithmic challenges in 90 minutes.',
        startTime: 'Live Now',
        duration: '90 Minutes',
        participants: 3420,
        status: 'LIVE',
        endTime: '5d 14h 22m'
      }
    ];

    const upcomingContests = [
      {
        id: 43,
        slug: 'systems-challenge-8',
        title: 'Low-Latency C++ & Rust Systems Challenge #8',
        description: 'Multi-threaded lock-free algorithms, memory arena allocators, and socket performance benchmarks.',
        startTime: 'Saturday, 14:00 UTC',
        duration: '120 Minutes',
        participants: 1840,
        status: 'UPCOMING'
      },
      {
        id: 44,
        slug: 'biweekly-contest-43',
        title: 'CodePilot Biweekly Algorithmic Arena #43',
        description: 'Standard 4-problem Div 1 / Div 2 rating contest with hidden test case evaluation.',
        startTime: 'In 12 Days',
        duration: '90 Minutes',
        participants: 960,
        status: 'UPCOMING'
      }
    ];

    const completedContests = [
      {
        id: 41,
        slug: 'biweekly-contest-41',
        title: 'CodePilot Biweekly Algorithmic Arena #41',
        description: 'Dynamic programming, segment trees, and bipartite graphs.',
        startTime: 'Concluded',
        duration: '90 Minutes',
        participants: 4120,
        status: 'COMPLETED'
      }
    ];

    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1 class="page-title">
              <span>Coding Contests & Arenas</span>
            </h1>
            <p class="page-description">Real-time competitive programming with rating adjustments, hidden tests, and live leaderboards.</p>
          </div>
        </div>

        <!-- Section 1: Live Contests -->
        <div style="margin-bottom: var(--space-6);">
          <div style="font-size: var(--fs-sm); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: var(--space-3); display: flex; align-items: center; gap: 8px;">
            <span class="badge-tag badge-live">LIVE</span>
            <span>Active Contests</span>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: var(--space-4);">
            ${liveContests.map(c => `
              <div class="contest-card live-contest">
                <div>
                  <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                    <span class="badge-tag badge-live">● LIVE NOW</span>
                    <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">Duration: ${c.duration}</span>
                  </div>

                  <h3 style="font-size: var(--fs-md); font-weight: 600; color: var(--text-primary); margin-bottom: 6px;">${c.title}</h3>
                  <p style="font-size: var(--fs-xs); color: var(--text-secondary); line-height: 1.45; margin-bottom: 12px;">${c.description}</p>

                  <div style="background: var(--bg-darkest); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 8px 12px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                      <div style="font-size: 10px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em;">Arena Closes In</div>
                      <div id="live-countdown" style="font-family: var(--font-mono); font-size: 16px; font-weight: 700; color: var(--status-error);">01:34:52</div>
                    </div>
                    <div style="text-align: right;">
                      <div style="font-size: 10px; color: var(--text-muted);">Participants</div>
                      <div style="font-family: var(--font-mono); font-size: 13px; font-weight: 600; color: var(--text-primary);">${c.participants.toLocaleString()}</div>
                    </div>
                  </div>
                </div>

                <div class="flex items-center gap-2">
                  <a href="#/ide" class="btn btn-primary w-full">Enter Live Arena</a>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Section 2: Upcoming Contests -->
        <div style="margin-bottom: var(--space-6);">
          <div style="font-size: var(--fs-sm); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: var(--space-3);">
            Upcoming Contests
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: var(--space-3);">
            ${upcomingContests.map(c => `
              <div class="contest-card">
                <div>
                  <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                    <span class="badge-tag">${c.startTime}</span>
                    <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">${c.duration}</span>
                  </div>

                  <h4 style="font-size: var(--fs-sm); font-weight: 600; color: var(--text-primary); margin-bottom: 4px;">${c.title}</h4>
                  <p style="font-size: var(--fs-xs); color: var(--text-secondary); line-height: 1.4; margin-bottom: 12px;">${c.description}</p>
                </div>

                <div class="flex items-center justify-between" style="padding-top: 8px; border-top: 1px solid var(--border-subtle);">
                  <span style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">${c.participants} registered</span>
                  <button class="btn btn-secondary btn-sm">Register</button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>

        <!-- Section 3: Completed Contests -->
        <div>
          <div style="font-size: var(--fs-sm); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: var(--space-3);">
            Completed Contests
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: var(--space-3);">
            ${completedContests.map(c => `
              <div class="contest-card">
                <div>
                  <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                    <span class="badge-tag badge-easy">CONCLUDED</span>
                    <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">${c.participants} competitors</span>
                  </div>
                  <h4 style="font-size: var(--fs-sm); font-weight: 600; color: var(--text-primary); margin-bottom: 4px;">${c.title}</h4>
                  <p style="font-size: var(--fs-xs); color: var(--text-secondary); line-height: 1.4; margin-bottom: 12px;">${c.description}</p>
                </div>
                <div class="flex items-center justify-end">
                  <button class="btn btn-secondary btn-sm">View Leaderboard</button>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }

  static afterRender() {
    // Live Countdown Timer logic
    const timerElem = document.getElementById('live-countdown');
    if (timerElem) {
      let secondsLeft = 94 * 60 + 52;
      const interval = setInterval(() => {
        if (secondsLeft <= 0) {
          clearInterval(interval);
          return;
        }
        secondsLeft--;
        const hrs = Math.floor(secondsLeft / 3600).toString().padStart(2, '0');
        const mins = Math.floor((secondsLeft % 3600) / 60).toString().padStart(2, '0');
        const secs = (secondsLeft % 60).toString().padStart(2, '0');
        timerElem.textContent = `${hrs}:${mins}:${secs}`;
      }, 1000);
    }
  }
}

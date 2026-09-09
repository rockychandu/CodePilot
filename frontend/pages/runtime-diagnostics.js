/**
 * CodePilot Language Runtime Diagnostics Dashboard Component
 * Executes and presents automated smoke tests for all compiler and interpreter adapters.
 */

export function renderRuntimeDiagnosticsPage() {
  return `
    <div class="container" style="padding: 2.5rem 1.5rem; max-width: 1200px; margin: 0 auto;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem;">
        <div>
          <h1 style="font-size: 2rem; font-weight: 800; color: var(--text-primary); margin-bottom: 0.5rem;">
            ⚡ Multi-Language Runtime Matrix & Diagnostics
          </h1>
          <p style="color: var(--text-secondary); font-size: 0.95rem;">
            Real-time verification of native compiler binaries, sandbox I/O redirections, and memory isolation.
          </p>
        </div>
        <button class="btn btn-primary" id="run-diagnostics-btn" style="display: flex; align-items: center; gap: 0.5rem;">
          ▶ Run Complete Smoke Test Suite
        </button>
      </div>

      <!-- Overview Cards -->
      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1.25rem; margin-bottom: 2rem;">
        <div class="card" style="padding: 1.5rem; background: var(--surface-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
          <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.5rem;">Registered Engines</div>
          <div style="font-size: 2rem; font-weight: 800; color: var(--accent-primary);" id="total-runtimes-count">11</div>
        </div>
        <div class="card" style="padding: 1.5rem; background: var(--surface-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
          <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.5rem;">Native Host Compilers</div>
          <div style="font-size: 2rem; font-weight: 800; color: #10b981;" id="installed-runtimes-count">Detecting...</div>
        </div>
        <div class="card" style="padding: 1.5rem; background: var(--surface-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
          <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.5rem;">Sandbox Time Limit</div>
          <div style="font-size: 2rem; font-weight: 800; color: var(--text-primary);">5.0s</div>
        </div>
        <div class="card" style="padding: 1.5rem; background: var(--surface-secondary); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
          <div style="color: var(--text-secondary); font-size: 0.85rem; margin-bottom: 0.5rem;">Process Memory Cap</div>
          <div style="font-size: 2rem; font-weight: 800; color: var(--text-primary);">128 MB</div>
        </div>
      </div>

      <!-- Diagnostics Table -->
      <div class="card" style="overflow-x: auto; background: var(--surface-primary); border: 1px solid var(--border-color); border-radius: var(--radius-md);">
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
          <thead>
            <tr style="border-bottom: 1px solid var(--border-color); background: var(--surface-secondary); color: var(--text-secondary); text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.05em;">
              <th style="padding: 1rem 1.25rem;">Language</th>
              <th style="padding: 1rem 1.25rem;">Type</th>
              <th style="padding: 1rem 1.25rem;">Version / Binary</th>
              <th style="padding: 1rem 1.25rem;">Hello World</th>
              <th style="padding: 1rem 1.25rem;">I/O Pipeline</th>
              <th style="padding: 1rem 1.25rem;">Overall Status</th>
            </tr>
          </thead>
          <tbody id="runtime-diagnostics-tbody">
            <tr>
              <td colspan="6" style="padding: 3rem; text-align: center; color: var(--text-tertiary);">
                Click "Run Complete Smoke Test Suite" to execute runtime diagnostics across all language adapters.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  `;
}

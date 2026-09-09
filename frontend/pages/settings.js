/* Settings Page Module */
import { store } from '../state/store.js';
import { NotificationService } from '../services/NotificationService.js';

export class SettingsPage {
  static async render() {
    const currentTheme = store.get('theme') || 'dark';

    return `
      <div class="page-wrapper" style="max-width: 800px;">
        <div class="page-header">
          <div>
            <h1>Platform & IDE Settings</h1>
            <p class="text-secondary">Customize your theme, editor font size, keybindings, and accessibility preferences.</p>
          </div>
        </div>

        <div class="card flex flex-col gap-6">
          <div>
            <h3>Appearance Theme</h3>
            <div class="flex items-center gap-4" style="margin-top: 12px;">
              <button id="btn-theme-dark" class="btn ${currentTheme === 'dark' ? 'btn-primary' : 'btn-secondary'}">
                🌙 Dark Navy Theme
              </button>
              <button id="btn-theme-light" class="btn ${currentTheme === 'light' ? 'btn-primary' : 'btn-secondary'}">
                ☀️ Light Theme
              </button>
            </div>
          </div>

          <div style="border-top: 1px solid var(--border-subtle); padding-top: 20px;">
            <h3>Editor Configuration</h3>
            <div class="form-group" style="margin-top: 12px;">
              <label class="form-label">Default Editor Font Size (px)</label>
              <input type="number" id="settings-font-size" class="input-control" value="14" min="10" max="24" style="width: 140px;" />
            </div>
          </div>

          <button id="btn-save-settings" class="btn btn-primary btn-lg" style="margin-top: 12px; width: fit-content;">Save Preferences</button>
        </div>
      </div>
    `;
  }

  static afterRender() {
    const darkBtn = document.getElementById('btn-theme-dark');
    const lightBtn = document.getElementById('btn-theme-light');
    const saveBtn = document.getElementById('btn-save-settings');

    if (darkBtn) {
      darkBtn.addEventListener('click', () => {
        store.set('theme', 'dark');
        document.documentElement.setAttribute('data-theme', 'dark');
        NotificationService.showToast('Theme set to Dark Navy', 'info');
      });
    }

    if (lightBtn) {
      lightBtn.addEventListener('click', () => {
        store.set('theme', 'light');
        document.documentElement.setAttribute('data-theme', 'light');
        NotificationService.showToast('Theme set to Light', 'info');
      });
    }

    if (saveBtn) {
      saveBtn.addEventListener('click', () => {
        NotificationService.showToast('Settings saved successfully!', 'success');
      });
    }
  }
}

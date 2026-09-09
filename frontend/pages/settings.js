/* Settings Page Module */
import { store } from '../state/store.js';
import { AuthService } from '../services/AuthService.js';
import { NotificationService } from '../services/NotificationService.js';
import { validatePassword } from '../utils/validators.js';

export class SettingsPage {
  static async render() {
    const user = store.get('currentUser') || AuthService.getCurrentUser();
    const currentTheme = store.get('theme') || 'dark';

    return `
      <div class="page-wrapper" style="max-width: 860px; padding: var(--space-8) var(--space-4);">
        <div class="page-header" style="margin-bottom: var(--space-6);">
          <div>
            <h1 style="font-size: var(--fs-2xl); font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em;">Account & Platform Settings</h1>
            <p class="text-secondary" style="font-size: var(--fs-sm); margin-top: 4px;">Manage your developer credentials, security keys, active sessions, and IDE preferences.</p>
          </div>
        </div>

        <div class="flex flex-col gap-6">
          
          <!-- Account Overview -->
          <div class="card" style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: var(--space-6);">
            <h3 style="font-size: var(--fs-lg); font-weight: 600; color: var(--text-primary); margin-bottom: var(--space-4);">User Profile</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4);">
              <div>
                <span class="text-secondary" style="font-size: var(--fs-xs); text-transform: uppercase; font-weight: 600;">Username</span>
                <div style="font-weight: 600; color: var(--text-primary); font-size: var(--fs-md); margin-top: 2px;">${user?.username || 'developer'}</div>
              </div>
              <div>
                <span class="text-secondary" style="font-size: var(--fs-xs); text-transform: uppercase; font-weight: 600;">Email Address</span>
                <div style="font-weight: 600; color: var(--text-primary); font-size: var(--fs-md); margin-top: 2px;">${user?.email || 'dev@codepilot.io'}</div>
              </div>
              <div>
                <span class="text-secondary" style="font-size: var(--fs-xs); text-transform: uppercase; font-weight: 600;">Account Role</span>
                <div style="font-weight: 600; color: var(--accent-primary); font-size: var(--fs-md); margin-top: 2px;">${user?.role || 'USER'}</div>
              </div>
              <div>
                <span class="text-secondary" style="font-size: var(--fs-xs); text-transform: uppercase; font-weight: 600;">Status</span>
                <div style="font-weight: 600; color: #10b981; font-size: var(--fs-md); margin-top: 2px;">Active & Verified</div>
              </div>
            </div>
          </div>

          <!-- Security: Password Change -->
          <div class="card" style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: var(--space-6);">
            <h3 style="font-size: var(--fs-lg); font-weight: 600; color: var(--text-primary); margin-bottom: var(--space-2);">Security & Password</h3>
            <p class="text-secondary" style="font-size: var(--fs-xs); margin-bottom: var(--space-4);">Ensure your account uses a strong password with at least 8 characters, numbers, and symbols.</p>

            <form id="change-password-form" style="max-width: 460px;" novalidate>
              <div class="form-group" style="margin-bottom: var(--space-3);">
                <label class="form-label" for="curr-password" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; color: var(--text-secondary); display: block; margin-bottom: 4px;">Current Password</label>
                <input type="password" id="curr-password" class="input-control w-full" required style="height: 38px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);" />
              </div>

              <div class="form-group" style="margin-bottom: var(--space-3);">
                <label class="form-label" for="new-password" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; color: var(--text-secondary); display: block; margin-bottom: 4px;">New Password</label>
                <input type="password" id="new-password" class="input-control w-full" required style="height: 38px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);" />
                <div id="err-new-pass" style="color: #f87171; font-size: 11px; margin-top: 4px; display: none;"></div>
              </div>

              <div class="form-group" style="margin-bottom: var(--space-4);">
                <label class="form-label" for="confirm-new-password" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; color: var(--text-secondary); display: block; margin-bottom: 4px;">Confirm New Password</label>
                <input type="password" id="confirm-new-password" class="input-control w-full" required style="height: 38px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);" />
                <div id="err-conf-pass" style="color: #f87171; font-size: 11px; margin-top: 4px; display: none;"></div>
              </div>

              <button type="submit" id="btn-update-password" class="btn btn-secondary btn-sm" style="font-weight: 600;">Update Password</button>
            </form>
          </div>

          <!-- Session Management -->
          <div class="card" style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: var(--space-6);">
            <h3 style="font-size: var(--fs-lg); font-weight: 600; color: var(--text-primary); margin-bottom: var(--space-2);">Active Sessions</h3>
            <p class="text-secondary" style="font-size: var(--fs-xs); margin-bottom: var(--space-4);">If you suspect unauthorized access, you can terminate all other active browser sessions.</p>

            <div class="flex items-center gap-4">
              <button id="btn-logout-all" class="btn btn-outline btn-sm" style="color: #f87171; border-color: rgba(239, 68, 68, 0.4);">
                Sign Out of All Devices
              </button>
              <button id="btn-logout-current" class="btn btn-secondary btn-sm">
                Sign Out Current Session
              </button>
            </div>
          </div>

          <!-- Appearance & Editor Preferences -->
          <div class="card" style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: var(--space-6);">
            <h3 style="font-size: var(--fs-lg); font-weight: 600; color: var(--text-primary); margin-bottom: var(--space-4);">Appearance & Editor</h3>
            
            <div style="margin-bottom: var(--space-4);">
              <label class="form-label" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; color: var(--text-secondary); display: block; margin-bottom: 8px;">Theme</label>
              <div class="flex items-center gap-4">
                <button id="btn-theme-dark" class="btn ${currentTheme === 'dark' ? 'btn-primary' : 'btn-secondary'} btn-sm">
                  🌙 Dark Zinc
                </button>
                <button id="btn-theme-light" class="btn ${currentTheme === 'light' ? 'btn-primary' : 'btn-secondary'} btn-sm">
                  ☀️ Light
                </button>
              </div>
            </div>

            <div class="form-group" style="margin-bottom: var(--space-4);">
              <label class="form-label" for="settings-font-size" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; color: var(--text-secondary); display: block; margin-bottom: 4px;">Editor Font Size (px)</label>
              <input type="number" id="settings-font-size" class="input-control" value="14" min="10" max="24" style="width: 120px; height: 36px; background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);" />
            </div>

            <button id="btn-save-settings" class="btn btn-primary btn-sm" style="font-weight: 600;">Save Preferences</button>
          </div>

        </div>
      </div>
    `;
  }

  static afterRender({ router }) {
    const darkBtn = document.getElementById('btn-theme-dark');
    const lightBtn = document.getElementById('btn-theme-light');
    const saveBtn = document.getElementById('btn-save-settings');
    const passForm = document.getElementById('change-password-form');
    const currPassInput = document.getElementById('curr-password');
    const newPassInput = document.getElementById('new-password');
    const confPassInput = document.getElementById('confirm-new-password');
    const errNew = document.getElementById('err-new-pass');
    const errConf = document.getElementById('err-conf-pass');
    const btnUpdatePass = document.getElementById('btn-update-password');
    const btnLogoutAll = document.getElementById('btn-logout-all');
    const btnLogoutCurrent = document.getElementById('btn-logout-current');

    if (darkBtn) {
      darkBtn.addEventListener('click', () => {
        store.set('theme', 'dark');
        document.documentElement.setAttribute('data-theme', 'dark');
        NotificationService.showToast('Theme set to Dark Zinc', 'info');
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
        NotificationService.showToast('Preferences saved successfully!', 'success');
      });
    }

    if (passForm) {
      passForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        errNew.style.display = 'none';
        errConf.style.display = 'none';

        const curr = currPassInput?.value || '';
        const nw = newPassInput?.value || '';
        const conf = confPassInput?.value || '';

        const pErr = validatePassword(nw);
        if (pErr) {
          errNew.textContent = pErr;
          errNew.style.display = 'block';
          return;
        }

        if (nw !== conf) {
          errConf.textContent = 'Passwords do not match.';
          errConf.style.display = 'block';
          return;
        }

        btnUpdatePass.disabled = true;
        btnUpdatePass.textContent = 'Updating...';

        try {
          await AuthService.changePassword(curr, nw);
          NotificationService.showToast('Password updated successfully!', 'success');
          currPassInput.value = '';
          newPassInput.value = '';
          confPassInput.value = '';
        } catch (err) {
          NotificationService.showToast(err.message, 'error');
        } finally {
          btnUpdatePass.disabled = false;
          btnUpdatePass.textContent = 'Update Password';
        }
      });
    }

    if (btnLogoutCurrent) {
      btnLogoutCurrent.addEventListener('click', async () => {
        await AuthService.logout();
        store.set('currentUser', null);
        store.set('isAuthenticated', false);
        NotificationService.showToast('Signed out successfully.', 'info');
        router.navigate('/login');
      });
    }

    if (btnLogoutAll) {
      btnLogoutAll.addEventListener('click', async () => {
        await AuthService.logoutAll();
        store.set('currentUser', null);
        store.set('isAuthenticated', false);
        NotificationService.showToast('All sessions revoked. Please sign in again.', 'info');
        router.navigate('/login');
      });
    }
  }
}

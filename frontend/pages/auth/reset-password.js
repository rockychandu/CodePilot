/* Reset Password Page Module */
import { AuthService } from '../../services/AuthService.js';
import { evaluatePasswordStrength, validatePassword } from '../../utils/validators.js';
import { NotificationService } from '../../services/NotificationService.js';

export class ResetPasswordPage {
  static async render({ queryParams }) {
    const token = queryParams?.token || '';

    return `
      <div class="page-wrapper flex items-center justify-center" style="min-height: 80vh; padding: var(--space-8) var(--space-4);">
        <div class="card w-full" style="max-width: 440px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); padding: var(--space-8);">
          
          <div class="text-center" style="margin-bottom: var(--space-6);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: var(--radius-md); background: var(--bg-elevated); border: 1px solid var(--border-medium); margin-bottom: var(--space-3);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 2l-2 2m-1-1l2 2M11 13l9-9m-6 0l4 4"></path>
                <circle cx="7.5" cy="16.5" r="5.5"></circle>
              </svg>
            </div>
            <h2 style="font-size: var(--fs-xl); font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em;">Set New Password</h2>
            <p class="text-secondary" style="font-size: var(--fs-sm); margin-top: 4px;">Choose a strong new password for your account</p>
          </div>

          <div id="reset-server-alert" class="hidden" style="margin-bottom: var(--space-4); padding: var(--space-3) var(--space-4); background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: var(--radius-md); color: #f87171; font-size: var(--fs-sm);">
            <span id="reset-server-alert-msg"></span>
          </div>

          <form id="reset-form" novalidate>
            <div class="form-group" style="margin-bottom: var(--space-4);">
              <label class="form-label" for="reset-token" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                Reset Token
              </label>
              <input 
                type="text" 
                id="reset-token" 
                class="input-control w-full" 
                value="${token}" 
                placeholder="Paste token from recovery email" 
                required 
                style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
              />
            </div>

            <div class="form-group" style="margin-bottom: var(--space-4);">
              <label class="form-label" for="reset-password" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                New Password
              </label>
              <input 
                type="password" 
                id="reset-password" 
                class="input-control w-full" 
                placeholder="••••••••••••" 
                required 
                style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
              />
              <div id="err-reset-pass" class="form-error" style="color: #f87171; font-size: 11px; margin-top: 4px; display: none;"></div>
            </div>

            <div class="form-group" style="margin-bottom: var(--space-5);">
              <label class="form-label" for="reset-confirm" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                Confirm New Password
              </label>
              <input 
                type="password" 
                id="reset-confirm" 
                class="input-control w-full" 
                placeholder="••••••••••••" 
                required 
                style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
              />
              <div id="err-reset-match" class="form-error" style="color: #f87171; font-size: 11px; margin-top: 4px; display: none;"></div>
            </div>

            <button 
              type="submit" 
              id="btn-submit-reset" 
              class="btn btn-primary w-full" 
              style="height: 42px; font-size: var(--fs-sm); font-weight: 600; justify-content: center;"
            >
              Update Password
            </button>
          </form>

          <div class="text-center" style="margin-top: var(--space-6); padding-top: var(--space-4); border-top: 1px solid var(--border-subtle); font-size: 13px; color: var(--text-secondary);">
            <a href="#/login" style="color: var(--accent-primary); font-weight: 600; text-decoration: none;">Return to Sign In</a>
          </div>
        </div>
      </div>
    `;
  }

  static afterRender({ router }) {
    const form = document.getElementById('reset-form');
    const tokenInput = document.getElementById('reset-token');
    const passInput = document.getElementById('reset-password');
    const confInput = document.getElementById('reset-confirm');
    const errPass = document.getElementById('err-reset-pass');
    const errMatch = document.getElementById('err-reset-match');
    const serverAlert = document.getElementById('reset-server-alert');
    const serverAlertMsg = document.getElementById('reset-server-alert-msg');
    const submitBtn = document.getElementById('btn-submit-reset');

    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      serverAlert.classList.add('hidden');
      errPass.style.display = 'none';
      errMatch.style.display = 'none';

      const token = (tokenInput?.value || '').trim();
      const password = passInput?.value || '';
      const confirm = confInput?.value || '';

      if (!token) {
        serverAlertMsg.textContent = 'A valid reset token is required.';
        serverAlert.classList.remove('hidden');
        return;
      }

      const pErr = validatePassword(password);
      if (pErr) {
        errPass.textContent = pErr;
        errPass.style.display = 'block';
        return;
      }

      if (password !== confirm) {
        errMatch.textContent = 'Passwords do not match.';
        errMatch.style.display = 'block';
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = 'Updating...';

      try {
        await AuthService.resetPassword(token, password);
        NotificationService.showToast('Password reset successful! Please sign in.', 'success');
        router.navigate('/login');
      } catch (err) {
        serverAlertMsg.textContent = err.message || 'Password reset failed.';
        serverAlert.classList.remove('hidden');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Update Password';
      }
    });
  }
}

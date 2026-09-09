/* Sign In Page Module - Clean Developer Aesthetic */
import { AuthService } from '../../services/AuthService.js';
import { NotificationService } from '../../services/NotificationService.js';
import { store } from '../../state/store.js';

export class LoginPage {
  static async render({ queryParams }) {
    const redirectUrl = queryParams?.redirect || '/dashboard';

    return `
      <div class="page-wrapper flex items-center justify-center" style="min-height: 80vh; padding: var(--space-8) var(--space-4);">
        <div class="card w-full" style="max-width: 440px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); padding: var(--space-8);">
          
          <!-- Header -->
          <div class="text-center" style="margin-bottom: var(--space-6);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: var(--radius-md); background: var(--bg-elevated); border: 1px solid var(--border-medium); margin-bottom: var(--space-3);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--text-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="16 18 22 12 16 6"></polyline>
                <polyline points="8 6 2 12 8 18"></polyline>
              </svg>
            </div>
            <h2 style="font-size: var(--fs-xl); font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em;">Welcome back</h2>
            <p class="text-secondary" style="font-size: var(--fs-sm); margin-top: 4px;">Sign in to your CodePilot developer account</p>
          </div>

          <!-- Server Error Alert -->
          <div id="login-server-alert" class="hidden" style="margin-bottom: var(--space-4); padding: var(--space-3) var(--space-4); background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: var(--radius-md); color: #f87171; font-size: var(--fs-sm);">
            <span id="login-server-alert-msg"></span>
          </div>

          <!-- Form -->
          <form id="login-form" novalidate>
            <input type="hidden" id="login-redirect" value="${redirectUrl}" />

            <div class="form-group" style="margin-bottom: var(--space-4);">
              <label class="form-label" for="login-identifier" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                Email or Username
              </label>
              <input 
                type="text" 
                id="login-identifier" 
                class="input-control w-full" 
                placeholder="alex.developer or alex@codepilot.dev" 
                autocomplete="username"
                required 
                style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
              />
              <div id="err-login-identifier" class="form-error" style="color: #f87171; font-size: 12px; margin-top: 4px; display: none;"></div>
            </div>

            <div class="form-group" style="margin-bottom: var(--space-4);">
              <div class="flex justify-between items-center" style="margin-bottom: 6px;">
                <label class="form-label" for="login-password" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin: 0;">
                  Password
                </label>
                <a href="#/forgot-password" style="font-size: 12px; color: var(--accent-primary); text-decoration: none;">Forgot password?</a>
              </div>
              <div style="position: relative;">
                <input 
                  type="password" 
                  id="login-password" 
                  class="input-control w-full" 
                  placeholder="••••••••••••" 
                  autocomplete="current-password"
                  required 
                  style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 40px 0 12px; color: var(--text-primary);"
                />
                <button 
                  type="button" 
                  id="btn-toggle-password" 
                  style="position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 4px; font-size: 14px;" 
                  title="Show / Hide Password"
                  tabindex="-1"
                >
                  👁️
                </button>
              </div>
              <div id="err-login-password" class="form-error" style="color: #f87171; font-size: 12px; margin-top: 4px; display: none;"></div>
            </div>

            <div class="flex items-center justify-between" style="margin-bottom: var(--space-6); font-size: var(--fs-sm);">
              <label class="flex items-center gap-2" style="cursor: pointer; color: var(--text-secondary); font-size: 13px;">
                <input type="checkbox" id="login-remember" checked style="accent-color: var(--accent-primary); cursor: pointer;" />
                <span>Remember me on this device</span>
              </label>
            </div>

            <button 
              type="submit" 
              id="btn-submit-login" 
              class="btn btn-primary w-full" 
              style="height: 42px; font-size: var(--fs-sm); font-weight: 600; justify-content: center; letter-spacing: 0.02em;"
            >
              <span id="btn-login-text">Sign In to CodePilot</span>
              <span id="btn-login-spinner" class="hidden" style="margin-left: 8px;">⏳</span>
            </button>
          </form>

          <!-- Footer -->
          <div class="text-center" style="margin-top: var(--space-6); padding-top: var(--space-4); border-top: 1px solid var(--border-subtle); font-size: 13px; color: var(--text-secondary);">
            Don't have an account? <a href="#/register" style="color: var(--accent-primary); font-weight: 600; text-decoration: none;">Create one for free</a>
          </div>

          <div class="text-center" style="margin-top: var(--space-3); font-size: 11px; color: var(--text-muted);">
            Protected by enterprise PBKDF2 authentication & rate limiting.
          </div>
        </div>
      </div>
    `;
  }

  static afterRender({ router }) {
    const form = document.getElementById('login-form');
    const idInput = document.getElementById('login-identifier');
    const passInput = document.getElementById('login-password');
    const toggleBtn = document.getElementById('btn-toggle-password');
    const rememberBox = document.getElementById('login-remember');
    const submitBtn = document.getElementById('btn-submit-login');
    const btnText = document.getElementById('btn-login-text');
    const btnSpinner = document.getElementById('btn-login-spinner');
    const serverAlert = document.getElementById('login-server-alert');
    const serverAlertMsg = document.getElementById('login-server-alert-msg');
    const errId = document.getElementById('err-login-identifier');
    const errPass = document.getElementById('err-login-password');
    const redirectField = document.getElementById('login-redirect');

    if (!form) return;

    // Toggle password visibility
    if (toggleBtn && passInput) {
      toggleBtn.addEventListener('click', () => {
        if (passInput.type === 'password') {
          passInput.type = 'text';
          toggleBtn.textContent = '🔒';
        } else {
          passInput.type = 'password';
          toggleBtn.textContent = '👁️';
        }
      });
    }

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Reset errors
      serverAlert.classList.add('hidden');
      errId.style.display = 'none';
      errId.textContent = '';
      errPass.style.display = 'none';
      errPass.textContent = '';

      const identifier = (idInput?.value || '').trim();
      const password = passInput?.value || '';
      const remember = rememberBox?.checked ?? true;

      let hasClientError = false;
      if (!identifier) {
        errId.textContent = 'Please enter your username or email address.';
        errId.style.display = 'block';
        hasClientError = true;
      }
      if (!password) {
        errPass.textContent = 'Please enter your password.';
        errPass.style.display = 'block';
        hasClientError = true;
      }

      if (hasClientError) return;

      // Loading State
      submitBtn.disabled = true;
      btnText.textContent = 'Signing in...';
      btnSpinner.classList.remove('hidden');

      try {
        const res = await AuthService.login(identifier, password, remember);
        store.set('currentUser', res.user);
        store.set('isAuthenticated', true);

        NotificationService.showToast(`Welcome back, ${res.user.displayName || res.user.username}!`, 'success');

        const dest = redirectField?.value || '/dashboard';
        router.navigate(dest.startsWith('/') ? dest : `/${dest}`);
      } catch (err) {
        serverAlertMsg.textContent = err.message || 'Invalid username or password.';
        serverAlert.classList.remove('hidden');
        NotificationService.showToast(err.message || 'Login failed', 'error');
      } finally {
        submitBtn.disabled = false;
        btnText.textContent = 'Sign In to CodePilot';
        btnSpinner.classList.add('hidden');
      }
    });
  }
}

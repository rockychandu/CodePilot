/* Forgot Password Page Module */
import { AuthService } from '../../services/AuthService.js';
import { validateEmail } from '../../utils/validators.js';
import { NotificationService } from '../../services/NotificationService.js';

export class ForgotPasswordPage {
  static async render() {
    return `
      <div class="page-wrapper flex items-center justify-center" style="min-height: 80vh; padding: var(--space-8) var(--space-4);">
        <div class="card w-full" style="max-width: 440px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); padding: var(--space-8);">
          
          <div class="text-center" style="margin-bottom: var(--space-6);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: var(--radius-md); background: var(--bg-elevated); border: 1px solid var(--border-medium); margin-bottom: var(--space-3);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--text-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
            </div>
            <h2 style="font-size: var(--fs-xl); font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em;">Reset Password</h2>
            <p class="text-secondary" style="font-size: var(--fs-sm); margin-top: 4px;">Enter your account email to receive recovery instructions</p>
          </div>

          <div id="forgot-success-banner" class="hidden" style="margin-bottom: var(--space-4); padding: var(--space-4); background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: var(--radius-md); color: #34d399; font-size: var(--fs-sm);">
            <div style="font-weight: 600; margin-bottom: 4px;">Password Reset Dispatched</div>
            <div id="forgot-success-text">If an account exists for that email, recovery instructions have been sent.</div>
          </div>

          <form id="forgot-form" novalidate>
            <div class="form-group" style="margin-bottom: var(--space-5);">
              <label class="form-label" for="forgot-email" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                Account Email Address
              </label>
              <input 
                type="email" 
                id="forgot-email" 
                class="input-control w-full" 
                placeholder="alex.developer@company.com" 
                required 
                style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
              />
              <div id="err-forgot-email" class="form-error" style="color: #f87171; font-size: 11px; margin-top: 4px; display: none;"></div>
            </div>

            <button 
              type="submit" 
              id="btn-submit-forgot" 
              class="btn btn-primary w-full" 
              style="height: 42px; font-size: var(--fs-sm); font-weight: 600; justify-content: center;"
            >
              Send Reset Instructions
            </button>
          </form>

          <div class="text-center" style="margin-top: var(--space-6); padding-top: var(--space-4); border-top: 1px solid var(--border-subtle); font-size: 13px; color: var(--text-secondary);">
            Remembered your credentials? <a href="#/login" style="color: var(--accent-primary); font-weight: 600; text-decoration: none;">Return to Sign In</a>
          </div>
        </div>
      </div>
    `;
  }

  static afterRender() {
    const form = document.getElementById('forgot-form');
    const emailInput = document.getElementById('forgot-email');
    const errEmail = document.getElementById('err-forgot-email');
    const successBanner = document.getElementById('forgot-success-banner');
    const successText = document.getElementById('forgot-success-text');
    const submitBtn = document.getElementById('btn-submit-forgot');

    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      errEmail.style.display = 'none';

      const email = (emailInput?.value || '').trim();
      const err = validateEmail(email);
      if (err) {
        errEmail.textContent = err;
        errEmail.style.display = 'block';
        return;
      }

      submitBtn.disabled = true;
      submitBtn.textContent = 'Sending...';

      try {
        const res = await AuthService.requestPasswordReset(email);
        successText.textContent = res.message || 'If an account exists, recovery instructions have been sent.';
        successBanner.classList.remove('hidden');
        NotificationService.showToast('Password reset instructions dispatched.', 'info');
      } catch (err) {
        NotificationService.showToast(err.message, 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Reset Instructions';
      }
    });
  }
}

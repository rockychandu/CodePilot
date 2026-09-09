/* Verify Email Page Module */
import { AuthService } from '../../services/AuthService.js';
import { NotificationService } from '../../services/NotificationService.js';

export class VerifyEmailPage {
  static async render({ queryParams }) {
    const token = queryParams?.token || '';

    return `
      <div class="page-wrapper flex items-center justify-center" style="min-height: 80vh; padding: var(--space-8) var(--space-4);">
        <div class="card w-full" style="max-width: 460px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); padding: var(--space-8);">
          
          <div class="text-center" style="margin-bottom: var(--space-6);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 48px; height: 48px; border-radius: var(--radius-md); background: var(--bg-elevated); border: 1px solid var(--border-medium); margin-bottom: var(--space-3);">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
            </div>
            <h2 style="font-size: var(--fs-xl); font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em;">Verify Your Email</h2>
            <p class="text-secondary" style="font-size: var(--fs-sm); margin-top: 4px;">Confirm your email address to unlock full developer features</p>
          </div>

          <div id="verify-status-box" style="margin-bottom: var(--space-5);">
            <div id="verify-loading" class="hidden text-center" style="padding: var(--space-4);">
              <div style="font-size: 24px; margin-bottom: 8px;">⏳</div>
              <p class="text-secondary" style="font-size: var(--fs-sm);">Verifying your email token...</p>
            </div>

            <div id="verify-success" class="hidden" style="padding: var(--space-4); background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: var(--radius-md); text-align: center;">
              <div style="font-size: 28px; margin-bottom: 8px;">✅</div>
              <h3 style="color: #34d399; font-size: var(--fs-md); font-weight: 600; margin-bottom: 4px;">Email Verified!</h3>
              <p class="text-secondary" style="font-size: var(--fs-xs); margin-bottom: var(--space-4);">Your account email has been successfully confirmed.</p>
              <a href="#/dashboard" class="btn btn-primary w-full" style="justify-content: center;">Continue to Dashboard</a>
            </div>

            <div id="verify-error" class="hidden" style="padding: var(--space-4); background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: var(--radius-md); text-align: center;">
              <div style="font-size: 28px; margin-bottom: 8px;">❌</div>
              <h3 style="color: #f87171; font-size: var(--fs-md); font-weight: 600; margin-bottom: 4px;">Verification Failed</h3>
              <p id="verify-error-msg" class="text-secondary" style="font-size: var(--fs-xs); margin-bottom: var(--space-4);">The verification token is invalid or has expired.</p>
            </div>
          </div>

          <form id="verify-form" novalidate>
            <div class="form-group" style="margin-bottom: var(--space-4);">
              <label class="form-label" for="verify-token-input" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                Verification Token
              </label>
              <input 
                type="text" 
                id="verify-token-input" 
                class="input-control w-full" 
                value="${token}" 
                placeholder="Paste code or token from verification email" 
                required 
                style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
              />
            </div>

            <button 
              type="submit" 
              id="btn-submit-verify" 
              class="btn btn-primary w-full" 
              style="height: 42px; font-size: var(--fs-sm); font-weight: 600; justify-content: center;"
            >
              Verify Token
            </button>
          </form>

          <div class="text-center" style="margin-top: var(--space-6); padding-top: var(--space-4); border-top: 1px solid var(--border-subtle); font-size: 13px; color: var(--text-secondary);">
            <a href="#/dashboard" style="color: var(--accent-primary); font-weight: 600; text-decoration: none;">Skip for now</a>
          </div>
        </div>
      </div>
    `;
  }

  static async afterRender({ queryParams }) {
    const form = document.getElementById('verify-form');
    const tokenInput = document.getElementById('verify-token-input');
    const loadingBox = document.getElementById('verify-loading');
    const successBox = document.getElementById('verify-success');
    const errorBox = document.getElementById('verify-error');
    const errorMsg = document.getElementById('verify-error-msg');
    const submitBtn = document.getElementById('btn-submit-verify');

    const handleVerification = async (token) => {
      if (!token) return;
      loadingBox.classList.remove('hidden');
      successBox.classList.add('hidden');
      errorBox.classList.add('hidden');
      if (form) form.classList.add('hidden');

      try {
        await AuthService.verifyEmail(token);
        loadingBox.classList.add('hidden');
        successBox.classList.remove('hidden');
        NotificationService.showToast('Email verified successfully!', 'success');
      } catch (err) {
        loadingBox.classList.add('hidden');
        errorMsg.textContent = err.message || 'The verification token is invalid or has expired.';
        errorBox.classList.remove('hidden');
        if (form) form.classList.remove('hidden');
      }
    };

    if (queryParams?.token) {
      await handleVerification(queryParams.token);
    }

    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = (tokenInput?.value || '').trim();
        if (token) {
          await handleVerification(token);
        }
      });
    }
  }
}

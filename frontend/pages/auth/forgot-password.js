/* Forgot Password Page Module */
import { AuthService } from '../../services/AuthService.js';
import { NotificationService } from '../../services/NotificationService.js';

export class ForgotPasswordPage {
  static async render() {
    return `
      <div class="page-wrapper flex items-center justify-center" style="min-height: 80vh;">
        <div class="card card-glass w-full" style="max-width: 440px; padding: var(--space-8);">
          <div class="text-center" style="margin-bottom: var(--space-6);">
            <img src="frontend/assets/logo.svg" style="width: 48px; height: 48px; margin-bottom: 12px;" alt="Logo" />
            <h2>Reset Your Password</h2>
            <p class="text-secondary" style="font-size: var(--fs-sm); margin-top: 4px;">Enter your email address to receive reset instructions</p>
          </div>

          <form id="forgot-form">
            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" id="forgot-email" class="input-control" placeholder="alex@codepilot.io" required />
            </div>

            <button type="submit" class="btn btn-primary w-full btn-lg" style="margin-top: var(--space-4);">Reset Password</button>
          </form>

          <div class="text-center" style="margin-top: var(--space-6); font-size: var(--fs-sm);">
            <a href="#/login">Return to Sign In</a>
          </div>
        </div>
      </div>
    `;
  }

  static afterRender({ router }) {
    const form = document.getElementById('forgot-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('forgot-email').value;
      try {
        const res = await AuthService.resetPassword(email);
        NotificationService.showToast(res.message, 'info');
        router.navigate('/login');
      } catch (err) {
        NotificationService.showToast(err.message, 'error');
      }
    });
  }
}

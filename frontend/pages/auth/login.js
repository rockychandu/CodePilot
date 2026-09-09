/* Sign In Page Module */
import { AuthService } from '../../services/AuthService.js';
import { NotificationService } from '../../services/NotificationService.js';

export class LoginPage {
  static async render() {
    return `
      <div class="page-wrapper flex items-center justify-center" style="min-height: 80vh;">
        <div class="card card-glass w-full" style="max-width: 440px; padding: var(--space-8);">
          <div class="text-center" style="margin-bottom: var(--space-6);">
            <img src="frontend/assets/logo.svg" style="width: 48px; height: 48px; margin-bottom: 12px;" alt="Logo" />
            <h2>Welcome back to CodePilot</h2>
            <p class="text-secondary" style="font-size: var(--fs-sm); margin-top: 4px;">Sign in to your developer account</p>
          </div>

          <form id="login-form">
            <div class="form-group">
              <label class="form-label" for="login-email">Email or Username</label>
              <input type="text" id="login-email" class="input-control" placeholder="alex.developer@codepilot.io" required />
              <div id="err-login-email" class="form-error"></div>
            </div>

            <div class="form-group">
              <div class="flex justify-between items-center">
                <label class="form-label" for="login-password">Password</label>
                <a href="#/forgot-password" style="font-size: var(--fs-xs);">Forgot password?</a>
              </div>
              <input type="password" id="login-password" class="input-control" placeholder="••••••••" required />
              <div id="err-login-password" class="form-error"></div>
            </div>

            <div class="flex items-center gap-2" style="margin-bottom: var(--space-6); font-size: var(--fs-sm);">
              <input type="checkbox" id="login-remember" checked />
              <label for="login-remember" class="text-secondary">Remember me on this browser</label>
            </div>

            <button type="submit" id="btn-submit-login" class="btn btn-primary w-full btn-lg">Sign In</button>
          </form>

          <div class="text-center" style="margin-top: var(--space-6); font-size: var(--fs-sm); color: var(--text-secondary);">
            Don't have an account? <a href="#/register" style="font-weight: 600;">Create Account</a>
          </div>
        </div>
      </div>
    `;
  }

  static afterRender({ router }) {
    const form = document.getElementById('login-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('login-email').value;
      const password = document.getElementById('login-password').value;
      const errEmail = document.getElementById('err-login-email');
      const errPass = document.getElementById('err-login-password');

      errEmail.innerText = '';
      errPass.innerText = '';

      try {
        await AuthService.login(email, password);
        NotificationService.showToast('Successfully signed in!', 'success');
        router.navigate('/dashboard');
      } catch (err) {
        if (err.message.includes('email')) errEmail.innerText = err.message;
        else if (err.message.includes('password')) errPass.innerText = err.message;
        else NotificationService.showToast(err.message, 'error');
      }
    });
  }
}

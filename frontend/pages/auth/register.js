/* Register Page Module */
import { AuthService } from '../../services/AuthService.js';
import { evaluatePasswordStrength } from '../../utils/validators.js';
import { NotificationService } from '../../services/NotificationService.js';

export class RegisterPage {
  static async render() {
    return `
      <div class="page-wrapper flex items-center justify-center" style="min-height: 85vh;">
        <div class="card card-glass w-full" style="max-width: 480px; padding: var(--space-8);">
          <div class="text-center" style="margin-bottom: var(--space-6);">
            <img src="frontend/assets/logo.svg" style="width: 48px; height: 48px; margin-bottom: 12px;" alt="Logo" />
            <h2>Create your CodePilot account</h2>
            <p class="text-secondary" style="font-size: var(--fs-sm); margin-top: 4px;">Join over 500,000+ developers</p>
          </div>

          <form id="register-form">
            <div class="form-group">
              <label class="form-label">Full Name</label>
              <input type="text" id="reg-name" class="input-control" placeholder="Alex Developer" required />
            </div>

            <div class="form-group">
              <label class="form-label">Username</label>
              <input type="text" id="reg-username" class="input-control" placeholder="alex_dev" required />
            </div>

            <div class="form-group">
              <label class="form-label">Email Address</label>
              <input type="email" id="reg-email" class="input-control" placeholder="alex@codepilot.io" required />
            </div>

            <div class="form-group">
              <label class="form-label">Password</label>
              <input type="password" id="reg-password" class="input-control" placeholder="••••••••" required />
              <!-- Password Strength Meter -->
              <div id="password-strength-bar" style="height: 4px; border-radius: 2px; background: var(--border-medium); margin-top: 6px; transition: all 250ms;"></div>
              <div id="password-strength-text" style="font-size: 11px; margin-top: 2px; text-align: right; color: var(--text-muted);">Strength: None</div>
            </div>

            <div class="form-group">
              <label class="form-label">Confirm Password</label>
              <input type="password" id="reg-confirm-password" class="input-control" placeholder="••••••••" required />
            </div>

            <button type="submit" class="btn btn-primary w-full btn-lg" style="margin-top: var(--space-4);">Create Account</button>
          </form>

          <div class="text-center" style="margin-top: var(--space-6); font-size: var(--fs-sm); color: var(--text-secondary);">
            Already registered? <a href="#/login" style="font-weight: 600;">Sign In</a>
          </div>
        </div>
      </div>
    `;
  }

  static afterRender({ router }) {
    const passInput = document.getElementById('reg-password');
    const bar = document.getElementById('password-strength-bar');
    const text = document.getElementById('password-strength-text');

    if (passInput) {
      passInput.addEventListener('input', (e) => {
        const str = evaluatePasswordStrength(e.target.value);
        text.innerText = `Strength: ${str.label}`;
        text.style.color = str.color;
        bar.style.background = str.color;
        bar.style.width = `${(str.score / 4) * 100}%`;
      });
    }

    const form = document.getElementById('register-form');
    if (form) {
      form.addEventListener('submit', async (e) => {
        e.preventDefault();
        try {
          await AuthService.register({
            name: document.getElementById('reg-name').value,
            username: document.getElementById('reg-username').value,
            email: document.getElementById('reg-email').value,
            password: document.getElementById('reg-password').value,
            confirmPassword: document.getElementById('reg-confirm-password').value
          });
          NotificationService.showToast('Account created successfully!', 'success');
          router.navigate('/dashboard');
        } catch (err) {
          NotificationService.showToast(err.message, 'error');
        }
      });
    }
  }
}

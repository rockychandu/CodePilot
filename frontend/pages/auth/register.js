/* Register Page Module - Restrained Developer UI */
import { AuthService } from '../../services/AuthService.js';
import { evaluatePasswordStrength, validateUsername, validateEmail, validatePassword } from '../../utils/validators.js';
import { NotificationService } from '../../services/NotificationService.js';
import { store } from '../../state/store.js';

export class RegisterPage {
  static async render() {
    return `
      <div class="page-wrapper flex items-center justify-center" style="min-height: 85vh; padding: var(--space-8) var(--space-4);">
        <div class="card w-full" style="max-width: 500px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); padding: var(--space-8);">
          
          <!-- Header -->
          <div class="text-center" style="margin-bottom: var(--space-6);">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: var(--radius-md); background: var(--bg-elevated); border: 1px solid var(--border-medium); margin-bottom: var(--space-3);">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--accent-primary)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <line x1="19" y1="8" x2="19" y2="14"></line>
                <line x1="22" y1="11" x2="16" y2="11"></line>
              </svg>
            </div>
            <h2 style="font-size: var(--fs-xl); font-weight: 700; color: var(--text-primary); letter-spacing: -0.02em;">Create your developer account</h2>
            <p class="text-secondary" style="font-size: var(--fs-sm); margin-top: 4px;">Join 500,000+ developers building on CodePilot</p>
          </div>

          <!-- Server Error Alert -->
          <div id="reg-server-alert" class="hidden" style="margin-bottom: var(--space-4); padding: var(--space-3) var(--space-4); background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: var(--radius-md); color: #f87171; font-size: var(--fs-sm);">
            <span id="reg-server-alert-msg"></span>
          </div>

          <form id="register-form" novalidate>
            <!-- Username & Display Name grid -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); margin-bottom: var(--space-4);">
              <div class="form-group">
                <label class="form-label" for="reg-username" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                  Username
                </label>
                <input 
                  type="text" 
                  id="reg-username" 
                  class="input-control w-full" 
                  placeholder="e.g. alex_dev" 
                  autocomplete="username"
                  required 
                  style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
                />
                <div id="err-reg-username" class="form-error" style="color: #f87171; font-size: 11px; margin-top: 4px; display: none;"></div>
              </div>

              <div class="form-group">
                <label class="form-label" for="reg-name" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                  Full Name
                </label>
                <input 
                  type="text" 
                  id="reg-name" 
                  class="input-control w-full" 
                  placeholder="e.g. Alex Rivera" 
                  autocomplete="name"
                  style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
                />
              </div>
            </div>

            <!-- Email Address -->
            <div class="form-group" style="margin-bottom: var(--space-4);">
              <label class="form-label" for="reg-email" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                Email Address
              </label>
              <input 
                type="email" 
                id="reg-email" 
                class="input-control w-full" 
                placeholder="alex.rivera@company.com" 
                autocomplete="email"
                required 
                style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
              />
              <div id="err-reg-email" class="form-error" style="color: #f87171; font-size: 11px; margin-top: 4px; display: none;"></div>
            </div>

            <!-- Password -->
            <div class="form-group" style="margin-bottom: var(--space-4);">
              <label class="form-label" for="reg-password" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                Password
              </label>
              <div style="position: relative;">
                <input 
                  type="password" 
                  id="reg-password" 
                  class="input-control w-full" 
                  placeholder="Minimum 8 characters with upper, lower, digit & symbol" 
                  autocomplete="new-password"
                  required 
                  style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 40px 0 12px; color: var(--text-primary);"
                />
                <button 
                  type="button" 
                  id="btn-toggle-reg-password" 
                  style="position: absolute; right: 8px; top: 50%; transform: translateY(-50%); background: none; border: none; color: var(--text-muted); cursor: pointer; padding: 4px; font-size: 14px;" 
                  title="Show / Hide Password"
                  tabindex="-1"
                >
                  👁️
                </button>
              </div>
              <div id="err-reg-password" class="form-error" style="color: #f87171; font-size: 11px; margin-top: 4px; display: none;"></div>

              <!-- Real-time Password Strength Meter -->
              <div style="margin-top: 8px;">
                <div style="display: flex; gap: 4px; height: 4px;">
                  <div id="str-seg-1" style="flex: 1; height: 100%; border-radius: 2px; background: var(--border-medium); transition: background 200ms;"></div>
                  <div id="str-seg-2" style="flex: 1; height: 100%; border-radius: 2px; background: var(--border-medium); transition: background 200ms;"></div>
                  <div id="str-seg-3" style="flex: 1; height: 100%; border-radius: 2px; background: var(--border-medium); transition: background 200ms;"></div>
                  <div id="str-seg-4" style="flex: 1; height: 100%; border-radius: 2px; background: var(--border-medium); transition: background 200ms;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px; font-size: 11px;">
                  <span id="password-feedback-text" style="color: var(--text-muted);">8+ chars, upper, lower, number, symbol</span>
                  <span id="password-strength-badge" style="font-weight: 600; color: var(--text-muted);">Strength: None</span>
                </div>
              </div>
            </div>

            <!-- Confirm Password -->
            <div class="form-group" style="margin-bottom: var(--space-5);">
              <label class="form-label" for="reg-confirm-password" style="font-size: var(--fs-xs); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 6px; display: block;">
                Confirm Password
              </label>
              <input 
                type="password" 
                id="reg-confirm-password" 
                class="input-control w-full" 
                placeholder="Re-enter your password" 
                autocomplete="new-password"
                required 
                style="height: 40px; font-size: var(--fs-sm); background: var(--bg-darkest); border: 1px solid var(--border-medium); border-radius: var(--radius-md); padding: 0 12px; color: var(--text-primary);"
              />
              <div id="password-match-status" style="font-size: 11px; margin-top: 4px; display: none;"></div>
            </div>

            <!-- Terms agreement -->
            <div class="flex items-center gap-2" style="margin-bottom: var(--space-6); font-size: 12px; color: var(--text-muted);">
              <input type="checkbox" id="reg-terms" checked required style="accent-color: var(--accent-primary);" />
              <label for="reg-terms">I agree to CodePilot's Developer Terms and Privacy Policy</label>
            </div>

            <button 
              type="submit" 
              id="btn-submit-register" 
              class="btn btn-primary w-full" 
              style="height: 42px; font-size: var(--fs-sm); font-weight: 600; justify-content: center; letter-spacing: 0.02em;"
            >
              <span id="btn-reg-text">Create Account</span>
              <span id="btn-reg-spinner" class="hidden" style="margin-left: 8px;">⏳</span>
            </button>
          </form>

          <!-- Footer -->
          <div class="text-center" style="margin-top: var(--space-6); padding-top: var(--space-4); border-top: 1px solid var(--border-subtle); font-size: 13px; color: var(--text-secondary);">
            Already have an account? <a href="#/login" style="color: var(--accent-primary); font-weight: 600; text-decoration: none;">Sign In</a>
          </div>
        </div>
      </div>
    `;
  }

  static afterRender({ router }) {
    const form = document.getElementById('register-form');
    const uInput = document.getElementById('reg-username');
    const nInput = document.getElementById('reg-name');
    const eInput = document.getElementById('reg-email');
    const pInput = document.getElementById('reg-password');
    const cpInput = document.getElementById('reg-confirm-password');
    const toggleBtn = document.getElementById('btn-toggle-reg-password');
    const termsBox = document.getElementById('reg-terms');

    const submitBtn = document.getElementById('btn-submit-register');
    const btnText = document.getElementById('btn-reg-text');
    const btnSpinner = document.getElementById('btn-reg-spinner');

    const serverAlert = document.getElementById('reg-server-alert');
    const serverAlertMsg = document.getElementById('reg-server-alert-msg');
    const errU = document.getElementById('err-reg-username');
    const errE = document.getElementById('err-reg-email');
    const errP = document.getElementById('err-reg-password');
    const matchStatus = document.getElementById('password-match-status');

    const seg1 = document.getElementById('str-seg-1');
    const seg2 = document.getElementById('str-seg-2');
    const seg3 = document.getElementById('str-seg-3');
    const seg4 = document.getElementById('str-seg-4');
    const strBadge = document.getElementById('password-strength-badge');
    const strFeedback = document.getElementById('password-feedback-text');

    if (!form) return;

    if (toggleBtn && pInput) {
      toggleBtn.addEventListener('click', () => {
        if (pInput.type === 'password') {
          pInput.type = 'text';
          toggleBtn.textContent = '🔒';
        } else {
          pInput.type = 'password';
          toggleBtn.textContent = '👁️';
        }
      });
    }

    // Dynamic Password Strength Meter
    const updateStrength = () => {
      const val = pInput?.value || '';
      const str = evaluatePasswordStrength(val);
      const segs = [seg1, seg2, seg3, seg4];

      segs.forEach((seg, idx) => {
        if (!seg) return;
        if (idx < str.score && val.length > 0) {
          seg.style.background = str.color;
        } else {
          seg.style.background = 'var(--border-medium)';
        }
      });

      if (strBadge) {
        strBadge.textContent = `Strength: ${str.label}`;
        strBadge.style.color = str.color;
      }

      if (strFeedback) {
        strFeedback.textContent = str.feedback.join(' • ') || '8+ chars, upper, lower, number, symbol';
      }
    };

    if (pInput) {
      pInput.addEventListener('input', () => {
        updateStrength();
        checkMatch();
      });
    }

    // Dynamic Password Match Check
    const checkMatch = () => {
      if (!matchStatus || !cpInput || !pInput) return;
      const p1 = pInput.value;
      const p2 = cpInput.value;

      if (!p2) {
        matchStatus.style.display = 'none';
        return;
      }

      matchStatus.style.display = 'block';
      if (p1 === p2) {
        matchStatus.textContent = '✓ Passwords match';
        matchStatus.style.color = '#10B981';
      } else {
        matchStatus.textContent = '✗ Passwords do not match';
        matchStatus.style.color = '#f87171';
      }
    };

    if (cpInput) {
      cpInput.addEventListener('input', checkMatch);
    }

    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      // Clear alerts
      serverAlert.classList.add('hidden');
      errU.style.display = 'none';
      errE.style.display = 'none';
      errP.style.display = 'none';

      const username = (uInput?.value || '').trim();
      const displayName = (nInput?.value || '').trim() || username;
      const email = (eInput?.value || '').trim();
      const password = pInput?.value || '';
      const confirmPassword = cpInput?.value || '';

      let hasError = false;

      const uErr = validateUsername(username);
      if (uErr) {
        errU.textContent = uErr;
        errU.style.display = 'block';
        hasError = true;
      }

      const eErr = validateEmail(email);
      if (eErr) {
        errE.textContent = eErr;
        errE.style.display = 'block';
        hasError = true;
      }

      const pErr = validatePassword(password);
      if (pErr) {
        errP.textContent = pErr;
        errP.style.display = 'block';
        hasError = true;
      }

      if (password !== confirmPassword) {
        matchStatus.textContent = 'Passwords do not match.';
        matchStatus.style.color = '#f87171';
        matchStatus.style.display = 'block';
        hasError = true;
      }

      if (termsBox && !termsBox.checked) {
        serverAlertMsg.textContent = 'You must agree to the Developer Terms to continue.';
        serverAlert.classList.remove('hidden');
        hasError = true;
      }

      if (hasError) return;

      submitBtn.disabled = true;
      btnText.textContent = 'Creating account...';
      btnSpinner.classList.remove('hidden');

      try {
        const res = await AuthService.register({
          username,
          displayName,
          email,
          password,
          confirmPassword
        });

        store.set('currentUser', res.user);
        store.set('isAuthenticated', true);

        NotificationService.showToast('Account registered successfully! Welcome to CodePilot.', 'success');
        router.navigate('/dashboard');
      } catch (err) {
        serverAlertMsg.textContent = err.message || 'Registration failed. Please check your details.';
        serverAlert.classList.remove('hidden');
        NotificationService.showToast(err.message || 'Registration failed', 'error');
      } finally {
        submitBtn.disabled = false;
        btnText.textContent = 'Create Account';
        btnSpinner.classList.add('hidden');
      }
    });
  }
}

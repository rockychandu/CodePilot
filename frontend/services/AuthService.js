/**
 * CodePilot Client Authentication Service
 * Manages JWT tokens, refresh tokens, registration, login, logout, password change,
 * email verification, and session state.
 */

const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
  ? 'http://localhost:5000/api/v1'
  : '/api/v1';

export const AuthService = {
  getToken() {
    return localStorage.getItem('codepilot_token') || sessionStorage.getItem('codepilot_token');
  },

  setToken(token, remember = true) {
    if (remember) {
      localStorage.setItem('codepilot_token', token);
    } else {
      sessionStorage.setItem('codepilot_token', token);
    }
  },

  getRefreshToken() {
    return localStorage.getItem('codepilot_refresh_token') || sessionStorage.getItem('codepilot_refresh_token');
  },

  setRefreshToken(token, remember = true) {
    if (remember) {
      localStorage.setItem('codepilot_refresh_token', token);
    } else {
      sessionStorage.setItem('codepilot_refresh_token', token);
    }
  },

  getCurrentUser() {
    try {
      const u = localStorage.getItem('codepilot_user') || sessionStorage.getItem('codepilot_user');
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  },

  setCurrentUser(user, remember = true) {
    const serialized = JSON.stringify(user);
    if (remember) {
      localStorage.setItem('codepilot_user', serialized);
    } else {
      sessionStorage.setItem('codepilot_user', serialized);
    }
  },

  isAuthenticated() {
    return !!this.getToken();
  },

  async login(identifier, password, remember = true) {
    const resp = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identifier, loginIdentifier: identifier, password })
    });
    const data = await resp.json();
    if (!resp.ok || !data.success) {
      throw new Error(data.error || 'Authentication failed. Check your credentials.');
    }
    this.setToken(data.token, remember);
    if (data.refreshToken) {
      this.setRefreshToken(data.refreshToken, remember);
    }
    this.setCurrentUser(data.user, remember);
    return data;
  },

  async register(arg1, email, password, confirmPassword = null, displayName = '') {
    let un = arg1;
    let em = email;
    let pw = password;
    let cp = confirmPassword;
    let dn = displayName;

    if (typeof arg1 === 'object' && arg1 !== null) {
      un = arg1.username;
      em = arg1.email;
      pw = arg1.password;
      cp = arg1.confirmPassword || arg1.confirm_password;
      dn = arg1.displayName || arg1.name || arg1.username;
    }

    const resp = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: un,
        email: em,
        password: pw,
        confirmPassword: cp,
        displayName: dn
      })
    });
    const data = await resp.json();
    if (!resp.ok || !data.success) {
      throw new Error(data.error || 'Registration failed.');
    }
    this.setToken(data.token, true);
    if (data.refreshToken) {
      this.setRefreshToken(data.refreshToken, true);
    }
    this.setCurrentUser(data.user, true);
    return data;
  },

  async logout() {
    try {
      const token = this.getToken();
      if (token) {
        await fetch(`${API_BASE}/auth/logout`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        });
      }
    } catch {}
    this.clearAuth();
  },

  async logoutAll() {
    const token = this.getToken();
    if (token) {
      try {
        await fetch(`${API_BASE}/auth/logout-all`, {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` }
        });
      } catch {}
    }
    this.clearAuth();
  },

  clearAuth() {
    localStorage.removeItem('codepilot_token');
    sessionStorage.removeItem('codepilot_token');
    localStorage.removeItem('codepilot_refresh_token');
    sessionStorage.removeItem('codepilot_refresh_token');
    localStorage.removeItem('codepilot_user');
    sessionStorage.removeItem('codepilot_user');
  },

  async fetchMe() {
    const token = this.getToken();
    if (!token) return null;
    try {
      const resp = await fetch(`${API_BASE}/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (resp.ok) {
        const data = await resp.json();
        if (data.success && data.user) {
          this.setCurrentUser(data.user);
          return data.user;
        }
      }
    } catch {}
    return this.getCurrentUser();
  },

  async fetchProfile() {
    return this.fetchMe();
  },

  async changePassword(currentPassword, newPassword) {
    const token = this.getToken();
    if (!token) throw new Error('Not authenticated.');
    const resp = await fetch(`${API_BASE}/auth/change-password`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ currentPassword, newPassword })
    });
    const data = await resp.json();
    if (!resp.ok || !data.success) {
      throw new Error(data.error || 'Failed to update password.');
    }
    return data;
  },

  async requestPasswordReset(email) {
    const resp = await fetch(`${API_BASE}/auth/forgot-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    const data = await resp.json();
    return data;
  },

  async resetPassword(token, password) {
    const resp = await fetch(`${API_BASE}/auth/reset-password`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, password })
    });
    const data = await resp.json();
    if (!resp.ok || !data.success) {
      throw new Error(data.error || 'Password reset failed.');
    }
    return data;
  },

  async verifyEmail(token) {
    const resp = await fetch(`${API_BASE}/auth/verify-email`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token })
    });
    const data = await resp.json();
    if (!resp.ok || !data.success) {
      throw new Error(data.error || 'Email verification failed.');
    }
    return data;
  },

  async resendVerification(email) {
    const resp = await fetch(`${API_BASE}/auth/resend-verification`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email })
    });
    return await resp.json();
  },

  async fetchHistory(params = {}) {
    const token = this.getToken();
    if (!token) return { items: [], total: 0 };
    try {
      const query = new URLSearchParams(params).toString();
      const resp = await fetch(`${API_BASE}/history?${query}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (resp.ok) {
        return await resp.json();
      }
    } catch {}
    return { items: [], total: 0 };
  }
};

export default AuthService;

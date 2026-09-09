/**
 * CodePilot Client Authentication Service
 * Manages JWT tokens, registration, login, logout, and profile sync with /api/v1/auth
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

  async login(identifier, password, remember = true) {
    try {
      const resp = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ loginIdentifier: identifier, password })
      });
      const data = await resp.json();
      if (!resp.ok) {
        throw new Error(data.error || 'Login failed.');
      }
      this.setToken(data.token, remember);
      this.setCurrentUser(data.user, remember);
      return data;
    } catch (err) {
      // Fallback local mock user for static file hosting
      const demoUser = {
        id: 1,
        username: identifier || 'developer',
        email: `${identifier || 'dev'}@codepilot.dev`,
        role: 'USER',
        profile: {
          displayName: identifier || 'Developer',
          avatarUrl: 'frontend/assets/logo.svg',
          bio: 'CodePilot Developer',
          primaryLanguage: 'Python',
          xp: 1250,
          level: 4,
          rankTitle: 'Junior Coder',
          streakDays: 5,
          problemsSolved: 12,
          contestRating: 1450
        }
      };
      this.setToken('demo-token-mock', remember);
      this.setCurrentUser(demoUser, remember);
      return { token: 'demo-token-mock', user: demoUser };
    }
  },

  async register(username, email, password, displayName = '') {
    try {
      const resp = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, displayName })
      });
      const data = await resp.json();
      if (!resp.ok) {
        throw new Error(data.error || 'Registration failed.');
      }
      this.setToken(data.token, true);
      this.setCurrentUser(data.user, true);
      return data;
    } catch (err) {
      throw err;
    }
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
    localStorage.removeItem('codepilot_token');
    sessionStorage.removeItem('codepilot_token');
    localStorage.removeItem('codepilot_user');
    sessionStorage.removeItem('codepilot_user');
  },

  async fetchProfile() {
    const token = this.getToken();
    if (!token) return null;
    try {
      const resp = await fetch(`${API_BASE}/profile`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (resp.ok) {
        const user = await resp.json();
        this.setCurrentUser(user);
        return user;
      }
    } catch {}
    return this.getCurrentUser();
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

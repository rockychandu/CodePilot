/* Central Application Reactive Store */
import { storage } from '../utils/storage.js';

class Store {
  constructor() {
    this.listeners = new Map();

    // Initial state with local storage hydration
    this.state = {
      currentUser: storage.get('user', {
        id: 'u_demo123',
        name: 'Alex Developer',
        username: 'alex_dev',
        email: 'alex.developer@codepilot.io',
        role: 'student', // 'student' | 'teacher' | 'admin'
        avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
        rating: 1845,
        xp: 4250,
        level: 12,
        streak: 7,
        solvedCount: 142
      }),

      isAuthenticated: storage.get('isAuthenticated', true),

      theme: storage.get('theme', 'dark'),

      editorSettings: storage.get('editorSettings', {
        fontSize: 14,
        wordWrap: true,
        theme: 'vs-dark',
        selectedLanguage: 'python',
        activeFile: 'main.py'
      }),

      bookmarks: storage.get('bookmarks', ['prob_1', 'prob_3']),

      notifications: storage.get('notifications', [
        { id: 'notif_1', title: 'Weekly Contest 42', message: 'Contest starts in 2 hours!', read: false, date: '2026-09-09' },
        { id: 'notif_2', title: 'Achievement Unlocked', message: 'You earned "7-Day Streak" badge!', read: false, date: '2026-09-08' }
      ]),

      terminalHistory: storage.get('terminalHistory', [
        'codepilot --version',
        'python main.py'
      ])
    };

    // Apply stored theme on load
    document.documentElement.setAttribute('data-theme', this.state.theme);
  }

  get(key) {
    return this.state[key];
  }

  set(key, value) {
    this.state[key] = value;
    storage.set(key, value);
    this.notify(key, value);
  }

  update(key, fn) {
    const newValue = fn(this.state[key]);
    this.set(key, newValue);
  }

  subscribe(key, callback) {
    if (!this.listeners.has(key)) {
      this.listeners.set(key, new Set());
    }
    this.listeners.get(key).add(callback);
    return () => this.listeners.get(key).delete(callback);
  }

  notify(key, value) {
    if (this.listeners.has(key)) {
      this.listeners.get(key).forEach(cb => cb(value, this.state));
    }
  }
}

export const store = new Store();

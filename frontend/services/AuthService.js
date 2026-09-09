/* Auth Service Abstraction Layer */
import { store } from '../state/store.js';
import { validateEmail, validatePassword, validateUsername } from '../utils/validators.js';
import { sleep } from '../utils/helpers.js';

export class AuthService {
  static async login(email, password) {
    await sleep(400); // Simulate network latency

    const emailErr = validateEmail(email);
    if (emailErr) throw new Error(emailErr);

    const passErr = validatePassword(password);
    if (passErr) throw new Error(passErr);

    // Mock Login Success
    const user = {
      id: 'u_demo123',
      name: 'Alex Developer',
      username: email.split('@')[0],
      email: email,
      role: email.includes('admin') ? 'admin' : (email.includes('teacher') ? 'teacher' : 'student'),
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
      rating: 1845,
      xp: 4250,
      level: 12,
      streak: 7,
      solvedCount: 142
    };

    store.set('currentUser', user);
    store.set('isAuthenticated', true);

    return { success: true, user };
  }

  static async register({ name, username, email, password, confirmPassword }) {
    await sleep(500);

    if (!name || !name.trim()) throw new Error('Full name is required.');
    
    const userErr = validateUsername(username);
    if (userErr) throw new Error(userErr);

    const emailErr = validateEmail(email);
    if (emailErr) throw new Error(emailErr);

    const passErr = validatePassword(password);
    if (passErr) throw new Error(passErr);

    if (password !== confirmPassword) throw new Error('Passwords do not match.');

    const user = {
      id: `u_${Date.now()}`,
      name: name.trim(),
      username: username.trim(),
      email: email.trim(),
      role: 'student',
      avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
      rating: 1500,
      xp: 100,
      level: 1,
      streak: 1,
      solvedCount: 0
    };

    store.set('currentUser', user);
    store.set('isAuthenticated', true);

    return { success: true, user };
  }

  static async logout() {
    await sleep(200);
    store.set('isAuthenticated', false);
    store.set('currentUser', null);
  }

  static async resetPassword(email) {
    await sleep(400);
    const emailErr = validateEmail(email);
    if (emailErr) throw new Error(emailErr);
    return { success: true, message: 'Password reset simulation completed.' };
  }
}

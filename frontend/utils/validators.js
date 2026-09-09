/* Input & Auth Validation Utilities */

export function validateEmail(email) {
  if (!email || !email.trim()) {
    return 'Please enter your email.';
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email.trim())) {
    return 'Enter a valid email address.';
  }
  return null;
}

export function validateUsername(username) {
  if (!username || !username.trim()) {
    return 'Username is required.';
  }
  if (username.trim().length < 3) {
    return 'Username must be at least 3 characters.';
  }
  if (!/^[a-zA-Z0-9_]+$/.test(username.trim())) {
    return 'Username can only contain letters, numbers, and underscores.';
  }
  return null;
}

export function validatePassword(password) {
  if (!password) {
    return 'Please enter your password.';
  }
  if (password.length < 6) {
    return 'Password must be at least 6 characters.';
  }
  return null;
}

export function evaluatePasswordStrength(password) {
  if (!password) return { label: 'Weak', score: 0, color: '#EF4444' };
  let score = 0;
  if (password.length >= 8) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/[0-9]/.test(password)) score++;
  if (/[^A-Za-z0-9]/.test(password)) score++;

  if (score <= 1) return { label: 'Weak', score: 1, color: '#EF4444' };
  if (score === 2) return { label: 'Fair', score: 2, color: '#F59E0B' };
  if (score === 3) return { label: 'Good', score: 3, color: '#3B82F6' };
  return { label: 'Strong', score: 4, color: '#10B981' };
}

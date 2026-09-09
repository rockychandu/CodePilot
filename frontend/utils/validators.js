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
  const trimmed = username.trim();
  if (trimmed.length < 3 || trimmed.length > 30) {
    return 'Username must be between 3 and 30 characters.';
  }
  if (!/^[a-zA-Z0-9_]+$/.test(trimmed)) {
    return 'Username can only contain letters, numbers, and underscores.';
  }
  return null;
}

export function validatePassword(password) {
  if (!password) {
    return 'Please enter your password.';
  }
  if (password.length < 8) {
    return 'Password must be at least 8 characters long.';
  }
  if (!/[A-Z]/.test(password)) {
    return 'Password must contain at least one uppercase letter.';
  }
  if (!/[a-z]/.test(password)) {
    return 'Password must contain at least one lowercase letter.';
  }
  if (!/[0-9]/.test(password)) {
    return 'Password must contain at least one number.';
  }
  if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`]/.test(password)) {
    return 'Password must contain at least one special character.';
  }
  return null;
}

export function evaluatePasswordStrength(password) {
  if (!password) {
    return { label: 'None', score: 0, color: 'var(--border-medium)', isAcceptable: false, feedback: ['Enter a password'] };
  }
  
  let score = 0;
  const feedback = [];

  if (password.length >= 8) score++;
  else feedback.push('At least 8 characters');

  if (/[A-Z]/.test(password) && /[a-z]/.test(password)) score++;
  else feedback.push('Upper and lowercase letters');

  if (/[0-9]/.test(password)) score++;
  else feedback.push('At least one digit');

  if (/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?/~`]/.test(password)) score++;
  else feedback.push('At least one symbol');

  if (score <= 1) {
    return { label: 'Weak', score: 1, color: '#EF4444', isAcceptable: false, feedback };
  }
  if (score === 2) {
    return { label: 'Fair', score: 2, color: '#F59E0B', isAcceptable: false, feedback };
  }
  if (score === 3) {
    return { label: 'Good', score: 3, color: '#3B82F6', isAcceptable: true, feedback };
  }
  return { label: 'Strong', score: 4, color: '#10B981', isAcceptable: true, feedback: ['Password meets security standards'] };
}

export function validatePasswordMatch(p1, p2) {
  if (!p2) return 'Please confirm your password.';
  if (p1 !== p2) return 'Passwords do not match.';
  return null;
}

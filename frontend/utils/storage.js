/* Storage Utility Module */
const STORAGE_PREFIX = 'codepilot_';

export const storage = {
  get(key, defaultValue = null) {
    try {
      const item = localStorage.getItem(STORAGE_PREFIX + key);
      return item ? JSON.parse(item) : defaultValue;
    } catch (err) {
      console.warn(`[Storage] Failed to read ${key}`, err);
      return defaultValue;
    }
  },

  set(key, value) {
    try {
      localStorage.setItem(STORAGE_PREFIX + key, JSON.stringify(value));
      return true;
    } catch (err) {
      console.warn(`[Storage] Failed to write ${key}`, err);
      return false;
    }
  },

  remove(key) {
    try {
      localStorage.removeItem(STORAGE_PREFIX + key);
    } catch (err) {
      console.warn(`[Storage] Failed to remove ${key}`, err);
    }
  },

  clear() {
    try {
      Object.keys(localStorage)
        .filter(k => k.startsWith(STORAGE_PREFIX))
        .forEach(k => localStorage.removeItem(k));
    } catch (err) {
      console.warn(`[Storage] Failed to clear storage`, err);
    }
  }
};

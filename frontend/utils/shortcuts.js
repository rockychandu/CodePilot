/* Global Shortcuts & Keybindings Handler */

const shortcuts = new Map();

export function registerShortcut(keyCombo, callback) {
  shortcuts.set(keyCombo.toLowerCase(), callback);
}

export function initShortcuts() {
  document.addEventListener('keydown', (e) => {
    const isCmdOrCtrl = e.metaKey || e.ctrlKey;
    let keyCombo = '';

    if (isCmdOrCtrl) keyCombo += 'ctrl+';
    if (e.shiftKey) keyCombo += 'shift+';
    if (e.altKey) keyCombo += 'alt+';
    keyCombo += e.key.toLowerCase();

    if (shortcuts.has(keyCombo)) {
      e.preventDefault();
      shortcuts.get(keyCombo)(e);
    }
  });
}

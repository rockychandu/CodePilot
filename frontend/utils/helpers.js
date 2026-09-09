/* Helpers and Formatting Utilities */

export function generateId(prefix = 'id') {
  return `${prefix}_${Math.random().toString(36).substring(2, 9)}`;
}

export function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
}

export function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

export function formatNumber(num) {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'k';
  return num.toString();
}

export function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/* Light Syntax Highlighter Tokenizer for Code Preview */
export function highlightCode(code, language = 'python') {
  if (!code) return '';
  let escaped = escapeHtml(code);

  const keywords = {
    python: ['def', 'return', 'import', 'from', 'class', 'if', 'else', 'elif', 'for', 'while', 'in', 'try', 'except', 'with', 'as', 'lambda', 'True', 'False', 'None', 'print'],
    javascript: ['function', 'const', 'let', 'var', 'return', 'if', 'else', 'for', 'while', 'import', 'export', 'default', 'async', 'await', 'class', 'try', 'catch', 'true', 'false', 'null', 'console'],
    cpp: ['#include', 'using', 'namespace', 'int', 'void', 'char', 'float', 'double', 'class', 'struct', 'public', 'private', 'return', 'if', 'else', 'for', 'while', 'cout', 'cin', 'endl'],
    java: ['public', 'class', 'static', 'void', 'main', 'String', 'int', 'boolean', 'if', 'else', 'for', 'while', 'return', 'import', 'new', 'System', 'out', 'println']
  };

  const kwList = keywords[language] || keywords.python;
  const kwRegex = new RegExp(`\\b(${kwList.join('|')})\\b`, 'g');

  escaped = escaped
    .replace(/"(.*?)"/g, '<span style="color: #A5D6FF;">"$1"</span>')
    .replace(/'(.*?)'/g, "<span style=\"color: #A5D6FF;\">'$1'</span>")
    .replace(/\b(\d+)\b/g, '<span style="color: #79C0FF;">$1</span>')
    .replace(/(#|\/\/).*/g, '<span style="color: #8B949E; font-style: italic;">$&</span>')
    .replace(kwRegex, '<span style="color: #FF7B72; font-weight: 600;">$1</span>');

  return escaped;
}

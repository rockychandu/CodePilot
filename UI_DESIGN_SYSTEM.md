# CodePilot Design System & Visual Language Specification

## Core Design Philosophy
CodePilot's user interface is crafted specifically for software engineers engaged in sustained, high-focus coding sessions. It intentionally avoids AI-generated clichés such as oversized glowing gradients, arbitrary glassmorphic blurs, and neon card borders in favor of a restrained, information-dense, and highly functional IDE layout.

---

## 🎨 Color Palette & Tokens

### Base & Background (Dark Zinc)
| Token | Hex Value | Usage |
| :--- | :--- | :--- |
| `--bg-darkest` | `#09090b` | Base background, line numbers, terminal background |
| `--bg-base` | `#121215` | Page background, workspace canvas |
| `--bg-surface` | `#18181b` | Cards, panels, sidebars, navbar |
| `--bg-surface-hover` | `#27272a` | Interactive hover states |
| `--bg-surface-active` | `#3f3f46` | Active tabs, pressed buttons |
| `--bg-code` | `#0d0e11` | Editor canvas, syntax buffer |

### Borders
| Token | Hex Value | Usage |
| :--- | :--- | :--- |
| `--border-subtle` | `#27272a` | Default 1px component borders |
| `--border-medium` | `#3f3f46` | Input borders, card hover borders |
| `--border-strong` | `#52525b` | Active borders, focused dividers |
| `--border-accent` | `#3b82f6` | Focus outlines, active tab indicators |

### Accents & Status
| Token | Hex Value | Usage |
| :--- | :--- | :--- |
| `--accent-primary` | `#3b82f6` | Primary action buttons, selection indicators |
| `--accent-emerald` | `#10b981` | Accepted status, passing tests, online indicators |
| `--accent-amber` | `#f59e0b` | Warnings, medium difficulty, pending states |
| `--accent-rose` | `#ef4444` | Runtime errors, wrong answer, failed tests |

---

## 🔤 Typography

- **UI & Controls Font**: `Inter`, sans-serif (Weights: 400 Regular, 500 Medium, 600 SemiBold, 700 Bold)
- **Code & Numbers Font**: `JetBrains Mono`, `Fira Code`, monospace (Weights: 400 Regular, 500 Medium, 700 Bold)

### Scale
- `--fs-2xs`: `11px` (Line numbers, timestamp badges, status pills)
- `--fs-xs`: `12px` (Toolbar buttons, table headers, breadcrumbs)
- `--fs-sm`: `13px` (Code editor text, standard inputs, table cells)
- `--fs-base`: `14px` (Card titles, modal headings, primary links)
- `--fs-lg`: `16px` (Subheaders, prominent metrics)
- `--fs-xl`: `18px` (Page titles)

---

## 📐 Component Patterns

### 1. 3-Column IDE Layout
- **Left**: File Explorer with tree hierarchy and file status indicators.
- **Center**: Tabbed code editor with line numbers, minimap, and status bar.
- **Right**: Pilot AI Assistant panel for AST code reviews, complexity breakdown, and test synthesis.
- **Bottom**: Resizable dock with Console Output, Custom Stdin input, and Terminal.

### 2. High-Density Tables
- Clear 1px dividers, uppercase subheadings, monospaced timestamp and runtime columns, subtle zebra hover.

### 3. Modals & Command Palette
- Dark zinc backdrop with sharp corners (`border-radius: 4px-6px`), keyboard navigable (`Escape` to close, `Ctrl+K` to trigger global search).

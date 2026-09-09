/* Custom PDF Reader Viewer UI Component */

export class PdfViewerComponent {
  static render({ docTitle = 'Python Architecture Guide.pdf' }) {
    return `
      <div class="pdf-viewer-layout w-full">
        <!-- Sidebar TOC & Thumbnails -->
        <div class="pdf-sidebar">
          <div style="font-size: var(--fs-xs); font-weight:700; color: var(--text-muted); text-transform: uppercase; margin-bottom: var(--space-4);">Table of Contents</div>
          <div style="font-size: var(--fs-sm); font-weight:600; color: var(--accent-cyan); margin-bottom: var(--space-2); cursor: pointer;">1. Introduction & Setup</div>
          <div style="font-size: var(--fs-sm); color: var(--text-secondary); margin-bottom: var(--space-2); cursor: pointer;">2. Memory & Reference Model</div>
          <div style="font-size: var(--fs-sm); color: var(--text-secondary); margin-bottom: var(--space-2); cursor: pointer;">3. Object Oriented Class Design</div>
          <div style="font-size: var(--fs-sm); color: var(--text-secondary); margin-bottom: var(--space-2); cursor: pointer;">4. Async IO & Concurrency</div>
        </div>

        <!-- Document Main Canvas Viewport -->
        <div class="pdf-viewport">
          <div class="flex items-center justify-between w-full" style="max-width: 650px; margin-bottom: var(--space-4); background: var(--bg-surface); padding: 8px 16px; border-radius: var(--radius-md);">
            <div style="font-size: var(--fs-sm); font-weight:600;">${docTitle}</div>
            <div class="flex items-center gap-2">
              <button id="pdf-zoom-out" class="btn btn-secondary btn-sm">-</button>
              <span id="pdf-zoom-level" style="font-size: var(--fs-xs);">100%</span>
              <button id="pdf-zoom-in" class="btn btn-secondary btn-sm">+</button>
            </div>
          </div>

          <div class="pdf-page-canvas">
            <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 12px; border-bottom: 1px solid #CBD5E1; padding-bottom: 8px;">Chapter 1: Python Architecture Overview</h2>
            <p style="margin-bottom: 12px; line-height: 1.6;">Python is a high-level dynamically typed programming language. Memory allocation is managed automatically by PyObject reference counting and a generational garbage collector.</p>
            <p style="margin-bottom: 12px; line-height: 1.6;">Key concepts in Python memory architecture:</p>
            <ul style="margin-left: 20px; margin-bottom: 16px; line-height: 1.6;">
              <li><strong>Reference Counting:</strong> Increments when objects are bound to names.</li>
              <li><strong>Generational GC:</strong> Tracks container objects (lists, dicts, tuples) to resolve circular references.</li>
            </ul>
            <div style="background: #F1F5F9; border-left: 4px solid #0284C7; padding: 12px; font-family: monospace; font-size: 13px;">
              import sys<br>
              x = [1, 2, 3]<br>
              print(sys.getrefcount(x)) # Output: 2
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

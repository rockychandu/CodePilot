/* Multi-Language Execution Studio Hub Page */
import { LANGUAGE_TEMPLATES } from '../components/ide-editor.js';

export class LanguagesPage {
  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Multi-Language Execution Studio</h1>
            <p class="text-secondary">Select any language below to write, edit, and execute code instantly in the browser workbench.</p>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-6">
          <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                <span style="font-size: 32px;">🐍</span>
                <span class="badge-tag badge-easy">Scripting & AI</span>
              </div>
              <h3 style="font-size: var(--fs-lg); margin-bottom: 8px;">Python 3</h3>
              <p class="text-muted" style="font-size: var(--fs-sm); line-height: 1.5; margin-bottom: 16px;">Write clean Python 3.12 scripts, data algorithms, and logic modules.</p>
            </div>
            <a href="#/ide?lang=python" class="btn btn-primary w-full">▶ Launch Python Workbench</a>
          </div>

          <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                <span style="font-size: 32px;">⚡</span>
                <span class="badge-tag badge-easy">Systems</span>
              </div>
              <h3 style="font-size: var(--fs-lg); margin-bottom: 8px;">C (GCC)</h3>
              <p class="text-muted" style="font-size: var(--fs-sm); line-height: 1.5; margin-bottom: 16px;">High performance C language memory management, pointers, and structs.</p>
            </div>
            <a href="#/ide?lang=c" class="btn btn-primary w-full">▶ Launch C Workbench</a>
          </div>

          <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                <span style="font-size: 32px;">🚀</span>
                <span class="badge-tag badge-easy">Performance</span>
              </div>
              <h3 style="font-size: var(--fs-lg); margin-bottom: 8px;">C++ 20</h3>
              <p class="text-muted" style="font-size: var(--fs-sm); line-height: 1.5; margin-bottom: 16px;">Competitive programming STL containers, vector operations, and algorithms.</p>
            </div>
            <a href="#/ide?lang=cpp" class="btn btn-primary w-full">▶ Launch C++ Workbench</a>
          </div>

          <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                <span style="font-size: 32px;">☕</span>
                <span class="badge-tag badge-easy">Enterprise</span>
              </div>
              <h3 style="font-size: var(--fs-lg); margin-bottom: 8px;">Java 21</h3>
              <p class="text-muted" style="font-size: var(--fs-sm); line-height: 1.5; margin-bottom: 16px;">Object-oriented class structures, collections, and Java virtual machine execution.</p>
            </div>
            <a href="#/ide?lang=java" class="btn btn-primary w-full">▶ Launch Java Workbench</a>
          </div>

          <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                <span style="font-size: 32px;">🟨</span>
                <span class="badge-tag badge-easy">Web & Node</span>
              </div>
              <h3 style="font-size: var(--fs-lg); margin-bottom: 8px;">JavaScript (Node.js)</h3>
              <p class="text-muted" style="font-size: var(--fs-sm); line-height: 1.5; margin-bottom: 16px;">Modern ES6+ JavaScript functions, closures, and async logic.</p>
            </div>
            <a href="#/ide?lang=javascript" class="btn btn-primary w-full">▶ Launch JS Workbench</a>
          </div>

          <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                <span style="font-size: 32px;">📊</span>
                <span class="badge-tag badge-easy">Data & Stats</span>
              </div>
              <h3 style="font-size: var(--fs-lg); margin-bottom: 8px;">R Language</h3>
              <p class="text-muted" style="font-size: var(--fs-sm); line-height: 1.5; margin-bottom: 16px;">Statistical computing, vector calculations, standard deviation, and data frames.</p>
            </div>
            <a href="#/ide?lang=r" class="btn btn-primary w-full">▶ Launch R Workbench</a>
          </div>

          <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
              <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                <span style="font-size: 32px;">🗄️</span>
                <span class="badge-tag badge-easy">Database</span>
              </div>
              <h3 style="font-size: var(--fs-lg); margin-bottom: 8px;">SQL Database</h3>
              <p class="text-muted" style="font-size: var(--fs-sm); line-height: 1.5; margin-bottom: 16px;">Write relational queries (`CREATE TABLE`, `INSERT`, `SELECT`, `WHERE`).</p>
            </div>
            <a href="#/ide?lang=sql" class="btn btn-primary w-full">▶ Launch SQL Workbench</a>
          </div>
        </div>
      </div>
    `;
  }
}

/* Landing Page View Module */

export class LandingPage {
  static async render() {
    return `
      <div class="w-full">
        <!-- Hero Section -->
        <section class="hero-section">
          <div class="container">
            <div class="hero-content">
              <div class="hero-badge">⚡ Multi-Language Code Execution Studio</div>
              <h1 class="hero-title">Write, compile, and execute code in 7 programming languages.</h1>
              <p class="hero-subtitle">
                Write code in Python, C, C++, Java, JavaScript, R, and SQL with instant execution output, syntax highlighting, and custom stdin input.
              </p>
              <div class="hero-cta-group">
                <a href="#/languages" class="btn btn-primary btn-lg">🚀 Launch Languages Studio</a>
                <a href="#/ide" class="btn btn-secondary btn-lg">💻 Open IDE Studio</a>
              </div>
            </div>

            <!-- Animated IDE Preview Box -->
            <div class="hero-ide-preview">
              <div class="ide-toolbar">
                <div class="flex items-center gap-2">
                  <span class="terminal-dot dot-red"></span>
                  <span class="terminal-dot dot-yellow"></span>
                  <span class="terminal-dot dot-green"></span>
                  <span style="font-size: var(--fs-xs); color: var(--text-muted); margin-left: 8px;">CodePilot Multi-Lang Workbench</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="output-status-pill status-accepted">🐍 Python • ⚡ C • 🚀 C++ • ☕ Java • 🟨 JS • 📊 R • 🗄️ SQL</span>
                </div>
              </div>
              <div style="padding: 24px; font-family: var(--font-mono); font-size: 14px; background: #030712; color: #E2E8F0; line-height: 1.6;">
                <span style="color: #FF7B72;">def</span> <span style="color: #D2A8FF;">execute_multi_language</span>():<br>
                &nbsp;&nbsp;&nbsp;&nbsp;languages = [<span style="color: #A5D6FF;">"Python"</span>, <span style="color: #A5D6FF;">"C"</span>, <span style="color: #A5D6FF;">"C++"</span>, <span style="color: #A5D6FF;">"Java"</span>, <span style="color: #A5D6FF;">"JavaScript"</span>, <span style="color: #A5D6FF;">"R"</span>, <span style="color: #A5D6FF;">"SQL"</span>]<br>
                &nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #FF7B72;">for</span> lang <span style="color: #FF7B72;">in</span> languages:<br>
                &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #79C0FF;">print</span>(f<span style="color: #A5D6FF;">"Ready to execute code in {lang}!"</span>)<br><br>
                execute_multi_language()
              </div>
            </div>
          </div>
        </section>

        <!-- Languages Cards Section -->
        <section class="features-section">
          <div class="container">
            <div class="section-header">
              <h2>Select Your Programming Language</h2>
              <p class="text-secondary">Click any language to launch its dedicated code editor and execution worker.</p>
            </div>

            <div class="grid grid-cols-4 gap-6">
              <a href="#/ide?lang=python" class="feature-card text-center" style="display: block;">
                <div style="font-size: 40px; margin-bottom: 12px;">🐍</div>
                <h3>Python 3</h3>
                <p class="text-muted" style="font-size: var(--fs-xs); margin-top: 6px;">Scripting, Algorithms, AST Data Structures</p>
              </a>

              <a href="#/ide?lang=c" class="feature-card text-center" style="display: block;">
                <div style="font-size: 40px; margin-bottom: 12px;">⚡</div>
                <h3>C (GCC)</h3>
                <p class="text-muted" style="font-size: var(--fs-xs); margin-top: 6px;">Pointers, Memory Allocation, Systems</p>
              </a>

              <a href="#/ide?lang=cpp" class="feature-card text-center" style="display: block;">
                <div style="font-size: 40px; margin-bottom: 12px;">🚀</div>
                <h3>C++ 20</h3>
                <p class="text-muted" style="font-size: var(--fs-xs); margin-top: 6px;">Vector STL, High Speed Execution</p>
              </a>

              <a href="#/ide?lang=java" class="feature-card text-center" style="display: block;">
                <div style="font-size: 40px; margin-bottom: 12px;">☕</div>
                <h3>Java 21</h3>
                <p class="text-muted" style="font-size: var(--fs-xs); margin-top: 6px;">JVM Classes, Collections, Streams</p>
              </a>

              <a href="#/ide?lang=javascript" class="feature-card text-center" style="display: block;">
                <div style="font-size: 40px; margin-bottom: 12px;">🟨</div>
                <h3>JavaScript</h3>
                <p class="text-muted" style="font-size: var(--fs-xs); margin-top: 6px;">Node.js runtime, Closures, Async</p>
              </a>

              <a href="#/ide?lang=r" class="feature-card text-center" style="display: block;">
                <div style="font-size: 40px; margin-bottom: 12px;">📊</div>
                <h3>R Language</h3>
                <p class="text-muted" style="font-size: var(--fs-xs); margin-top: 6px;">Data Science, Statistics, Data Frames</p>
              </a>

              <a href="#/ide?lang=sql" class="feature-card text-center" style="display: block;">
                <div style="font-size: 40px; margin-bottom: 12px;">🗄️</div>
                <h3>SQL Database</h3>
                <p class="text-muted" style="font-size: var(--fs-xs); margin-top: 6px;">Relational Queries, Tables, Joins</p>
              </a>
            </div>
          </div>
        </section>
      </div>
    `;
  }
}

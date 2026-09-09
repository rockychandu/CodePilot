/* Interactive SVG Skill Tree Component */

export class SkillTreeComponent {
  static render() {
    return `
      <div class="skill-tree-canvas flex items-center justify-center">
        <svg width="100%" height="100%" viewBox="0 0 800 450" xmlns="http://www.w3.org/2000/svg">
          <!-- Connection Lines -->
          <line x1="150" y1="225" x2="300" y2="120" stroke="#38BDF8" stroke-width="4" stroke-dasharray="6,6" />
          <line x1="150" y1="225" x2="300" y2="330" stroke="#38BDF8" stroke-width="4" />
          <line x1="300" y1="120" x2="500" y2="120" stroke="#818CF8" stroke-width="4" />
          <line x1="300" y1="330" x2="500" y2="330" stroke="#10B981" stroke-width="4" />
          <line x1="500" y1="120" x2="680" y2="225" stroke="#F59E0B" stroke-width="4" stroke-dasharray="6,6" />
          <line x1="500" y1="330" x2="680" y2="225" stroke="#F59E0B" stroke-width="4" />

          <!-- Root Node: Python Basics (Completed) -->
          <g class="skill-node" transform="translate(150, 225)">
            <circle r="36" fill="#0284C7" stroke="#38BDF8" stroke-width="6" />
            <text text-anchor="middle" dy="5" fill="#FFF" font-weight="bold" font-size="14">Python 101</text>
            <text text-anchor="middle" dy="55" fill="#38BDF8" font-size="12">✓ Completed</text>
          </g>

          <!-- Branch 1: DSA (Unlocked) -->
          <g class="skill-node" transform="translate(300, 120)">
            <circle r="32" fill="#4F46E5" stroke="#818CF8" stroke-width="4" />
            <text text-anchor="middle" dy="5" fill="#FFF" font-weight="bold" font-size="13">DSA</text>
            <text text-anchor="middle" dy="50" fill="#818CF8" font-size="12">In Progress</text>
          </g>

          <!-- Branch 2: Web APIs (Completed) -->
          <g class="skill-node" transform="translate(300, 330)">
            <circle r="32" fill="#059669" stroke="#10B981" stroke-width="4" />
            <text text-anchor="middle" dy="5" fill="#FFF" font-weight="bold" font-size="13">REST APIs</text>
            <text text-anchor="middle" dy="50" fill="#10B981" font-size="12">✓ Mastered</text>
          </g>

          <!-- Advanced 1: Algorithms -->
          <g class="skill-node" transform="translate(500, 120)">
            <circle r="32" fill="#1E293B" stroke="#475569" stroke-width="4" />
            <text text-anchor="middle" dy="5" fill="#94A3B8" font-weight="bold" font-size="13">Advanced Graph</text>
            <text text-anchor="middle" dy="50" fill="#64748B" font-size="12">🔒 Locked</text>
          </g>

          <!-- Advanced 2: System Design -->
          <g class="skill-node" transform="translate(500, 330)">
            <circle r="32" fill="#059669" stroke="#10B981" stroke-width="4" />
            <text text-anchor="middle" dy="5" fill="#FFF" font-weight="bold" font-size="13">System Design</text>
            <text text-anchor="middle" dy="50" fill="#10B981" font-size="12">✓ Mastered</text>
          </g>

          <!-- Master Node: AI/ML Engineering -->
          <g class="skill-node" transform="translate(680, 225)">
            <circle r="40" fill="#D97706" stroke="#F59E0B" stroke-width="6" />
            <text text-anchor="middle" dy="5" fill="#FFF" font-weight="bold" font-size="14">AI Master</text>
            <text text-anchor="middle" dy="60" fill="#F59E0B" font-size="12">⭐ Next Goal</text>
          </g>
        </svg>
      </div>
    `;
  }
}

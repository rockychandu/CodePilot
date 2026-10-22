/* Professional Developer Learning & Curriculum Page */
import { CourseService } from '../../services/CourseService.js';

export class CourseListPage {
  static async render() {
    let courses = [];
    try {
      courses = await CourseService.getCourses();
    } catch (e) {
      courses = [];
    }

    if (!courses || courses.length === 0) {
      courses = [
        {
          id: 1,
          slug: 'python-mastery-2026',
          title: 'Modern Python 3.12+ Systems & Architecture',
          category: 'Systems & Backend',
          difficulty: 'Intermediate',
          description: 'Deep-dive into metaprogramming, AST parsing, asynchronous event loops, C-extensions, and production design patterns.',
          estimatedHours: 14.5,
          lessonsCount: 18,
          progress: 35
        },
        {
          id: 2,
          slug: 'data-structures-pro',
          title: 'Advanced Data Structures & Graph Algorithms',
          category: 'Algorithms',
          difficulty: 'Advanced',
          description: 'Segment trees, Trie prefix structures, disjoint-set union, Tarjan strongly connected components, and max-flow networks.',
          estimatedHours: 20.0,
          lessonsCount: 24,
          progress: 10
        },
        {
          id: 3,
          slug: 'distributed-systems',
          title: 'Distributed Consensus & Microservices Architecture',
          category: 'Architecture',
          difficulty: 'Advanced',
          description: 'Raft consensus, idempotent event streaming, distributed caching, and zero-trust security.',
          estimatedHours: 16.0,
          lessonsCount: 16,
          progress: 0
        }
      ];
    }

    const inProgress = courses.filter(c => (c.progress || 0) > 0);
    const catalog = courses;

    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1 class="page-title">
              <span>Developer Academy</span>
            </h1>
            <p class="page-description">Production software engineering, algorithmic problem solving, and cloud systems curriculum.</p>
          </div>
        </div>

        <!-- Section 1: Continue Learning -->
        ${inProgress.length > 0 ? `
          <div style="margin-bottom: var(--space-6);">
            <div style="font-size: var(--fs-sm); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: var(--space-3);">
              Continue Learning
            </div>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: var(--space-3);">
              ${inProgress.map(c => `
                <div class="card" style="background: var(--bg-surface);">
                  <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                    <span class="badge-tag badge-easy">${c.category}</span>
                    <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">${c.estimatedHours || 12} hrs</span>
                  </div>

                  <h3 style="font-size: var(--fs-sm); font-weight: 600; color: var(--text-primary); margin-bottom: 6px;">${c.title}</h3>
                  <p style="font-size: var(--fs-xs); color: var(--text-secondary); line-height: 1.45; margin-bottom: 12px;">${c.description}</p>

                  <div style="margin-bottom: 12px;">
                    <div class="flex justify-between" style="font-size: 11px; color: var(--text-muted); margin-bottom: 4px; font-family: var(--font-mono);">
                      <span>Progress</span>
                      <span style="color: var(--status-success); font-weight: 600;">${c.progress}% completed</span>
                    </div>
                    <div style="height: 4px; background: var(--bg-darkest); border-radius: 2px; overflow: hidden;">
                      <div style="width: ${c.progress}%; height: 100%; background: var(--accent-emerald);"></div>
                    </div>
                  </div>

                  <div class="flex justify-end">
                    <a href="#/courses/${c.slug || c.id}" class="btn btn-primary btn-sm">Resume Lesson →</a>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}

        <!-- Section 2: All Curriculum Tracks -->
        <div>
          <div style="font-size: var(--fs-sm); font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: var(--space-3);">
            Engineering Tracks & Courses
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: var(--space-3);">
            ${catalog.map(c => `
              <div class="card" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                  <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                    <span class="badge-tag">${c.category}</span>
                    <span style="font-family: var(--font-mono); font-size: 11px; color: var(--text-muted);">${c.difficulty}</span>
                  </div>

                  <h4 style="font-size: var(--fs-sm); font-weight: 600; color: var(--text-primary); margin-bottom: 6px;">${c.title}</h4>
                  <p style="font-size: var(--fs-xs); color: var(--text-secondary); line-height: 1.45; margin-bottom: 12px;">${c.description}</p>
                </div>

                <div class="flex items-center justify-between" style="padding-top: 10px; border-top: 1px solid var(--border-subtle);">
                  <span style="font-size: 11px; color: var(--text-muted); font-family: var(--font-mono);">${c.lessonsCount || 15} Lessons</span>
                  <a href="#/courses/${c.slug || c.id}" class="btn btn-secondary btn-sm">Explore Course</a>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }
}

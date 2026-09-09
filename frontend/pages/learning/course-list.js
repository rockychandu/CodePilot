/* Course Catalog Page Module */
import { CourseService } from '../../services/CourseService.js';

export class CourseListPage {
  static async render() {
    const courses = await CourseService.getCourses();

    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Developer Learning Center</h1>
            <p class="text-secondary">Master Python backend, data structures, algorithms, and AI engineering.</p>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-6">
          ${courses.map(c => `
            <div class="card" style="display: flex; flex-direction: column;">
              <img src="${c.thumbnail}" style="width: 100%; height: 160px; object-fit: cover; border-radius: var(--radius-md); margin-bottom: var(--space-4);" alt="${c.title}" />
              <div class="flex items-center justify-between" style="margin-bottom: 8px;">
                <span class="badge-tag badge-easy">${c.category}</span>
                <span style="font-size: var(--fs-xs); color: var(--accent-amber);">★ ${c.rating} (${c.studentsCount.toLocaleString()} students)</span>
              </div>
              <h3 style="font-size: var(--fs-base); margin-bottom: 8px;">${c.title}</h3>
              <p class="text-muted" style="font-size: var(--fs-xs); line-height: 1.5; margin-bottom: var(--space-4); flex: 1;">${c.description}</p>
              
              <div style="margin-bottom: var(--space-4);">
                <div class="flex justify-between" style="font-size: 11px; margin-bottom: 4px; color: var(--text-muted);">
                  <span>Progress</span>
                  <span style="color: var(--accent-cyan); font-weight: 600;">${c.progress}%</span>
                </div>
                <div style="height: 6px; background: var(--bg-darkest); border-radius: 3px; overflow: hidden;">
                  <div style="width: ${c.progress}%; height: 100%; background: var(--accent-cyan);"></div>
                </div>
              </div>

              <a href="#/learn/${c.id}" class="btn btn-primary w-full btn-sm">Explore Course (${c.lessonsCount} Lessons)</a>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }
}

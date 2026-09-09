/* Course Detail & Lesson Syllabus Page */
import { CourseService } from '../../services/CourseService.js';

export class CourseDetailPage {
  static async render({ params }) {
    const courseId = params?.id || 'course_1';
    let course;
    try {
      course = await CourseService.getCourseById(courseId);
    } catch (e) {
      course = await CourseService.getCourseById('course_1');
    }

    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <div class="flex items-center gap-2" style="margin-bottom: 8px;">
              <span class="badge-tag badge-easy">${course.category}</span>
              <span class="text-muted" style="font-size: var(--fs-xs);">Instructor: ${course.instructor}</span>
            </div>
            <h1>${course.title}</h1>
            <p class="text-secondary" style="max-width: 700px;">${course.description}</p>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-6">
          <div class="card" style="grid-column: span 2;">
            <h3 style="margin-bottom: var(--space-4);">Course Syllabus</h3>
            <div class="flex flex-col gap-3">
              ${course.lessons.map(l => `
                <div class="flex items-center justify-between" style="padding: 16px; background: var(--bg-darkest); border: 1px solid var(--border-subtle); border-radius: var(--radius-md);">
                  <div class="flex items-center gap-3">
                    <span style="font-size: 18px;">${l.type === 'video' ? '🎥' : '📄'}</span>
                    <div>
                      <strong style="font-size: var(--fs-sm);">${l.title}</strong>
                      <div class="text-muted" style="font-size: 11px;">${l.type.toUpperCase()} • ${l.duration}</div>
                    </div>
                  </div>

                  <a href="#/${l.type === 'video' ? 'videos' : 'pdfs'}/${l.id}" class="btn btn-secondary btn-sm">
                    ${l.completed ? '✓ Rewatch' : '▶ Start Lesson'}
                  </a>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="card" style="height: fit-content;">
            <h3 style="margin-bottom: var(--space-4);">Overview</h3>
            <div style="font-size: var(--fs-sm); color: var(--text-secondary); display: flex; flex-direction: column; gap: 12px;">
              <div>⏱️ Duration: <strong>${course.duration}</strong></div>
              <div>📖 Lessons: <strong>${course.lessonsCount} Total</strong></div>
              <div>🎓 Certificate: <strong>Included upon completion</strong></div>
            </div>
          </div>
        </div>
      </div>
    `;
  }
}

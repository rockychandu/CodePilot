/* Teacher Portal Page Module */

export class TeacherPage {
  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Teacher & Instructor Portal</h1>
            <p class="text-secondary">Manage courses, assignments, student progress metrics, and quiz problems.</p>
          </div>
          <button class="btn btn-primary">+ Create Course</button>
        </div>

        <div class="grid grid-cols-3 gap-6" style="margin-bottom: var(--space-8);">
          <div class="stat-widget">
            <div class="stat-widget-icon icon-blue">📚</div>
            <div>
              <div class="text-muted" style="font-size: var(--fs-xs);">Managed Courses</div>
              <div style="font-size: var(--fs-2xl); font-weight: 800;">4 Active</div>
            </div>
          </div>
          <div class="stat-widget">
            <div class="stat-widget-icon icon-purple">🎓</div>
            <div>
              <div class="text-muted" style="font-size: var(--fs-xs);">Enrolled Students</div>
              <div style="font-size: var(--fs-2xl); font-weight: 800;">24,300</div>
            </div>
          </div>
          <div class="stat-widget">
            <div class="stat-widget-icon icon-emerald">📝</div>
            <div>
              <div class="text-muted" style="font-size: var(--fs-xs);">Submissions Reviewed</div>
              <div style="font-size: var(--fs-2xl); font-weight: 800;">1,420</div>
            </div>
          </div>
        </div>

        <div class="card">
          <h3 style="margin-bottom: var(--space-4);">Student Performance Metrics</h3>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Course</th>
                  <th>Progress</th>
                  <th>Avg. Score</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Alex Developer</td>
                  <td>Python Core Mastery</td>
                  <td>65%</td>
                  <td><strong style="color: var(--accent-emerald);">94%</strong></td>
                  <td><button class="btn btn-secondary btn-sm">View Details</button></td>
                </tr>
                <tr>
                  <td>Samantha Wu</td>
                  <td>DSA with Python</td>
                  <td>80%</td>
                  <td><strong style="color: var(--accent-emerald);">98%</strong></td>
                  <td><button class="btn btn-secondary btn-sm">View Details</button></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  }
}

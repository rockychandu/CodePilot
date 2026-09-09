/* Problem List Page Module */
import { ProblemService } from '../../services/ProblemService.js';
import { store } from '../../state/store.js';

export class ProblemListPage {
  static async render() {
    const { problems } = await ProblemService.getProblems();
    const bookmarks = store.get('bookmarks') || [];

    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Problem Explorer</h1>
            <p class="text-secondary">Solve algorithm & engineering challenges across Python, C++, Java, and SQL.</p>
          </div>
        </div>

        <!-- Filter Bar -->
        <div class="card flex items-center justify-between" style="padding: 16px; margin-bottom: var(--space-6); flex-wrap: wrap; gap: 12px;">
          <div class="flex items-center gap-3" style="flex: 1; min-width: 280px;">
            <input type="text" id="problem-search-input" class="input-control" placeholder="Search problems by name or topic..." />
          </div>

          <div class="flex items-center gap-3">
            <select id="filter-difficulty" class="input-control" style="width: 140px;">
              <option value="All">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>

            <select id="filter-topic" class="input-control" style="width: 160px;">
              <option value="All">All Topics</option>
              <option value="Array">Array & Hash Map</option>
              <option value="Stack">Stack & String</option>
              <option value="Trees">Trees & BFS</option>
              <option value="Heap">Heap & Linked List</option>
            </select>
          </div>
        </div>

        <!-- Problem Data Table -->
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th style="width: 50px;">Status</th>
                <th>Title</th>
                <th>Difficulty</th>
                <th>Topic</th>
                <th>Acceptance</th>
                <th>Solved</th>
                <th style="width: 80px;">Bookmark</th>
              </tr>
            </thead>
            <tbody id="problems-table-body">
              ${problems.map(p => {
                const isBookmarked = bookmarks.includes(p.id);
                return `
                  <tr>
                    <td><span style="color: var(--status-success);">✓</span></td>
                    <td>
                      <a href="#/problems/${p.id}" style="font-weight: 600;">${p.title}</a>
                    </td>
                    <td><span class="badge-tag badge-${p.difficulty.toLowerCase()}">${p.difficulty}</span></td>
                    <td><span class="text-secondary">${p.topic}</span></td>
                    <td>${p.acceptanceRate}</td>
                    <td>${p.solvedCount.toLocaleString()}</td>
                    <td>
                      <button class="btn-bookmark btn btn-icon btn-sm" data-id="${p.id}">
                        ${isBookmarked ? '⭐' : '☆'}
                      </button>
                    </td>
                  </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;
  }

  static afterRender() {
    const searchInput = document.getElementById('problem-search-input');
    const diffSelect = document.getElementById('filter-difficulty');
    const topicSelect = document.getElementById('filter-topic');

    const updateList = async () => {
      const { problems } = await ProblemService.getProblems({
        search: searchInput?.value,
        difficulty: diffSelect?.value,
        topic: topicSelect?.value
      });

      const bookmarks = store.get('bookmarks') || [];
      const tbody = document.getElementById('problems-table-body');

      if (tbody) {
        tbody.innerHTML = problems.map(p => `
          <tr>
            <td><span style="color: var(--status-success);">✓</span></td>
            <td><a href="#/problems/${p.id}" style="font-weight: 600;">${p.title}</a></td>
            <td><span class="badge-tag badge-${p.difficulty.toLowerCase()}">${p.difficulty}</span></td>
            <td><span class="text-secondary">${p.topic}</span></td>
            <td>${p.acceptanceRate}</td>
            <td>${p.solvedCount.toLocaleString()}</td>
            <td>
              <button class="btn-bookmark btn btn-icon btn-sm" data-id="${p.id}">
                ${bookmarks.includes(p.id) ? '⭐' : '☆'}
              </button>
            </td>
          </tr>
        `).join('');
        attachBookmarkEvents();
      }
    };

    if (searchInput) searchInput.addEventListener('input', updateList);
    if (diffSelect) diffSelect.addEventListener('change', updateList);
    if (topicSelect) topicSelect.addEventListener('change', updateList);

    const attachBookmarkEvents = () => {
      document.querySelectorAll('.btn-bookmark').forEach(btn => {
        btn.addEventListener('click', (e) => {
          const id = btn.getAttribute('data-id');
          const isNowBookmarked = ProblemService.toggleBookmark(id);
          btn.innerText = isNowBookmarked ? '⭐' : '☆';
        });
      });
    };

    attachBookmarkEvents();
  }
}

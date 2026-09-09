/* Problem Service Layer */
import { mockProblems } from '../mock-data/problems.js';
import { store } from '../state/store.js';
import { sleep } from '../utils/helpers.js';

export class ProblemService {
  static async getProblems({ difficulty, topic, search, category, page = 1, limit = 10 } = {}) {
    await sleep(200);
    let results = [...mockProblems];

    if (difficulty && difficulty !== 'All') {
      results = results.filter(p => p.difficulty.toLowerCase() === difficulty.toLowerCase());
    }

    if (topic && topic !== 'All') {
      results = results.filter(p => p.topic.toLowerCase().includes(topic.toLowerCase()));
    }

    if (search && search.trim()) {
      const query = search.trim().toLowerCase();
      results = results.filter(p => p.title.toLowerCase().includes(query) || p.description.toLowerCase().includes(query));
    }

    const total = results.length;
    const start = (page - 1) * limit;
    const paginated = results.slice(start, start + limit);

    return { problems: paginated, total, page, totalPages: Math.ceil(total / limit) };
  }

  static async getProblemById(id) {
    await sleep(150);
    const problem = mockProblems.find(p => p.id === id);
    if (!problem) throw new Error(`Problem ${id} not found.`);
    return problem;
  }

  static toggleBookmark(problemId) {
    const currentBookmarks = store.get('bookmarks') || [];
    const exists = currentBookmarks.includes(problemId);
    const updated = exists ? currentBookmarks.filter(id => id !== problemId) : [...currentBookmarks, problemId];
    store.set('bookmarks', updated);
    return !exists;
  }
}

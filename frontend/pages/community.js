/* Community Discussions Forum Page Module */
import { mockDiscussions } from '../mock-data/discussions.js';

export class CommunityPage {
  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>Developer Community Forum</h1>
            <p class="text-secondary">Ask questions, share Python architecture tips, and collaborate.</p>
          </div>
          <button class="btn btn-primary">+ New Discussion</button>
        </div>

        <div class="flex flex-col gap-4">
          ${mockDiscussions.map(d => `
            <div class="card flex justify-between items-center">
              <div class="flex items-center gap-4">
                <img src="${d.authorAvatar}" style="width: 44px; height: 44px; border-radius: 50%;" />
                <div>
                  <h3 style="font-size: var(--fs-base); margin-bottom: 4px;">
                    <a href="#/community">${d.title}</a>
                  </h3>
                  <div class="flex items-center gap-3 text-muted" style="font-size: var(--fs-xs);">
                    <span>By ${d.author}</span>
                    <span>• ${d.category}</span>
                    <span>• ${d.repliesCount} replies</span>
                  </div>
                </div>
              </div>

              <div class="flex items-center gap-2">
                <button class="btn btn-secondary btn-sm">▲ ${d.upvotes}</button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }
}

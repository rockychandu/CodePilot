/* Video Lesson Page Module */
import { VideoPlayerComponent } from '../../components/video-player.js';

export class VideoViewPage {
  static async render({ params }) {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <a href="#/learn" class="text-muted" style="font-size: var(--fs-xs);">← Back to Course</a>
            <h1 style="margin-top: 4px;">Lesson 1: Python Syntax & Control Flow</h1>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-6">
          <div style="grid-column: span 2;">
            ${VideoPlayerComponent.render({ title: 'Lesson 1: Python Syntax & Control Flow' })}
            
            <div class="card" style="margin-top: var(--space-6);">
              <h3 style="margin-bottom: 12px;">Lesson Transcript & Notes</h3>
              <p class="text-secondary" style="font-size: var(--fs-sm); line-height: 1.6;">
                In this video lesson, we explore Python's dynamic typing, whitespace-delimited indentation syntax, and conditional execution statements.
              </p>
            </div>
          </div>

          <div class="card" style="height: fit-content;">
            <h4 style="margin-bottom: 12px;">Take Lesson Notes</h4>
            <textarea class="input-control" style="height: 140px; margin-bottom: 12px;" placeholder="Type your personal lesson notes here..."></textarea>
            <button class="btn btn-primary w-full btn-sm">Save Notes</button>
          </div>
        </div>
      </div>
    `;
  }

  static afterRender() {
    VideoPlayerComponent.attachEvents();
  }
}

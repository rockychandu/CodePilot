/* PDF Document Reader Page Module */
import { PdfViewerComponent } from '../../components/pdf-viewer.js';

export class PdfViewPage {
  static async render({ params }) {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <a href="#/learn" class="text-muted" style="font-size: var(--fs-xs);">← Back to Course</a>
            <h1 style="margin-top: 4px;">PDF Guide: Python OOP & Architecture</h1>
          </div>
        </div>

        ${PdfViewerComponent.render({ docTitle: 'Python OOP & Architecture Guide.pdf' })}
      </div>
    `;
  }
}

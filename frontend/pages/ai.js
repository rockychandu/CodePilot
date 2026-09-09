/* Pilot AI Assistant & AI Fine-Tuning Dashboard */
import { AIService } from '../services/AIService.js';

export class AIPage {
  static async render() {
    return `
      <div class="page-wrapper">
        <div class="page-header">
          <div>
            <h1>✨ Pilot AI Assistant & Fine-Tuning Studio</h1>
            <p class="text-secondary">AI-powered code review, bug detection, PEP8 linting, and experiment tracking.</p>
          </div>
        </div>

        <!-- Grid: AI Assistant Chat & AI Model Metrics -->
        <div class="grid grid-cols-2 gap-6">
          <!-- Chat Assistant Window -->
          <div class="ai-chat-window">
            <div style="padding: 12px 20px; background: var(--bg-darkest); border-bottom: 1px solid var(--border-subtle); font-weight: 600; font-size: var(--fs-sm);">
              ✨ Pilot AI Assistant (Python v2.4)
            </div>

            <div id="ai-messages-list" class="ai-chat-messages">
              <div class="chat-bubble chat-bubble-ai">
                Hello! I am <strong>Pilot AI</strong>. Paste your Python code or ask me to review complexity, fix bugs, or write solutions!
              </div>
            </div>

            <div style="padding: 16px; background: var(--bg-darkest); border-top: 1px solid var(--border-subtle); display: flex; gap: 8px;">
              <input type="text" id="ai-prompt-input" class="input-control" placeholder="Ask Pilot AI to review code, explain AST, or optimize..." />
              <button id="btn-send-ai" class="btn btn-primary btn-sm">Send</button>
            </div>
          </div>

          <!-- AI Model Fine-Tuning Dashboard -->
          <div class="card flex flex-col justify-between">
            <div>
              <h3 style="margin-bottom: 16px;">AI Model Experiments & Metrics</h3>
              <div class="grid grid-cols-2 gap-4" style="margin-bottom: 20px;">
                <div style="background: var(--bg-darkest); padding: 12px; border-radius: var(--radius-md);">
                  <div class="text-muted" style="font-size: 11px;">Active Checkpoint</div>
                  <strong style="color: var(--accent-cyan);">PilotAI-v2.4-epoch40</strong>
                </div>
                <div style="background: var(--bg-darkest); padding: 12px; border-radius: var(--radius-md);">
                  <div class="text-muted" style="font-size: 11px;">Training Loss</div>
                  <strong style="color: var(--accent-emerald);">0.0412 (Optimal)</strong>
                </div>
              </div>

              <!-- Simulated Training Curve SVG -->
              <h4 style="font-size: var(--fs-xs); text-transform: uppercase; color: var(--text-muted); margin-bottom: 8px;">Loss Curve Across Epochs</h4>
              <div style="height: 160px; background: var(--bg-darkest); border-radius: var(--radius-md); padding: 12px; position: relative;">
                <svg width="100%" height="100%" viewBox="0 0 400 120">
                  <path d="M 10 100 Q 100 20, 200 60 T 390 20" fill="none" stroke="#38BDF8" stroke-width="3" />
                  <circle cx="390" cy="20" r="5" fill="#38BDF8" />
                </svg>
              </div>
            </div>

            <button id="btn-trigger-review" class="btn btn-secondary w-full" style="margin-top: 16px;">Run Code Review Audit</button>
          </div>
        </div>
      </div>
    `;
  }

  static afterRender() {
    const input = document.getElementById('ai-prompt-input');
    const sendBtn = document.getElementById('btn-send-ai');
    const list = document.getElementById('ai-messages-list');

    const handleSend = async () => {
      const text = input?.value.trim();
      if (!text) return;

      list.innerHTML += `<div class="chat-bubble chat-bubble-user">${text}</div>`;
      input.value = '';
      list.scrollTop = list.scrollHeight;

      const aiRes = await AIService.askPilotAI(text);
      list.innerHTML += `<div class="chat-bubble chat-bubble-ai">${aiRes.reply.replace(/\n/g, '<br>')}</div>`;
      list.scrollTop = list.scrollHeight;
    };

    if (sendBtn) sendBtn.addEventListener('click', handleSend);
    if (input) {
      input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleSend();
      });
    }
  }
}

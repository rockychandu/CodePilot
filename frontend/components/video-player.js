/* Custom HTML5 Video Player UI Component */

export class VideoPlayerComponent {
  static render({ title, chapters = [] }) {
    return `
      <div class="video-player-container w-full">
        <!-- HTML5 Video element -->
        <video id="course-video-element" class="w-full h-full" style="object-fit: cover;" poster="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&auto=format&fit=crop&q=80">
          <source src="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4" type="video/mp4" />
          Your browser does not support HTML5 video.
        </video>

        <!-- Custom Video Controls Overlay -->
        <div class="video-player-controls">
          <div class="flex items-center gap-3">
            <button id="btn-video-play" class="btn btn-icon btn-sm" style="color: #FFF;">▶</button>
            <span style="font-size: var(--fs-xs); font-weight: 600;">${title || 'Lesson Video'}</span>
          </div>

          <div class="flex items-center gap-4">
            <select id="video-speed-select" style="background: rgba(0,0,0,0.6); color: #FFF; font-size: 11px; padding: 2px 6px; border-radius: 4px;">
              <option value="1">1.0x Speed</option>
              <option value="1.25">1.25x Speed</option>
              <option value="1.5">1.5x Speed</option>
              <option value="2">2.0x Speed</option>
            </select>
            <button id="btn-video-fullscreen" class="btn btn-icon btn-sm" style="color: #FFF;">⛶</button>
          </div>
        </div>
      </div>
    `;
  }

  static attachEvents() {
    const video = document.getElementById('course-video-element');
    const playBtn = document.getElementById('btn-video-play');
    const speedSelect = document.getElementById('video-speed-select');
    const fsBtn = document.getElementById('btn-video-fullscreen');

    if (video && playBtn) {
      playBtn.addEventListener('click', () => {
        if (video.paused) {
          video.play();
          playBtn.innerText = '⏸';
        } else {
          video.pause();
          playBtn.innerText = '▶';
        }
      });
    }

    if (video && speedSelect) {
      speedSelect.addEventListener('change', (e) => {
        video.playbackRate = parseFloat(e.target.value);
      });
    }

    if (video && fsBtn) {
      fsBtn.addEventListener('click', () => {
        if (video.requestFullscreen) video.requestFullscreen();
      });
    }
  }
}

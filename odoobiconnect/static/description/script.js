// script.js

// Modal Lightbox
const modal = document.getElementById('imageModal');
const modalImg = document.getElementById('fullImage');
const closeModal = document.querySelector('.close-modal');

// Open modal on screenshot click (only if image exists)
const cards = document.querySelectorAll('.screenshot-card');
cards.forEach(card => {
    card.addEventListener('click', (e) => {
        const img = card.querySelector('img');
        if (img && img.src && !img.src.includes('error')) {
            modal.style.display = 'flex';
            modalImg.src = img.src;
        }
    });
});

closeModal.addEventListener('click', () => {
    modal.style.display = 'none';
});
modal.addEventListener('click', (e) => {
    if (e.target === modal) modal.style.display = 'none';
});

// Video fallback function
function showVideoFallback() {
    const videoContainer = document.getElementById('videoContainer');
    if (videoContainer) {
        videoContainer.innerHTML = `
            <div class="video-placeholder" onclick="window.open('https://youtu.be/9RicXvZ6_GI', '_blank')">
                <i class="fab fa-youtube"></i>
                <strong style="color: #C9A03D; display: block; margin-bottom: 8px;">Video: odoobiconnect_demo.mp4</strong>
                <span style="color: #94A3B8; font-size: 14px;">Click to watch on YouTube →</span>
            </div>
        `;
    }
}

// Check if video exists and load, otherwise show fallback
const video = document.getElementById('demoVideo');
if (video) {
    video.addEventListener('error', function() {
        showVideoFallback();
    });
}
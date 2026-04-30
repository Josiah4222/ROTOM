// Event Detail Sharing Functionality

// Helper: Draw rounded rectangle
function roundRect(ctx, x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
}

// Helper: Wrap text
function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
    const words = text.split(' ');
    let line = '';
    let testLine, metrics, testWidth;

    for (let n = 0; n < words.length; n++) {
        testLine = line + words[n] + ' ';
        metrics = ctx.measureText(testLine);
        testWidth = metrics.width;
        if (testWidth > maxWidth && n > 0) {
            ctx.fillText(line.trim(), x, y);
            line = words[n] + ' ';
            y += lineHeight;
        } else {
            line = testLine;
        }
    }
    ctx.fillText(line.trim(), x, y);
}

// Generate story card using Canvas API - CLEAN PROFESSIONAL DESIGN
async function generateStoryImage() {
    const data = window.eventData;
    if (!data) return;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // Story dimensions (9:16 ratio)
    canvas.width = 1080;
    canvas.height = 1920;

    const img = new Image();
    img.crossOrigin = 'anonymous';

    return new Promise((resolve, reject) => {
        img.onload = () => {
            // Fill white background
            ctx.fillStyle = 'white';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Draw image in top 65% (1248px)
            const imageHeight = 1248;
            const scale = Math.max(canvas.width / img.width, imageHeight / img.height);
            const scaledWidth = img.width * scale;
            const scaledHeight = img.height * scale;
            const x = (canvas.width - scaledWidth) / 2;
            const y = (imageHeight - scaledHeight) / 2;
            
            // Clip to image area
            ctx.save();
            ctx.rect(0, 0, canvas.width, imageHeight);
            ctx.clip();
            ctx.drawImage(img, x, y, scaledWidth, scaledHeight);
            ctx.restore();

            // Gradient overlay at bottom of image
            const gradient = ctx.createLinearGradient(0, imageHeight - 200, 0, imageHeight + 100);
            gradient.addColorStop(0, 'rgba(255, 255, 255, 0)');
            gradient.addColorStop(0.5, 'rgba(255, 255, 255, 0.95)');
            gradient.addColorStop(1, 'rgba(255, 255, 255, 1)');
            ctx.fillStyle = gradient;
            ctx.fillRect(0, imageHeight - 200, canvas.width, 300);

            // Logo at top left
            ctx.fillStyle = 'white';
            ctx.font = 'bold 56px Poppins, sans-serif';
            ctx.textAlign = 'left';
            ctx.shadowColor = 'rgba(0,0,0,0.3)';
            ctx.shadowBlur = 8;
            ctx.shadowOffsetY = 2;
            ctx.fillText('ROTOM Ethiopia', 80, 140);
            ctx.shadowBlur = 0;
            ctx.shadowOffsetY = 0;

            // Badge at middle left
            ctx.fillStyle = 'white';
            ctx.shadowColor = 'rgba(0,0,0,0.15)';
            ctx.shadowBlur = 12;
            roundRect(ctx, 80, 960, 280, 60, 8);
            ctx.fill();
            ctx.shadowBlur = 0;
            
            ctx.fillStyle = '#1C651B';
            ctx.font = 'bold 28px Poppins, sans-serif';
            ctx.textAlign = 'left';
            ctx.fillText('UPCOMING EVENT', 100, 1000);

            // Title on white background
            ctx.fillStyle = '#1f2937';
            ctx.font = 'bold 80px Poppins, sans-serif';
            ctx.textAlign = 'left';
            wrapText(ctx, data.title, 80, 1380, canvas.width - 160, 95);

            // Date
            ctx.fillStyle = '#1C651B';
            ctx.font = '600 48px Poppins, sans-serif';
            ctx.textAlign = 'left';
            ctx.fillText('📅  ' + data.date, 80, 1600);

            // CTA Button
            ctx.fillStyle = '#1C651B';
            ctx.shadowColor = 'rgba(28, 101, 27, 0.25)';
            ctx.shadowBlur = 20;
            roundRect(ctx, 80, 1680, 920, 100, 12);
            ctx.fill();
            ctx.shadowBlur = 0;
            
            ctx.fillStyle = 'white';
            ctx.font = 'bold 52px Poppins, sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('Join Us!', canvas.width / 2, 1750);

            canvas.toBlob(resolve, 'image/png', 1.0);
        };
        img.onerror = reject;
        img.src = data.imageUrl;
    });
}

// Share story card
async function downloadStoryCard() {
    const btn = document.querySelector('.download-story-btn');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Creating...';
    btn.disabled = true;

    try {
        const data = window.eventData;
        const blob = await generateStoryImage();
        const file = new File([blob], `ROTOM-Event-${data.date.replace(/\s/g, '-')}.png`, { type: 'image/png' });

        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            await navigator.share({
                files: [file],
                title: data.title,
                text: `Check out this event: ${data.title}`
            });
            showNotification('Shared successfully!');
        } else {
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.download = file.name;
            link.href = url;
            link.click();
            URL.revokeObjectURL(url);
            showNotification('Image saved! Share it to your story!');
        }
    } catch (error) {
        if (error.name !== 'AbortError') {
            console.error('Error:', error);
            showNotification('Could not share. Try again!');
        }
    } finally {
        btn.innerHTML = originalText;
        btn.disabled = false;
    }
}

// Copy link to clipboard
function copyEventLink() {
    const data = window.eventData;
    navigator.clipboard.writeText(data.url).then(() => {
        showNotification('Link copied!');
    }).catch(() => {
        const textArea = document.createElement('textarea');
        textArea.value = data.url;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Link copied!');
    });
}

// Show notification
function showNotification(message) {
    const notification = document.getElementById('copyNotification');
    if (notification) {
        notification.textContent = message;
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }
}

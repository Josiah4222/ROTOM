// Event Detail Sharing Functionality - Immersive Redesign

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

// Helper: Wrap text with line limit
function wrapText(ctx, text, x, y, maxWidth, lineHeight, maxLines = 4) {
    const words = text.split(' ');
    let line = '';
    let lines = 0;

    for (let n = 0; n < words.length; n++) {
        let testLine = line + words[n] + ' ';
        let metrics = ctx.measureText(testLine);
        let testWidth = metrics.width;
        
        if (testWidth > maxWidth && n > 0) {
            ctx.fillText(line.trim(), x, y);
            line = words[n] + ' ';
            y += lineHeight;
            lines++;
            if (lines >= maxLines - 1) {
                let lastLine = '';
                for(let i=n; i<words.length; i++) {
                    let testLast = lastLine + words[i] + ' ';
                    if (ctx.measureText(testLast + '...').width > maxWidth) break;
                    lastLine = testLast;
                }
                ctx.fillText(lastLine.trim() + (n < words.length - 1 ? '...' : ''), x, y);
                return y;
            }
        } else {
            line = testLine;
        }
    }
    ctx.fillText(line.trim(), x, y);
    return y;
}

// Generate story card using Canvas API - ULTRA ROBUST VERSION
async function generateStoryImage() {
    const data = window.eventData;
    if (!data) return;

    // Use a more standard story size (720x1280) to avoid browser limits
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 720;
    canvas.height = 1280;

    return new Promise((resolve, reject) => {
        const img = new Image();
        // Force crossOrigin to anonymous to try and get CORS working
        img.crossOrigin = 'anonymous';
        
        img.onload = () => {
            try {
                // 1. Draw Background
                const scale = Math.max(canvas.width / img.width, canvas.height / img.height);
                const x = (canvas.width - img.width * scale) / 2;
                const y = (canvas.height - img.height * scale) / 2;
                ctx.drawImage(img, x, y, img.width * scale, img.height * scale);

                // 2. Immersive Gradients
                const bottomGrad = ctx.createLinearGradient(0, canvas.height * 0.4, 0, canvas.height);
                bottomGrad.addColorStop(0, 'rgba(0, 0, 0, 0)');
                bottomGrad.addColorStop(0.7, 'rgba(0, 0, 0, 0.85)');
                bottomGrad.addColorStop(1, 'rgba(0, 0, 0, 0.95)');
                ctx.fillStyle = bottomGrad;
                ctx.fillRect(0, canvas.height * 0.4, canvas.width, canvas.height * 0.6);

                const topGrad = ctx.createLinearGradient(0, 0, 0, 200);
                topGrad.addColorStop(0, 'rgba(0, 0, 0, 0.6)');
                topGrad.addColorStop(1, 'rgba(0, 0, 0, 0)');
                ctx.fillStyle = topGrad;
                ctx.fillRect(0, 0, canvas.width, 200);

                // 3. Branding
                ctx.fillStyle = 'white';
                ctx.font = 'bold 32px sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('ROTOM Ethiopia', 40, 60);

                // 4. Content Decor
                ctx.fillStyle = '#F1C93B';
                ctx.fillRect(40, 950, 80, 6);

                // 5. Title (Bold and Clear)
                ctx.fillStyle = 'white';
                ctx.font = 'bold 64px sans-serif';
                ctx.textAlign = 'left';
                wrapText(ctx, data.title.toUpperCase(), 40, 1050, canvas.width - 80, 75, 2);

                // 6. Event Details
                ctx.fillStyle = '#F1C93B';
                ctx.font = '600 36px sans-serif';
                ctx.fillText('📅 ' + data.date, 40, 1200);

                // Export as Blob
                canvas.toBlob((blob) => {
                    if (blob) resolve(blob);
                    else reject(new Error('Canvas toBlob failed'));
                }, 'image/png');
            } catch (err) {
                console.error('Canvas Error:', err);
                // Fallback: fetch original image as blob
                fetch(data.imageUrl).then(res => res.blob()).then(resolve).catch(reject);
            }
        };

        img.onerror = () => {
            fetch(data.imageUrl).then(res => res.blob()).then(resolve).catch(reject);
        };

        img.src = data.imageUrl + (data.imageUrl.includes('?') ? '&' : '?') + 't=' + Date.now();
    });
}

// Share story card - NOW SUPPORTS DIRECT STORY SHARING
async function downloadStoryCard() {
    const btn = document.querySelector('.share-icon-btn i.fa-camera-retro')?.parentElement;
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    }

    try {
        const data = window.eventData;
        showNotification('Preparing for story...');
        const blob = await generateStoryImage();
        
        const fileName = `ROTOM-${data.title.substring(0,15).replace(/[^a-z0-9]/gi, '_')}.png`;
        const file = new File([blob], fileName, { type: 'image/png' });

        // Try to use Native Share API for direct Story sharing (Mobile)
        if (navigator.canShare && navigator.canShare({ files: [file] })) {
            await navigator.share({
                files: [file],
                title: data.title,
                text: 'Join us for this event!'
            });
            showNotification('Shared to story!');
        } else {
            // Fallback for Desktop: Download automatically
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = fileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            setTimeout(() => URL.revokeObjectURL(url), 100);
            showNotification('Poster saved! Upload it to your story.');
        }
    } catch (error) {
        if (error.name !== 'AbortError') {
            console.error('Share Error:', error);
            showNotification('Could not share. Downloaded instead.');
        }
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-camera-retro"></i>';
        }
    }
}

// Download poster specifically as JPEG
async function downloadPoster() {
    await downloadStoryCard();
}

// Native Web Share API
async function shareNative() {
    const data = window.eventData;
    if (navigator.share) {
        try {
            await navigator.share({
                title: data.title,
                text: `Check out this event: ${data.title}`,
                url: data.url
            });
        } catch (error) {
            if (error.name !== 'AbortError') {
                console.error('Error sharing:', error);
            }
        }
    } else {
        copyEventLink();
        showNotification('Link copied to clipboard!');
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

// QR Code Toggle
let qrCodeInstance = null;
function toggleQRCode() {
    const modal = document.getElementById('qrModal');
    const data = window.eventData;
    
    if (!modal.classList.contains('show')) {
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        if (!qrCodeInstance) {
            qrCodeInstance = new QRCode(document.getElementById("qrcode"), {
                text: data.url,
                width: 256,
                height: 256,
                colorDark: "#1C651B",
                colorLight: "#ffffff",
                correctLevel: QRCode.CorrectLevel.H
            });
        }
    } else {
        modal.classList.remove('show');
        document.body.style.overflow = '';
    }
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

// Close QR Modal on outside click
window.addEventListener('click', (e) => {
    const modal = document.getElementById('qrModal');
    if (e.target === modal) {
        toggleQRCode();
    }
});

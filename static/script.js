// API endpoint
const API_URL = 'http://localhost:8080';

// Get DOM elements
const searchForm = document.getElementById('searchForm');
const queryInput = document.getElementById('queryInput');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const answerContent = document.getElementById('answerContent');
const sourcesContent = document.getElementById('sourcesContent');
const errorMessage = document.getElementById('errorMessage');
const modelStatus = document.getElementById('modelStatus');
const statusText = document.getElementById('statusText');

// ============================================
// MODEL STATUS UPDATER
// ============================================
async function updateModelStatus() {
    try {
        const response = await fetch(`${API_URL}/model-status`);
        const data = await response.json();
        
        if (data.display_text) {
            statusText.textContent = data.display_text;
            
            // Change color based on state
            if (data.state === 'expert') {
                modelStatus.style.borderLeftColor = '#00ff88';
                statusText.style.color = '#00ff88';
            } else if (data.state === 'ready') {
                modelStatus.style.borderLeftColor = '#ffed4e';
                statusText.style.color = '#ffed4e';
            } else {
                modelStatus.style.borderLeftColor = '#00fff9';
                statusText.style.color = '#00fff9';
            }
        }
    } catch (error) {
        console.log('Could not fetch model status:', error);
        statusText.textContent = 'STATUS OFFLINE';
    }
}

// Update status every 10 seconds
updateModelStatus();
setInterval(updateModelStatus, 10000);

// ============================================
// STARFIELD ANIMATION
// ============================================
const canvas = document.getElementById('starfield');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

// Star particles with FUNK (optimized)
const stars = [];
const starCount = 100;

class Star {
    constructor() {
        this.reset();
    }

    reset() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.z = Math.random() * canvas.width;
        this.size = Math.random() * 3;
        this.speed = Math.random() * 0.8 + 0.3;
        
        // More FUNK colors!
        const colors = ['#00fff9', '#ffed4e', '#ff2a6d', '#00ff88', '#b967ff', '#ff6b35', '#ffffff'];
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.twinkle = Math.random() * Math.PI * 2;
    }

    update() {
        this.z -= this.speed;
        this.twinkle += 0.05;
        
        if (this.z <= 0) {
            this.reset();
            this.z = canvas.width;
        }
    }

    draw() {
        const x = (this.x - canvas.width / 2) * (canvas.width / this.z);
        const y = (this.y - canvas.height / 2) * (canvas.width / this.z);
        const s = this.size * (canvas.width / this.z);
        
        const centerX = canvas.width / 2 + x;
        const centerY = canvas.height / 2 + y;
        
        if (centerX >= 0 && centerX <= canvas.width && 
            centerY >= 0 && centerY <= canvas.height) {
            
            // Twinkle effect
            const twinkleAlpha = (Math.sin(this.twinkle) + 1) / 2;
            
            ctx.beginPath();
            ctx.arc(centerX, centerY, s, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.shadowBlur = 15 + twinkleAlpha * 10;
            ctx.shadowColor = this.color;
            ctx.globalAlpha = 0.6 + twinkleAlpha * 0.4;
            ctx.fill();
            ctx.globalAlpha = 1;
            
            // Longer, more vibrant trail
            const trailLength = 30;
            const trailX = centerX + x / 40;
            const trailY = centerY + y / 40;
            
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(trailX, trailY);
            ctx.strokeStyle = this.color;
            ctx.lineWidth = s / 1.5;
            ctx.globalAlpha = 0.5;
            ctx.shadowBlur = 20;
            ctx.shadowColor = this.color;
            ctx.stroke();
            ctx.globalAlpha = 1;
        }
    }
}

// Initialize stars
for (let i = 0; i < starCount; i++) {
    stars.push(new Star());
}

// Draw static stars once
function drawStaticStarfield() {
    ctx.fillStyle = '#0a1535';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    stars.forEach(star => {
        const x = star.x;
        const y = star.y;
        const s = star.size;
        
        ctx.beginPath();
        ctx.arc(x, y, s, 0, Math.PI * 2);
        ctx.fillStyle = star.color;
        ctx.shadowBlur = 5;
        ctx.shadowColor = star.color;
        ctx.globalAlpha = 0.8;
        ctx.fill();
        ctx.globalAlpha = 1;
    });
}

drawStaticStarfield();

// Resize canvas on window resize
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    drawStaticStarfield();
});

// ============================================
// PARTICLE BURST EFFECT ON BUTTON CLICK
// ============================================
function createParticleBurst(x, y) {
    const particleCount = 25;
    const particles = [];
    
    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 15,
            vy: (Math.random() - 0.5) * 15,
            life: 120,
            size: Math.random() * 4 + 2,
            rotation: Math.random() * Math.PI * 2,
            rotationSpeed: (Math.random() - 0.5) * 0.3,
            color: ['#00fff9', '#ffed4e', '#ff2a6d', '#00ff88', '#b967ff', '#ff6b35'][Math.floor(Math.random() * 6)]
        });
    }
    
    function animateParticles() {
        particles.forEach((particle, index) => {
            particle.x += particle.vx;
            particle.y += particle.vy;
            particle.life -= 2;
            particle.vy += 0.3; // gravity
            particle.vx *= 0.99; // friction
            particle.rotation += particle.rotationSpeed;
            
            if (particle.life > 0) {
                ctx.save();
                ctx.translate(particle.x, particle.y);
                ctx.rotate(particle.rotation);
                
                // Draw star-shaped particle
                ctx.beginPath();
                for (let i = 0; i < 5; i++) {
                    const angle = (i * 4 * Math.PI) / 5;
                    const radius = i % 2 === 0 ? particle.size : particle.size / 2;
                    const px = Math.cos(angle) * radius;
                    const py = Math.sin(angle) * radius;
                    if (i === 0) ctx.moveTo(px, py);
                    else ctx.lineTo(px, py);
                }
                ctx.closePath();
                
                ctx.fillStyle = particle.color;
                ctx.globalAlpha = particle.life / 120;
                ctx.shadowBlur = 20;
                ctx.shadowColor = particle.color;
                ctx.fill();
                ctx.globalAlpha = 1;
                
                ctx.restore();
            } else {
                particles.splice(index, 1);
            }
        });
        
        if (particles.length > 0) {
            requestAnimationFrame(animateParticles);
        }
    }
    
    animateParticles();
}

// Add particle effect on search button click
document.getElementById('searchBtn').addEventListener('click', (e) => {
    const rect = e.target.getBoundingClientRect();
    const x = rect.left + rect.width / 2;
    const y = rect.top + rect.height / 2;
    createParticleBurst(x, y);
});

// ============================================
// SEARCH FORM SUBMISSION
// ============================================
searchForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const query = queryInput.value.trim();
    if (!query) return;
    
    // Hide previous results and errors
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Show loading with glitch effect
    loadingSection.style.display = 'block';
    loadingSection.style.animation = 'glitch 0.3s ease-in-out';
    
    setTimeout(() => {
        loadingSection.style.animation = '';
    }, 300);
    
    animateLoadingSteps();
    
    try {
        const response = await fetch(`${API_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'System error detected');
        }
        
        // Hide loading
        loadingSection.style.display = 'none';
        
        // Display results with holographic effect
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        loadingSection.style.display = 'none';
        showError(error.message);
    }
});

// ============================================
// ANIMATE LOADING STEPS
// ============================================
function animateLoadingSteps() {
    const steps = ['step1', 'step2', 'step3'];
    steps.forEach((stepId, index) => {
        const step = document.getElementById(stepId);
        step.classList.remove('active');
        
        setTimeout(() => {
            step.classList.add('active');
            
            // Add glitch effect when step activates
            step.style.animation = 'glitch 0.2s ease-in-out';
            setTimeout(() => {
                step.style.animation = '';
            }, 200);
        }, index * 1000);
    });
}

// ============================================
// DISPLAY RESULTS
// ============================================
function displayResults(data) {
    // Format and display answer with typing effect
    const formattedAnswer = formatAnswer(data.answer);
    answerContent.innerHTML = '';
    
    // Add holographic reveal effect
    resultsSection.style.display = 'block';
    resultsSection.style.animation = 'fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
    
    // Typing effect for answer
    let charIndex = 0;
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = formattedAnswer;
    const textContent = tempDiv.textContent;
    
    answerContent.innerHTML = formattedAnswer;
    answerContent.style.opacity = '0';
    
    setTimeout(() => {
        answerContent.style.transition = 'opacity 0.8s ease-in';
        answerContent.style.opacity = '1';
    }, 100);
    
    // Display sources with staggered animation
    if (data.sources && data.sources.length > 0) {
        sourcesContent.innerHTML = '';
        data.sources.forEach((source, index) => {
            const sourceDiv = document.createElement('div');
            sourceDiv.className = 'source-item';
            sourceDiv.style.opacity = '0';
            sourceDiv.style.transform = 'translateX(-20px)';
            
            sourceDiv.innerHTML = `
                <a href="${source.url}" target="_blank" rel="noopener noreferrer">
                    ▶ ${index + 1}. ${source.title || 'Unknown Source'}
                </a>
                <div class="source-url">${source.url}</div>
            `;
            
            sourcesContent.appendChild(sourceDiv);
            
            // Staggered fade-in animation
            setTimeout(() => {
                sourceDiv.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
                sourceDiv.style.opacity = '1';
                sourceDiv.style.transform = 'translateX(0)';
            }, 100 * index);
        });
    } else {
        sourcesContent.innerHTML = '<p style="color: rgba(255, 255, 255, 0.6);">⚠ No sources detected</p>';
    }
    
    // Scroll to results with smooth animation
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 200);
}

// ============================================
// FORMAT ANSWER
// ============================================
function formatAnswer(text) {
    if (!text) return '<p style="color: rgba(255, 255, 255, 0.6);">⚠ No data available</p>';
    
    // Convert markdown-style formatting to HTML
    let formatted = text
        // Headers
        .replace(/### (.*)/g, '<h4>⟨ $1 ⟩</h4>')
        .replace(/## (.*)/g, '<h3>⟨ $1 ⟩</h3>')
        .replace(/# (.*)/g, '<h3>⟨ $1 ⟩</h3>')
        // Bold
        .replace(/\*\*(.*?)\*\*/g, '<strong>⟨ $1 ⟩</strong>')
        // Lists - numbered
        .replace(/^\d+\.\s(.+)$/gm, '<li>▸ $1</li>')
        // Lists - bullets
        .replace(/^[•\-\*]\s(.+)$/gm, '<li>▸ $1</li>')
        // Paragraphs
        .split('\n\n')
        .map(para => {
            if (para.includes('<li>')) {
                return '<ul>' + para + '</ul>';
            } else if (para.includes('<h')) {
                return para;
            } else if (para.trim()) {
                return '<p>' + para + '</p>';
            }
            return '';
        })
        .join('');
    
    // Clean up nested lists
    formatted = formatted.replace(/<\/ul>\s*<ul>/g, '');
    
    return formatted;
}

// ============================================
// SHOW ERROR
// ============================================
function showError(message) {
    errorMessage.textContent = message || '⚠ Temporal anomaly detected. Please retry.';
    errorSection.style.display = 'block';
    errorSection.style.animation = 'fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ============================================
// FOCUS AND PLACEHOLDER ROTATION
// ============================================
window.addEventListener('load', () => {
    queryInput.focus();
});

// Rotating placeholder text with futuristic queries
const exampleQueries = [
    "▶ What are the quantum mechanics of reality?",
    "▶ How does temporal displacement work?",
    "▶ Explain the multiverse theory...",
    "▶ What is consciousness in AI systems?",
    "▶ Future of space-time manipulation..."
];

let placeholderIndex = 0;
setInterval(() => {
    placeholderIndex = (placeholderIndex + 1) % exampleQueries.length;
    queryInput.placeholder = exampleQueries[placeholderIndex];
}, 4000);

// ============================================
// HOLOGRAPHIC GLITCH EFFECT ON HOVER
// ============================================
const cards = document.querySelectorAll('.answer-card, .sources-card');
cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.animation = 'glitch 0.3s ease-in-out';
        setTimeout(() => {
            card.style.animation = '';
        }, 300);
    });
});

// ============================================
// KEYBOARD SHORTCUTS
// ============================================
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to focus search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        queryInput.focus();
        queryInput.select();
    }
});

// Add visual feedback to input on focus
queryInput.addEventListener('focus', () => {
    queryInput.style.animation = 'glitch 0.2s ease-in-out';
    setTimeout(() => {
        queryInput.style.animation = '';
    }, 200);
});

console.log('%c⚡ QUANTUM RESEARCH TERMINAL INITIALIZED ⚡', 'color: #00fff9; font-size: 20px; font-weight: bold; text-shadow: 0 0 20px #00fff9;');
console.log('%c[SYSTEM STATUS]: OPERATIONAL', 'color: #ffed4e; font-size: 14px; font-weight: bold;');
console.log('%c[TEMPORAL ENGINE]: ONLINE', 'color: #ff2a6d; font-size: 14px; font-weight: bold;');
console.log('%c[FUNK MODE]: MAXIMUM 🎨✨', 'color: #00ff88; font-size: 14px; font-weight: bold;');

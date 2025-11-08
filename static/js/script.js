// Auto-refresh stats every 30 seconds
setInterval(async () => {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        // Update stats if they've changed
        updateStat('guilds', data.guilds);
        updateStat('users', data.users);
        updateStat('channels', data.channels);
        
        // Update uptime
        const uptimeStr = formatUptime(data.uptime_seconds);
        const uptimeElements = document.querySelectorAll('.stat-card:nth-child(4) .stat-value');
        uptimeElements.forEach(el => el.textContent = uptimeStr);
        
    } catch (error) {
        console.error('Failed to fetch stats:', error);
    }
}, 30000);

function updateStat(statName, value) {
    const statMap = {
        'guilds': 1,
        'users': 2,
        'channels': 3
    };
    
    const index = statMap[statName];
    const element = document.querySelector(`.stat-card:nth-child(${index}) .stat-value`);
    
    if (element && element.textContent !== value.toString()) {
        // Animate the change
        element.style.transform = 'scale(1.2)';
        element.style.color = '#ff006e';
        
        setTimeout(() => {
            element.textContent = value;
            element.style.transform = 'scale(1)';
            element.style.color = 'var(--neon-cyan)';
        }, 200);
    }
}

function formatUptime(seconds) {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    return `${days}d ${hours}h ${minutes}m ${secs}s`;
}

// Add scroll animations
document.addEventListener('DOMContentLoaded', () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    });

    document.querySelectorAll('.stat-card, .feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
});

// Cyber grid effect on mouse move
document.addEventListener('mousemove', (e) => {
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    document.querySelector('.stars').style.transform = `translate(${x * 10}px, ${y * 10}px)`;
    document.querySelector('.stars2').style.transform = `translate(${x * 20}px, ${y * 20}px)`;
    document.querySelector('.stars3').style.transform = `translate(${x * 30}px, ${y * 30}px)`;
});

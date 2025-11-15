// Admin Dashboard JavaScript

const API_BASE = '';

// =============== LOAD STATISTICS ===============

async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/api/admin/stats`);
        const data = await response.json();
        
        // Update stat cards
        document.getElementById('statUsers').textContent = data.total_users || 0;
        document.getElementById('statNeeds').textContent = data.total_needs || 0;
        document.getElementById('statLearnings').textContent = data.total_learnings || 0;
        document.getElementById('statMatches').textContent = data.total_matches || 0;
        document.getElementById('statPendingMatches').textContent = data.pending_matches || 0;
        document.getElementById('statConfirmedChats').textContent = data.confirmed_chats || 0;
        
        // Render category charts
        renderCategoryChart('needsChart', data.need_categories || {});
        renderCategoryChart('learningsChart', data.learning_categories || {});
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function renderCategoryChart(containerId, categories) {
    const container = document.getElementById(containerId);
    
    if (Object.keys(categories).length === 0) {
        container.innerHTML = '<p style="color: #6b7280; text-align: center; padding: 2rem;">No data yet</p>';
        return;
    }
    
    // Get max value for scaling
    const maxValue = Math.max(...Object.values(categories));
    
    // Sort by value
    const sortedCategories = Object.entries(categories).sort((a, b) => b[1] - a[1]);
    
    const html = sortedCategories.map(([category, count]) => {
        const percentage = (count / maxValue) * 100;
        return `
            <div class="category-bar">
                <div class="category-label">${category}</div>
                <div class="category-bar-fill">
                    <div class="category-bar-progress" style="width: ${percentage}%">
                        ${count}
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = html;
}

// =============== LOAD NEEDS ===============

async function loadNeeds() {
    try {
        const response = await fetch(`${API_BASE}/api/admin/needs`);
        const data = await response.json();
        
        const tbody = document.querySelector('#needsTable tbody');
        
        if (data.needs && data.needs.length > 0) {
            tbody.innerHTML = data.needs.map(need => {
                const user = need.user || { name: 'Unknown', company: '' };
                return `
                    <tr>
                        <td>
                            <strong>${user.name}</strong><br>
                            <small style="color: #6b7280;">${user.company}</small>
                        </td>
                        <td>${need.label}</td>
                        <td>
                            <span class="badge badge-${need.category}">${need.category}</span>
                        </td>
                        <td>${formatDate(need.created_at)}</td>
                    </tr>
                `;
            }).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #6b7280;">No needs yet</td></tr>';
        }
    } catch (error) {
        console.error('Error loading needs:', error);
        const tbody = document.querySelector('#needsTable tbody');
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #ef4444;">Error loading needs</td></tr>';
    }
}

// =============== LOAD LEARNINGS ===============

async function loadLearnings() {
    try {
        const response = await fetch(`${API_BASE}/api/admin/learnings`);
        const data = await response.json();
        
        const tbody = document.querySelector('#learningsTable tbody');
        
        if (data.learnings && data.learnings.length > 0) {
            tbody.innerHTML = data.learnings.map(learning => {
                const user = learning.user || { name: 'Unknown', company: '' };
                return `
                    <tr>
                        <td>
                            <strong>${user.name}</strong><br>
                            <small style="color: #6b7280;">${user.company}</small>
                        </td>
                        <td>${learning.label}</td>
                        <td>
                            <span class="badge badge-${learning.category}">${learning.category}</span>
                        </td>
                        <td>${formatDate(learning.created_at)}</td>
                    </tr>
                `;
            }).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #6b7280;">No learnings yet</td></tr>';
        }
    } catch (error) {
        console.error('Error loading learnings:', error);
        const tbody = document.querySelector('#learningsTable tbody');
        tbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #ef4444;">Error loading learnings</td></tr>';
    }
}

// =============== LOAD MATCHES ===============

async function loadMatches() {
    try {
        const response = await fetch(`${API_BASE}/api/admin/matches`);
        const data = await response.json();
        
        const tbody = document.querySelector('#matchesTable tbody');
        
        if (data.matches && data.matches.length > 0) {
            tbody.innerHTML = data.matches.map(match => {
                const requester = match.requester || { name: 'Unknown', company: '' };
                const expert = match.expert || { name: 'Unknown', company: '' };
                return `
                    <tr>
                        <td>
                            <strong>${requester.name}</strong><br>
                            <small style="color: #6b7280;">${requester.company}</small>
                        </td>
                        <td>
                            <strong>${expert.name}</strong><br>
                            <small style="color: #6b7280;">${expert.company}</small>
                        </td>
                        <td>
                            <strong style="color: #6366f1;">${Math.round(match.score * 100)}%</strong>
                        </td>
                        <td>
                            <span class="badge ${getStatusBadgeClass(match.status)}">${match.status}</span>
                        </td>
                        <td>${formatDate(match.created_at)}</td>
                    </tr>
                `;
            }).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #6b7280;">No matches yet</td></tr>';
        }
    } catch (error) {
        console.error('Error loading matches:', error);
        const tbody = document.querySelector('#matchesTable tbody');
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #ef4444;">Error loading matches</td></tr>';
    }
}

// =============== LOAD COFFEE CHATS ===============

async function loadCoffeeChats() {
    try {
        const response = await fetch(`${API_BASE}/api/admin/coffee-chats`);
        const data = await response.json();
        
        const tbody = document.querySelector('#chatsTable tbody');
        
        if (data.coffee_chats && data.coffee_chats.length > 0) {
            tbody.innerHTML = data.coffee_chats.map(chat => {
                const requester = chat.requester || { name: 'Unknown', company: '' };
                const expert = chat.expert || { name: 'Unknown', company: '' };
                return `
                    <tr>
                        <td>
                            <strong>${requester.name}</strong><br>
                            <small style="color: #6b7280;">${requester.company}</small>
                        </td>
                        <td>
                            <strong>${expert.name}</strong><br>
                            <small style="color: #6b7280;">${expert.company}</small>
                        </td>
                        <td>
                            <span class="badge ${getStatusBadgeClass(chat.status)}">${chat.status.replace('_', ' ')}</span>
                        </td>
                        <td>
                            ${chat.scheduled_time ? formatDateTime(chat.scheduled_time) : '-'}
                        </td>
                        <td>${formatDate(chat.created_at)}</td>
                    </tr>
                `;
            }).join('');
        } else {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #6b7280;">No coffee chats yet</td></tr>';
        }
    } catch (error) {
        console.error('Error loading coffee chats:', error);
        const tbody = document.querySelector('#chatsTable tbody');
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #ef4444;">Error loading coffee chats</td></tr>';
    }
}

// =============== UTILITY FUNCTIONS ===============

function formatDate(isoString) {
    if (!isoString) return '-';
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
    });
}

function formatDateTime(isoString) {
    if (!isoString) return '-';
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

function getStatusBadgeClass(status) {
    const statusMap = {
        'pending': 'badge-fundraising',
        'accepted': 'badge-product',
        'declined': 'badge-marketing',
        'confirmed': 'badge-product',
        'pending_slots': 'badge-fundraising',
        'pending_confirmation': 'badge-fundraising',
        'cancelled': 'badge-marketing'
    };
    return statusMap[status] || 'badge-technical';
}

// =============== INITIALIZATION ===============

async function initDashboard() {
    console.log('Loading admin dashboard...');
    
    await Promise.all([
        loadStats(),
        loadNeeds(),
        loadLearnings(),
        loadMatches(),
        loadCoffeeChats()
    ]);
    
    console.log('✅ Admin dashboard loaded');
}

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', initDashboard);

// Auto-refresh every 30 seconds
setInterval(initDashboard, 30000);











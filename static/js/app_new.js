// Configuration
const API_BASE = '';

// State
let currentChatForSlots = null;
let recognition = null;
let isRecording = false;

// DOM Elements
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');
const checkinForm = document.getElementById('checkinForm');
const transcriptInput = document.getElementById('transcript');
const charCount = document.getElementById('charCount');
const exampleBtn = document.getElementById('exampleBtn');
const voiceBtn = document.getElementById('voiceBtn');
const voiceStatus = document.getElementById('voiceStatus');

// Example transcripts for different languages
const exampleTranscripts = {
    'en-US': `This week I've been working on deploying our machine learning recommendation model to production. The model works great in development - we're getting 95% accuracy.

But here's where I'm stuck: when I try to deploy it and serve predictions to real users, the response times are terrible - like 5+ seconds per prediction. And when multiple users hit it at once, it just crashes.

I think I need to containerize it with Docker and set up load balancing, but I've never done MLOps at scale before. Our data pipeline is also a mess - it takes hours to retrain.

On the bright side, I figured out how to do proper A/B testing and set up our analytics pipeline. We're now tracking user behavior end-to-end, which is helping us make better product decisions.`,
    
    'de-DE': `Diese Woche habe ich an der Bereitstellung unseres Machine-Learning-Empfehlungsmodells gearbeitet. Das Modell funktioniert in der Entwicklung großartig - wir erreichen 95% Genauigkeit.

Aber hier hänge ich fest: Wenn ich versuche, es bereitzustellen und Vorhersagen für echte Benutzer zu liefern, sind die Antwortzeiten schrecklich - etwa 5+ Sekunden pro Vorhersage. Und wenn mehrere Benutzer gleichzeitig zugreifen, stürzt es einfach ab.

Ich denke, ich muss es mit Docker containerisieren und Load Balancing einrichten, aber ich habe noch nie MLOps in großem Maßstab gemacht. Unsere Datenpipeline ist auch ein Chaos - es dauert Stunden zum Neutrainieren.

Auf der positiven Seite habe ich herausgefunden, wie man richtige A/B-Tests durchführt und unsere Analytics-Pipeline einrichtet. Wir verfolgen jetzt das Benutzerverhalten von Ende zu Ende, was uns hilft, bessere Produktentscheidungen zu treffen.`,
    
    'es-ES': `Esta semana he estado trabajando en implementar nuestro modelo de recomendación de machine learning en producción. El modelo funciona muy bien en desarrollo - obtenemos un 95% de precisión.

Pero aquí es donde estoy atascado: cuando intento implementarlo y servir predicciones a usuarios reales, los tiempos de respuesta son terribles - como más de 5 segundos por predicción. Y cuando múltiples usuarios lo usan a la vez, simplemente se cae.

Creo que necesito containerizarlo con Docker y configurar balanceo de carga, pero nunca he hecho MLOps a escala antes. Nuestra pipeline de datos también es un desastre - toma horas reentrenar.

En el lado positivo, descubrí cómo hacer pruebas A/B adecuadas y configurar nuestra pipeline de análisis. Ahora estamos rastreando el comportamiento del usuario de principio a fin, lo que nos ayuda a tomar mejores decisiones de producto.`,
    
    'fr-FR': `Cette semaine, j'ai travaillé sur le déploiement de notre modèle de recommandation d'apprentissage automatique en production. Le modèle fonctionne très bien en développement - nous obtenons 95% de précision.

Mais voici où je suis bloqué : quand j'essaie de le déployer et de servir des prédictions aux vrais utilisateurs, les temps de réponse sont terribles - environ 5+ secondes par prédiction. Et quand plusieurs utilisateurs y accèdent en même temps, ça plante tout simplement.

Je pense que je dois le containeriser avec Docker et configurer l'équilibrage de charge, mais je n'ai jamais fait de MLOps à grande échelle auparavant. Notre pipeline de données est aussi un désastre - ça prend des heures pour réentraîner.

Du côté positif, j'ai découvert comment faire des tests A/B appropriés et configurer notre pipeline d'analyse. Nous suivons maintenant le comportement des utilisateurs de bout en bout, ce qui nous aide à prendre de meilleures décisions produit.`
};

const exampleTranscript = exampleTranscripts['en-US']; // Default

// Placeholder texts for different languages
const placeholderTexts = {
    'en-US': "Example: This week I've been working on deploying our ML model to production. I'm stuck on scaling issues - the response time is terrible when multiple users hit it. I think I need help with MLOps and containerization. On the bright side, I figured out how to optimize our data pipeline and reduced processing time by 40%...",
    'de-DE': "Beispiel: Diese Woche habe ich an der Bereitstellung unseres ML-Modells in die Produktion gearbeitet. Ich hänge bei Skalierungsproblemen fest - die Antwortzeit ist schrecklich, wenn mehrere Benutzer darauf zugreifen. Ich denke, ich brauche Hilfe bei MLOps und Containerisierung. Auf der positiven Seite habe ich herausgefunden, wie man unsere Datenpipeline optimiert und die Verarbeitungszeit um 40% reduziert...",
    'es-ES': "Ejemplo: Esta semana he estado trabajando en implementar nuestro modelo ML en producción. Estoy atascado con problemas de escalabilidad - el tiempo de respuesta es terrible cuando múltiples usuarios lo usan. Creo que necesito ayuda con MLOps y containerización. En el lado positivo, descubrí cómo optimizar nuestra pipeline de datos y reduje el tiempo de procesamiento en un 40%...",
    'fr-FR': "Exemple: Cette semaine, j'ai travaillé sur le déploiement de notre modèle ML en production. Je suis bloqué sur des problèmes d'échelle - le temps de réponse est terrible quand plusieurs utilisateurs y accèdent. Je pense avoir besoin d'aide avec MLOps et la containerisation. Du côté positif, j'ai découvert comment optimiser notre pipeline de données et réduit le temps de traitement de 40%..."
};

// Function to update placeholder text based on selected language
function updatePlaceholder(lang) {
    if (transcriptInput && placeholderTexts[lang]) {
        transcriptInput.placeholder = placeholderTexts[lang];
    }
}

// =============== TAB NAVIGATION ===============

tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const tabName = tab.dataset.tab;
        
        // Update active tab
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Update active content
        tabContents.forEach(tc => tc.classList.remove('active'));
        document.getElementById(`${tabName}-tab`).classList.add('active');
        
        // Load data for the tab
        if (tabName === 'matches') {
            loadMyMatches();
        } else if (tabName === 'help-requests') {
            loadHelpRequests();
        } else if (tabName === 'coffee-chats') {
            loadCoffeeChats();
        } else if (tabName === 'profile') {
            loadUserProfile();
        } else if (tabName === 'community') {
            loadCommunityStats();
        }
    });
});

// =============== UTILITY FUNCTIONS ===============

// Get current user ID from session
async function getCurrentUserId() {
    try {
        const response = await fetch(`${API_BASE}/api/current-user`);
        if (!response.ok) {
            window.location.href = '/login';
            return null;
        }
        const data = await response.json();
        return data.user_id;
    } catch (error) {
        console.error('Error getting current user:', error);
        window.location.href = '/login';
        return null;
    }
}

// =============== CHECK-IN SUBMISSION ===============

// Character counter
transcriptInput.addEventListener('input', () => {
    charCount.textContent = transcriptInput.value.length;
});

// Example button - uses the currently selected language
exampleBtn.addEventListener('click', () => {
    const selectedLang = document.querySelector('.lang-btn.active')?.dataset.lang || 'en-US';
    const example = exampleTranscripts[selectedLang];
    transcriptInput.value = example;
    charCount.textContent = example.length;
    transcriptInput.focus();
});

// =============== VOICE INPUT ===============

// Initialize Speech Recognition
function initVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        
        let finalTranscript = '';
        let interimTranscript = '';
        
        recognition.onstart = () => {
            isRecording = true;
            voiceBtn.style.background = '#ef4444';
            voiceBtn.innerHTML = '⏹️';
            voiceStatus.textContent = '🔴 Recording... (click to stop)';
            voiceStatus.style.color = '#ef4444';
            finalTranscript = transcriptInput.value;
        };
        
        recognition.onresult = (event) => {
            interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += (finalTranscript ? ' ' : '') + transcript;
                } else {
                    interimTranscript += transcript;
                }
            }
            
            transcriptInput.value = finalTranscript + (interimTranscript ? ' ' + interimTranscript : '');
            charCount.textContent = transcriptInput.value.length;
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            stopRecording();
            
            if (event.error === 'not-allowed') {
                voiceStatus.textContent = '❌ Microphone access denied';
                alert('Please allow microphone access to use voice input');
            } else if (event.error === 'no-speech') {
                voiceStatus.textContent = '🎤 No speech detected';
            } else {
                voiceStatus.textContent = `❌ Error: ${event.error}`;
            }
        };
        
        recognition.onend = () => {
            if (isRecording) {
                stopRecording();
            }
        };
        
        return true;
    } else {
        console.warn('Speech recognition not supported');
        voiceBtn.disabled = true;
        voiceBtn.style.opacity = '0.5';
        voiceBtn.title = 'Voice input not supported in this browser';
        return false;
    }
}

function startRecording() {
    if (!recognition) {
        if (!initVoiceRecognition()) {
            alert('Voice recognition is not supported in your browser. Please use Chrome, Edge, or Safari.');
            return;
        }
    }
    
    try {
        recognition.start();
    } catch (e) {
        console.error('Error starting recognition:', e);
    }
}

function stopRecording() {
    if (recognition && isRecording) {
        recognition.stop();
        isRecording = false;
        voiceBtn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        voiceBtn.innerHTML = '🎤';
        voiceStatus.textContent = '✓ Voice input stopped';
        voiceStatus.style.color = '#10b981';
        
        setTimeout(() => {
            voiceStatus.textContent = '';
        }, 3000);
    }
}

// Voice button click handler
if (voiceBtn) {
    voiceBtn.addEventListener('click', () => {
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    });
}

// Initialize voice recognition on page load
if (voiceBtn) {
    initVoiceRecognition();
}

// Language selector
const langButtons = document.querySelectorAll('.lang-btn');
langButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent any default button behavior
        e.stopPropagation(); // Stop event from bubbling
        
        const selectedLang = btn.dataset.lang;
        
        // Update active state
        langButtons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        
        // Update placeholder text
        updatePlaceholder(selectedLang);
        
        // Update recognition language if initialized
        if (recognition) {
            recognition.lang = selectedLang;
        }
        
        // Show status message
        const langNames = {
            'en-US': 'English',
            'de-DE': 'Deutsch',
            'es-ES': 'Español',
            'fr-FR': 'Français'
        };
        if (voiceStatus) {
            voiceStatus.textContent = `✓ Language: ${langNames[selectedLang]}`;
            voiceStatus.style.color = '#10b981';
            setTimeout(() => {
                voiceStatus.textContent = '';
            }, 2000);
        }
    });
});

// Form submission
checkinForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const transcript = transcriptInput.value.trim();
    
    if (transcript.length < 20) {
        alert('Please provide a longer check-in (at least 20 characters)');
        return;
    }
    
    await submitCheckin(transcript);
});

async function submitCheckin(text) {
    try {
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-text').textContent = '🤖 Analyzing...';
        
        const response = await fetch(`${API_BASE}/api/submit-checkin`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text
                // user_id is now handled by session on backend
            }),
        });
        
        if (!response.ok) {
            throw new Error('Failed to submit check-in');
        }
        
        const data = await response.json();
        
        // Show XP notification
        showXPNotification(
            data.xp_gained || 0,
            data.total_xp || 0,
            data.level || 1,
            data.leveled_up || false,
            data.new_badges || []
        );
        
        // Show results
        displaySubmissionResults(data);
        
        // Clear form
        transcriptInput.value = '';
        charCount.textContent = '0';
        
        submitBtn.disabled = false;
        submitBtn.querySelector('.btn-text').textContent = '🤖 Analyze & Find Matches';
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error submitting check-in: ' + error.message);
        
        const submitBtn = document.getElementById('submitBtn');
        submitBtn.disabled = false;
        submitBtn.querySelector('.btn-text').textContent = '🤖 Analyze & Find Matches';
    }
}

function displaySubmissionResults(data) {
    const resultsDiv = document.getElementById('submissionResults');
    const infoDiv = document.getElementById('extractedInfo');
    
    let html = `
        <div style="background: #f0f9ff; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
            <p><strong>Summary:</strong> ${data.summary}</p>
            
            <div style="margin-top: 1rem;">
                <strong>🎯 Your Needs:</strong>
                <div class="needs-list" style="margin-top: 0.5rem;">
                    ${data.needs.map(need => `
                        <span class="need-tag">${need.label} <small>(${need.category})</small></span>
                    `).join('')}
                </div>
            </div>
            
            <div style="margin-top: 1rem;">
                <strong>💡 Your Learnings:</strong>
                <div class="needs-list" style="margin-top: 0.5rem;">
                    ${data.learnings.map(learning => `
                        <span class="need-tag" style="background: #d1fae5;">${learning.label} <small>(${learning.category})</small></span>
                    `).join('')}
                </div>
            </div>
            
            ${data.skills && data.skills.length > 0 ? `
                <div style="margin-top: 1rem;">
                    <strong>🎓 Your Skill Profile (${data.skills.length} skills):</strong>
                    <p style="margin-top: 0.25rem; font-size: 0.875rem; color: #6b7280;">These skills help us match you with founders who need your help</p>
                    <div class="needs-list" style="margin-top: 0.5rem;">
                        ${data.skills.slice(0, 5).map(skill => `
                            <span class="need-tag" style="background: #ddd6fe; color: #5b21b6;">${skill.label} <small>(${skill.category})</small></span>
                        `).join('')}
                        ${data.skills.length > 5 ? `<span style="color: #6b7280; font-size: 0.875rem;">+${data.skills.length - 5} more</span>` : ''}
                    </div>
                </div>
            ` : ''}
            
            ${data.matches && data.matches.length > 0 ? `
                <div style="margin-top: 1rem;">
                    <strong>👥 Matched Founders:</strong>
                    <p style="margin-top: 0.5rem; color: #6b7280;">Found ${data.matches.length} potential matches! Check the "My Matches" tab to connect.</p>
                </div>
            ` : ''}
        </div>
        
        <button class="btn btn-primary" onclick="document.querySelectorAll('.tab')[1].click()" style="margin-top: 1rem;">
            View My Matches →
        </button>
    `;
    
    infoDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

// =============== MY MATCHES (People who can help me) ===============

async function loadMyMatches() {
    const listDiv = document.getElementById('myMatchesList');
    
    try {
        const userId = await getCurrentUserId();
        if (!userId) return;
        
        const response = await fetch(`${API_BASE}/api/matches/${userId}`);
        const data = await response.json();
        
        if (data.matches && data.matches.length > 0) {
            listDiv.innerHTML = data.matches.map(match => {
                const expert = match.expert;
                const need = match.need;
                
                return `
                    <div class="match-card">
                        <div class="match-header">
                            <div>
                                <h3 style="margin: 0 0 0.5rem 0;">${expert.name}</h3>
                                <p style="color: #6b7280; margin: 0;">${expert.company}</p>
                            </div>
                            <div class="match-score">${Math.round(match.score * 100)}% Match</div>
                        </div>
                        
                        <div style="background: #f9fafb; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <strong>Your Need:</strong> ${need.label}
                        </div>
                        
                        <div style="color: #6b7280; margin-bottom: 1rem;">
                            <strong>💡 Why this match:</strong><br>
                            ${match.reason}
                        </div>
                        
                        <div class="status-badge status-${match.status}">
                            ${match.status}
                        </div>
                        
                        ${match.status === 'pending' ? `
                            <p style="margin-top: 1rem; font-size: 0.875rem; color: #6b7280;">
                                Waiting for ${expert.name} to accept your match request...
                            </p>
                        ` : match.status === 'accepted' ? `
                            <p style="margin-top: 1rem; color: #10b981;">
                                ✅ Match accepted! Check Coffee Chats tab for scheduling.
                            </p>
                        ` : ''}
                    </div>
                `;
            }).join('');
        } else {
            listDiv.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🔍</div>
                    <p>No matches yet. Submit a check-in to find expert founders!</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading matches:', error);
        listDiv.innerHTML = '<p style="color: #ef4444;">Error loading matches</p>';
    }
}

// =============== HELP REQUESTS (People who need my help) ===============

async function loadHelpRequests() {
    const listDiv = document.getElementById('helpRequestsList');
    
    try {
        const userId = await getCurrentUserId();
        if (!userId) return;
        
        const response = await fetch(`${API_BASE}/api/matches/expert/${userId}`);
        const data = await response.json();
        
        if (data.matches && data.matches.length > 0) {
            listDiv.innerHTML = data.matches.map(match => {
                const requester = match.requester;
                const need = match.need;
                
                return `
                    <div class="match-card">
                        <div class="match-header">
                            <div>
                                <h3 style="margin: 0 0 0.5rem 0;">${requester.name}</h3>
                                <p style="color: #6b7280; margin: 0;">${requester.company}</p>
                            </div>
                            <div class="match-score">${Math.round(match.score * 100)}% Match</div>
                        </div>
                        
                        <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                            <strong>They Need Help With:</strong><br>
                            ${need.label}
                        </div>
                        
                        <div style="color: #6b7280; margin-bottom: 1rem;">
                            <strong>💡 Why you can help:</strong><br>
                            ${match.reason}
                        </div>
                        
                        <div class="status-badge status-${match.status}">
                            ${match.status}
                        </div>
                        
                        ${match.status === 'pending' ? `
                            <div class="match-actions">
                                <button class="btn btn-accept" onclick="acceptMatch('${match.id}')">
                                    ✅ Accept & Schedule Chat
                                </button>
                                <button class="btn btn-decline" onclick="declineMatch('${match.id}')">
                                    ❌ Decline
                                </button>
                            </div>
                        ` : match.status === 'accepted' ? `
                            <p style="margin-top: 1rem; color: #10b981;">
                                ✅ Match accepted! Check Coffee Chats tab to propose time slots.
                            </p>
                        ` : ''}
                    </div>
                `;
            }).join('');
        } else {
            listDiv.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">💪</div>
                    <p>No help requests yet. Share your learnings in your check-ins to help others!</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading help requests:', error);
        listDiv.innerHTML = '<p style="color: #ef4444;">Error loading help requests</p>';
    }
}

async function acceptMatch(matchId) {
    try {
        const response = await fetch(`${API_BASE}/api/matches/${matchId}/accept`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.xp_gained) {
                alert(`✅ Match accepted! +${data.xp_gained} XP earned!\n\nRedirecting to coffee chats to propose time slots...`);
            } else {
                alert('Match accepted! Redirecting to coffee chats to propose time slots...');
            }
            // Switch to coffee chats tab
            document.querySelectorAll('.tab')[3].click();
        } else {
            alert('Error accepting match');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error accepting match');
    }
}

async function declineMatch(matchId) {
    if (!confirm('Are you sure you want to decline this match?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/matches/${matchId}/decline`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok) {
            alert('Match declined');
            loadHelpRequests();
        } else {
            alert('Error declining match');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error declining match');
    }
}

// =============== COFFEE CHATS ===============

async function loadCoffeeChats() {
    const listDiv = document.getElementById('coffeeChatsList');
    
    try {
        const userId = await getCurrentUserId();
        if (!userId) return;
        
        const response = await fetch(`${API_BASE}/api/coffee-chats/${userId}`);
        const data = await response.json();
        
        if (data.coffee_chats && data.coffee_chats.length > 0) {
            // Filter out completed chats and separate past meetings
            const now = new Date();
            const activeChats = data.coffee_chats.filter(chat => {
                if (chat.status === 'completed') return false;
                if (chat.status === 'confirmed' && chat.scheduled_time) {
                    const meetingTime = new Date(chat.scheduled_time);
                    // Hide if meeting was more than 1 hour ago
                    return (now - meetingTime) < (60 * 60 * 1000);
                }
                return true;
            });
            
            if (activeChats.length === 0) {
                listDiv.innerHTML = `
                    <div class="empty-state">
                        <div class="empty-state-icon">☕</div>
                        <p>No active coffee chats</p>
                    </div>
                `;
                return;
            }
            
            listDiv.innerHTML = activeChats.map(chat => {
                const isExpert = chat.expert_id === userId;
                const otherPerson = isExpert ? chat.requester : chat.expert;
                const role = isExpert ? 'Expert' : 'Requester';
                
                return `
                    <div class="coffee-chat-card">
                        <div class="match-header">
                            <div>
                                <h3 style="margin: 0 0 0.5rem 0;">☕ Coffee Chat with ${otherPerson.name}</h3>
                                <p style="color: #6b7280; margin: 0;">${otherPerson.company} • Your role: ${role}</p>
                            </div>
                            <div class="status-badge status-${chat.status.replace('_', '-')}">
                                ${chat.status.replace('_', ' ')}
                            </div>
                        </div>
                        
                        ${chat.status === 'pending_slots' && isExpert ? `
                            <p style="margin-top: 1rem; color: #6b7280;">Please propose 3 time slots for this chat</p>
                            <button class="btn btn-primary" onclick="openProposeSlotModal('${chat.id}')">
                                📅 Propose Time Slots
                            </button>
                        ` : chat.status === 'pending_confirmation' && !isExpert ? `
                            <p style="margin-top: 1rem; color: #6b7280;">Please select a time slot:</p>
                            <div class="time-slots">
                                ${chat.proposed_slots.filter(s => s.status === 'pending').map(slot => `
                                    <div class="time-slot" onclick="selectTimeSlot('${chat.id}', '${slot.id}')">
                                        📅 ${formatDateTime(slot.slot_time)}
                                    </div>
                                `).join('')}
                            </div>
                        ` : chat.status === 'confirmed' ? `
                            <div style="background: #d1fae5; padding: 1.5rem; border-radius: 12px; margin-top: 1rem; border: 2px solid #10b981;">
                                <p style="margin: 0 0 1rem 0; font-size: 1.1rem;"><strong>✅ Meeting Confirmed!</strong></p>
                                <p style="margin: 0 0 0.75rem 0;"><strong>📅 Time:</strong> ${formatDateTime(chat.scheduled_time)}</p>
                                <div style="background: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
                                    <p style="margin: 0 0 0.5rem 0; font-size: 0.875rem; color: #6b7280;"><strong>🎥 Video Meeting Link (Jitsi):</strong></p>
                                    <p style="margin: 0; font-family: monospace; font-size: 0.875rem; color: #4b5563; word-break: break-all;">${chat.meeting_link}</p>
                                </div>
                                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                                    <a href="${chat.meeting_link}" target="_blank" class="btn btn-primary" style="display: inline-block; text-decoration: none; background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);">
                                        🎥 Join Video Call
                                    </a>
                                    <button onclick="markChatComplete('${chat.id}')" class="btn" style="background: #6b7280; color: white; padding: 0.75rem 1.5rem; border-radius: 8px; font-weight: 600; border: none; cursor: pointer;">
                                        ✓ Mark as Complete
                                    </button>
                                </div>
                                <p style="margin-top: 0.75rem; font-size: 0.875rem; color: #6b7280;">💡 Tip: You can join directly from your browser, no account needed!</p>
                            </div>
                        ` : ''}
                        
                        <p style="margin-top: 1rem; font-size: 0.875rem; color: #9ca3af;">
                            Created: ${formatDateTime(chat.created_at)}
                        </p>
                    </div>
                `;
            }).join('');
        } else {
            listDiv.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">☕</div>
                    <p>No coffee chats scheduled yet</p>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading coffee chats:', error);
        listDiv.innerHTML = '<p style="color: #ef4444;">Error loading coffee chats</p>';
    }
}

// =============== TIME SLOT MANAGEMENT ===============

function openProposeSlotModal(chatId) {
    currentChatForSlots = chatId;
    
    // Set default values (next week, 2pm, 3pm, 4pm)
    const now = new Date();
    const nextWeek = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
    
    for (let i = 1; i <= 3; i++) {
        const slotDate = new Date(nextWeek);
        slotDate.setHours(13 + i, 0, 0, 0);
        document.getElementById(`slot${i}`).value = formatDateTimeLocal(slotDate);
    }
    
    document.getElementById('proposeSlotModal').style.display = 'flex';
}

document.getElementById('submitSlotsBtn')?.addEventListener('click', async () => {
    const slots = [
        document.getElementById('slot1').value,
        document.getElementById('slot2').value,
        document.getElementById('slot3').value
    ];
    
    if (slots.some(s => !s)) {
        alert('Please fill in all 3 time slots');
        return;
    }
    
    try {
        const userId = await getCurrentUserId();
        if (!userId) return;
        
        const response = await fetch(`${API_BASE}/api/coffee-chats/${currentChatForSlots}/propose-slots`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                slots: slots.map(s => new Date(s).toISOString()),
                user_id: userId
            }),
        });
        
        if (response.ok) {
            alert('Time slots proposed successfully!');
            document.getElementById('proposeSlotModal').style.display = 'none';
            loadCoffeeChats();
        } else {
            alert('Error proposing time slots');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error proposing time slots');
    }
});

document.getElementById('cancelSlotsBtn')?.addEventListener('click', () => {
    document.getElementById('proposeSlotModal').style.display = 'none';
});

async function selectTimeSlot(chatId, slotId) {
    if (!confirm('Confirm this time slot?')) {
        return;
    }
    
    try {
        const userId = await getCurrentUserId();
        if (!userId) return;
        
        const response = await fetch(`${API_BASE}/api/coffee-chats/${chatId}/select-slot`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                slot_id: slotId,
                user_id: userId
            }),
        });
        
        if (response.ok) {
            const data = await response.json();
            alert('✅ Time slot confirmed!\n\n🎥 Your Jitsi video call link is ready:\n' + data.meeting_link + '\n\nYou can join directly from your browser - no account needed!');
            loadCoffeeChats();
        } else {
            alert('Error selecting time slot');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error selecting time slot');
    }
}

async function markChatComplete(chatId) {
    if (!confirm('Mark this coffee chat as complete?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/coffee-chats/${chatId}/complete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        
        if (response.ok) {
            alert('✅ Coffee chat marked as complete!');
            loadCoffeeChats();
        } else {
            alert('Error marking chat as complete');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error marking chat as complete');
    }
}

// =============== UTILITY FUNCTIONS ===============

function formatDateTime(isoString) {
    if (!isoString) return 'Not set';
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

function formatDateTimeLocal(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}`;
}

// =============== INITIALIZATION ===============

// Modal styling
const style = document.createElement('style');
style.textContent = `
    .modal {
        display: none;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        justify-content: center;
        align-items: center;
        z-index: 1000;
    }
    
    .modal-content {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        max-width: 500px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
    }
    
    .form-control {
        width: 100%;
        padding: 0.5rem;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        font-size: 1rem;
    }
`;
document.head.appendChild(style);

// =============== USER PROFILE ===============

async function loadUserProfile() {
    try {
        const userId = await getCurrentUserId();
        if (!userId) return;
        
        const response = await fetch(`${API_BASE}/api/users/${userId}/profile`);
        if (!response.ok) throw new Error('Failed to load profile');
        
        const data = await response.json();
        
        // Update profile stats
        document.getElementById('profileLevel').textContent = data.level || 1;
        document.getElementById('profileXP').textContent = data.xp || 0;
        document.getElementById('profileCheckins').textContent = data.total_checkins || 0;
        document.getElementById('profileMatches').textContent = data.total_matches || 0;
        document.getElementById('profileChats').textContent = data.total_chats || 0;
        
        // Update XP bar with color transition from grey to green
        const xpProgress = data.profile.xp_progress || 0;
        const xpNeeded = data.profile.xp_needed || 100;
        const percentage = data.profile.progress_percentage || 0;
        const profileXPBar = document.getElementById('profileXPBar');
        profileXPBar.style.width = percentage + '%';
        
        // Transition color from grey to green based on progress
        if (percentage === 0) {
            profileXPBar.style.background = '#9ca3af'; // Grey at 0%
        } else if (percentage < 30) {
            profileXPBar.style.background = '#9ca3af'; // Grey for low XP
        } else if (percentage < 70) {
            profileXPBar.style.background = 'linear-gradient(90deg, #9ca3af 0%, #10b981 100%)'; // Gradient in middle
        } else {
            profileXPBar.style.background = '#10b981'; // Green for high XP
        }
        
        document.getElementById('profileXPText').textContent = `${xpProgress} / ${xpNeeded} XP to next level`;
        
        // Update badges
        const badgesContainer = document.getElementById('badgesContainer');
        const badges = data.badges || [];
        
        if (badges.length > 0) {
            badgesContainer.innerHTML = badges.map(badge => {
                const badgeIcons = {
                    'First Steps': '🎯',
                    'Rising Star': '⭐',
                    'Community Leader': '👑',
                    'Helper': '🤝',
                    'Expert': '🎓'
                };
                return `
                    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; min-width: 100px; box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);">
                        <div style="font-size: 2rem;">${badgeIcons[badge] || '🏆'}</div>
                        <div style="font-size: 0.875rem; margin-top: 0.5rem; font-weight: 600;">${badge}</div>
                    </div>
                `;
            }).join('');
        }
        
        // Update skills
        const skillsContainer = document.getElementById('skillsContainer');
        const skills = data.skills || [];
        
        if (skills.length > 0) {
            const categoryColors = {
                'technical': '#3b82f6',
                'product': '#10b981',
                'marketing': '#f59e0b',
                'fundraising': '#8b5cf6',
                'sales': '#ef4444',
                'UX': '#ec4899',
                'branding': '#06b6d4',
                'AI': '#6366f1',
                'hiring': '#14b8a6',
                'strategy': '#84cc16'
            };
            
            skillsContainer.innerHTML = `
                <div style="display: flex; flex-wrap: wrap; gap: 0.75rem;">
                    ${skills.map(skill => `
                        <div style="background: ${categoryColors[skill.category] || '#6b7280'}; color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.875rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <span style="font-weight: 600;">${skill.category}</span>: ${skill.label}
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        // Update bio
        document.getElementById('profileBio').value = data.bio || '';
        
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

// Save bio
document.getElementById('saveBioBtn')?.addEventListener('click', async () => {
    try {
        const userId = await getCurrentUserId();
        if (!userId) return;
        
        const bio = document.getElementById('profileBio').value;
        
        const response = await fetch(`${API_BASE}/api/users/${userId}/profile`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ bio }),
        });
        
        if (response.ok) {
            alert('✅ Bio saved successfully!');
        } else {
            alert('❌ Error saving bio');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('❌ Error saving bio');
    }
});

// =============== COMMUNITY STATS ===============

async function loadCommunityStats() {
    try {
        const response = await fetch(`${API_BASE}/api/community/stats`);
        if (!response.ok) throw new Error('Failed to load community stats');
        
        const data = await response.json();
        
        // Update weekly stats
        document.getElementById('statsNewUsers').textContent = data.new_users_this_week || 0;
        document.getElementById('statsMatches').textContent = data.matches_this_week || 0;
        document.getElementById('statsChats').textContent = data.chats_this_week || 0;
        
        // Update total stats
        document.getElementById('statsTotalUsers').textContent = data.total_users || 0;
        document.getElementById('statsTotalXP').textContent = data.total_xp_awarded || 0;
        
        // Update trending skills
        const trendingSkills = document.getElementById('trendingSkills');
        const topSkills = data.top_skills || [];
        
        if (topSkills.length > 0) {
            const categoryIcons = {
                'technical': '💻',
                'product': '📦',
                'marketing': '📈',
                'fundraising': '💰',
                'sales': '🤝',
                'UX': '🎨',
                'branding': '✨',
                'AI': '🤖',
                'hiring': '👥',
                'strategy': '🎯'
            };
            
            trendingSkills.innerHTML = topSkills.map((skill, index) => `
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: ${index === 0 ? '#fef3c7' : '#f9fafb'}; border-radius: 8px; margin-bottom: 0.5rem; border-left: 4px solid ${index === 0 ? '#f59e0b' : '#e5e7eb'};">
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <span style="font-size: 1.5rem;">${categoryIcons[skill.category] || '📌'}</span>
                        <span style="font-weight: 600; text-transform: capitalize;">${skill.category}</span>
                    </div>
                    <span style="background: ${index === 0 ? '#f59e0b' : '#6b7280'}; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.875rem; font-weight: 600;">${skill.count}</span>
                </div>
            `).join('');
        } else {
            trendingSkills.innerHTML = '<p style="color: #6b7280;">No skills data yet</p>';
        }
        
        // Update leaderboard
        const leaderboard = document.getElementById('leaderboard');
        const activeUsers = data.most_active_users || [];
        
        if (activeUsers.length > 0) {
            leaderboard.innerHTML = activeUsers.map((user, index) => {
                const medals = ['🥇', '🥈', '🥉'];
                const medal = medals[index] || '🏅';
                return `
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 1rem; background: ${index < 3 ? '#f0f9ff' : '#f9fafb'}; border-radius: 8px; margin-bottom: 0.5rem;">
                        <div style="display: flex; align-items: center; gap: 1rem;">
                            <span style="font-size: 1.5rem;">${medal}</span>
                            <div>
                                <div style="font-weight: 600;">${user.name}</div>
                                <div style="font-size: 0.875rem; color: #6b7280;">Level ${user.level} • ${user.xp} XP</div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 1.25rem; font-weight: bold; color: #6366f1;">${user.activity_score}</div>
                            <div style="font-size: 0.75rem; color: #6b7280;">Activity</div>
                        </div>
                    </div>
                `;
            }).join('');
        } else {
            leaderboard.innerHTML = '<p style="color: #6b7280;">No activity yet</p>';
        }
        
    } catch (error) {
        console.error('Error loading community stats:', error);
    }
}

// Update XP bar in header after actions
function updateHeaderXP(xp, level) {
    const xpPerLevel = 100;
    const xpProgress = xp % xpPerLevel;
    const percentage = (xpProgress / xpPerLevel) * 100;
    
    document.getElementById('userLevel').textContent = `Lv. ${level}`;
    const xpBar = document.getElementById('xpBar');
    xpBar.style.width = percentage + '%';
    
    // Transition color from grey to green based on progress
    if (percentage === 0) {
        xpBar.style.background = '#9ca3af'; // Grey at 0%
    } else if (percentage < 30) {
        xpBar.style.background = '#9ca3af'; // Grey for low XP
    } else if (percentage < 70) {
        xpBar.style.background = 'linear-gradient(90deg, #9ca3af 0%, #10b981 100%)'; // Gradient in middle
    } else {
        xpBar.style.background = '#10b981'; // Green for high XP
    }
    
    document.getElementById('xpText').textContent = `${xp} XP`;
}

// Show XP gain notification
function showXPNotification(xpGained, totalXP, level, leveledUp, newBadges) {
    if (xpGained > 0) {
        let message = `🎉 +${xpGained} XP earned!`;
        if (leveledUp) {
            message += `\n🎊 Level Up! You're now Level ${level}!`;
        }
        if (newBadges && newBadges.length > 0) {
            message += `\n🏆 New badge: ${newBadges.join(', ')}`;
        }
        alert(message);
        updateHeaderXP(totalXP, level);
    }
}

// Initialize placeholder text on page load
updatePlaceholder('en-US');

console.log('✅ Founder Matching Platform loaded');




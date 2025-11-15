// DOM Elements
const checkinForm = document.getElementById('checkinForm');
const transcriptInput = document.getElementById('transcript');
const charCount = document.getElementById('charCount');
const submitBtn = document.getElementById('submitBtn');
const exampleBtn = document.getElementById('exampleBtn');
const newCheckInBtn = document.getElementById('newCheckIn');
const retryBtn = document.getElementById('retryBtn');

// Sections
const inputSection = document.getElementById('inputSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

// Example transcript
const exampleTranscript = `Hey team, weekly check-in here. This week I've been working on getting our machine learning recommendation model into production. The model works great in development - we're getting 95% accuracy on our test set.

But here's where I'm stuck: when I try to deploy it and serve predictions to real users, everything falls apart. The response times are terrible - like 5+ seconds per prediction. And when multiple users hit it at once, it just crashes.

I think I need to containerize it with Docker and maybe set up some kind of load balancing? But I've never done MLOps at scale before. Our data pipeline is also a mess - it takes hours to retrain the model on new data.

Really need someone who's built production ML systems before and knows about data engineering, model serving, and scaling. Any help would be amazing!`;

// Character counter
transcriptInput.addEventListener('input', () => {
    charCount.textContent = transcriptInput.value.length;
});

// Example button
exampleBtn.addEventListener('click', () => {
    transcriptInput.value = exampleTranscript;
    charCount.textContent = exampleTranscript.length;
    transcriptInput.focus();
});

// Form submission
checkinForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const transcript = transcriptInput.value.trim();
    
    if (transcript.length < 20) {
        showError('Please provide a longer check-in (at least 20 characters)');
        return;
    }
    
    await analyzeCheckin(transcript);
});

// New check-in button
newCheckInBtn.addEventListener('click', () => {
    showSection('input');
    transcriptInput.value = '';
    charCount.textContent = '0';
    transcriptInput.focus();
});

// Retry button
retryBtn.addEventListener('click', () => {
    showSection('input');
});

// Show specific section
function showSection(section) {
    inputSection.style.display = 'none';
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    switch (section) {
        case 'input':
            inputSection.style.display = 'block';
            break;
        case 'loading':
            loadingSection.style.display = 'block';
            animateLoadingSteps();
            break;
        case 'results':
            resultsSection.style.display = 'block';
            break;
        case 'error':
            errorSection.style.display = 'block';
            break;
    }
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Animate loading steps
function animateLoadingSteps() {
    const steps = document.querySelectorAll('.loading-step');
    steps.forEach((step, index) => {
        step.classList.remove('active');
    });
    
    let currentStep = 0;
    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            steps[currentStep].classList.add('active');
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 800);
}

// Analyze check-in
async function analyzeCheckin(transcript) {
    try {
        showSection('loading');
        
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ transcript }),
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to analyze check-in');
        }
        
        const data = await response.json();
        
        // Small delay for better UX
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        displayResults(data);
        showSection('results');
        
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Something went wrong. Please try again.');
    }
}

// Display results
function displayResults(data) {
    // Summary
    document.getElementById('summaryText').textContent = data.summary;
    
    // Needs
    const needsList = document.getElementById('needsList');
    needsList.innerHTML = '';
    data.needs.forEach((need, index) => {
        const tag = document.createElement('div');
        tag.className = 'need-tag';
        tag.textContent = need;
        tag.style.animationDelay = `${index * 0.1}s`;
        needsList.appendChild(tag);
    });
    
    // Matched Founders
    const foundersGrid = document.getElementById('foundersGrid');
    foundersGrid.innerHTML = '';
    
    data.matchedFounders.forEach((founder, index) => {
        const card = document.createElement('div');
        card.className = 'founder-card';
        card.style.animationDelay = `${index * 0.15}s`;
        
        const expertiseTags = founder.expertise
            .slice(0, 3)
            .map(exp => `<span class="expertise-tag">${exp}</span>`)
            .join('');
        
        card.innerHTML = `
            <div class="founder-header">
                <div class="founder-name">${founder.name}</div>
                <div class="founder-company">${founder.company}</div>
            </div>
            <div class="founder-expertise">
                ${expertiseTags}
            </div>
            <div class="founder-reason">
                <span class="reason-label">💡 Why this match:</span>
                <div class="reason-text">${founder.reason}</div>
            </div>
        `;
        
        foundersGrid.appendChild(card);
    });
}

// Show error
function showError(message) {
    document.getElementById('errorText').textContent = message;
    showSection('error');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    showSection('input');
});


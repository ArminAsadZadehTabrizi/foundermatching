#!/usr/bin/env python3
"""
Flask Web Application for Founder Matching Agent
Provides a web interface for submitting voice check-ins and viewing matches
"""

from flask import Flask, render_template, request, jsonify
import json
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Load founder database
with open('founders_db.json', 'r') as f:
    db = json.load(f)
    FOUNDERS_DB = {f['id']: f for f in db['founders']}

# Pre-computed demo results (works without API key)
DEMO_RESULTS = {
    "ml": {
        "summary": "You're working on deploying your ML recommendation model to production but facing scaling issues, slow response times, and crashes under load",
        "needs": [
            "ML deployment at scale",
            "MLOps best practices",
            "Production model serving infrastructure",
            "Data pipeline optimization",
            "Containerization and load balancing"
        ],
        "matchedFounders": [
            {
                "id": "f001",
                "name": "Sarah Chen",
                "company": "DataFlow AI",
                "expertise": ["machine learning", "data pipelines", "MLOps"],
                "reason": "Sarah has deep expertise in production ML systems from her time at Google. She specializes in MLOps, scaling data pipelines, and optimizing model serving - exactly the challenges you're facing."
            },
            {
                "id": "f004",
                "name": "Alex Kim",
                "company": "DevTools Inc",
                "expertise": ["developer tools", "CI/CD", "Kubernetes"],
                "reason": "Alex built CI/CD infrastructure used by 10,000+ companies and is an expert in containerization with Docker and Kubernetes orchestration for load balancing."
            },
            {
                "id": "f009",
                "name": "Carlos Martinez",
                "company": "EdgeCompute",
                "expertise": ["distributed systems", "microservices", "real-time data"],
                "reason": "Carlos built real-time systems at Uber and specializes in distributed architecture that can handle multiple concurrent users without crashing."
            }
        ]
    }
}


def detect_topic(transcript):
    """Simple keyword-based topic detection"""
    text_lower = transcript.lower()
    
    keywords = {
        "ml": ["machine learning", "ml", "model", "deployment", "mlops", "data pipeline"],
        "fundraising": ["fundraising", "pitch", "investors", "vc", "seed round", "raise"],
        "mobile": ["mobile", "react native", "ios", "android", "app"],
        "security": ["security", "compliance", "soc 2", "penetration test", "encryption"],
        "growth": ["growth", "marketing", "user acquisition", "seo", "analytics"]
    }
    
    for topic, words in keywords.items():
        if any(word in text_lower for word in words):
            return topic
    
    return "ml"  # Default


def analyze_transcript(transcript):
    """Analyze transcript and return matches"""
    
    # Simulate AI processing
    time.sleep(0.5)
    
    # Detect topic
    topic = detect_topic(transcript)
    
    # For demo, use pre-computed results or generate simple matches
    if "machine learning" in transcript.lower() or "ml" in transcript.lower() or "model" in transcript.lower():
        return DEMO_RESULTS["ml"]
    
    # Simple matching based on keywords
    needs = []
    matched_ids = []
    
    text_lower = transcript.lower()
    
    # Analyze needs
    if "fundraising" in text_lower or "pitch" in text_lower or "investor" in text_lower:
        needs = ["Fundraising strategy", "Pitch deck creation", "Investor networking", "Term sheets"]
        matched_ids = ["f011", "f007", "f005"]
    elif "mobile" in text_lower or "react native" in text_lower or "app" in text_lower:
        needs = ["Mobile app optimization", "React Native expertise", "Performance tuning", "App store optimization"]
        matched_ids = ["f006", "f009", "f012"]
    elif "security" in text_lower or "compliance" in text_lower or "soc" in text_lower:
        needs = ["Security compliance", "SOC 2 preparation", "Data encryption", "Enterprise security"]
        matched_ids = ["f008", "f007", "f003"]
    elif "growth" in text_lower or "marketing" in text_lower or "users" in text_lower:
        needs = ["User acquisition", "Growth marketing", "Analytics setup", "SEO and content"]
        matched_ids = ["f005", "f007", "f012"]
    else:
        # Default ML deployment
        needs = ["ML deployment", "Production systems", "Scaling infrastructure", "Data pipelines"]
        matched_ids = ["f001", "f004", "f009"]
    
    # Get founder details
    matched_founders = []
    for founder_id in matched_ids[:3]:
        if founder_id in FOUNDERS_DB:
            founder = FOUNDERS_DB[founder_id].copy()
            # Generate simple reason
            founder["reason"] = f"{founder['name']} has expertise in {', '.join(founder['expertise'][:2])} and can help with your challenges."
            matched_founders.append(founder)
    
    # Create summary
    summary = f"Based on your check-in, you need help with {', '.join(needs[:2])}"
    
    return {
        "summary": summary,
        "needs": needs,
        "matchedFounders": matched_founders
    }


@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze a voice check-in transcript and return matches"""
    try:
        data = request.get_json()
        transcript = data.get('transcript', '')
        
        if not transcript or len(transcript.strip()) < 20:
            return jsonify({
                'error': 'Please provide a longer check-in (at least 20 characters)'
            }), 400
        
        # Analyze and get matches
        result = analyze_transcript(transcript)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': f'Error analyzing check-in: {str(e)}'
        }), 500


@app.route('/api/founders')
def list_founders():
    """List all founders"""
    return jsonify({
        'founders': list(FOUNDERS_DB.values())
    })


@app.route('/api/founder/<founder_id>')
def get_founder(founder_id):
    """Get a specific founder by ID"""
    founder = FOUNDERS_DB.get(founder_id)
    if founder:
        return jsonify(founder)
    else:
        return jsonify({'error': 'Founder not found'}), 404


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    import os
    
    # Get port from environment variable (for Cloud Run/App Engine) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "=" * 70)
    print("🚀 FOUNDER MATCHING AGENT - Web Interface")
    print("=" * 70)
    print("\n✅ Server starting...")
    print(f"📍 Port: {port}")
    print("\n💡 Demo Mode: Works without API key!")
    print("🛑 Press Ctrl+C to stop\n")
    
    # Use debug=False for production
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)


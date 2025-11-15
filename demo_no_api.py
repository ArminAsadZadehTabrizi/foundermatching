#!/usr/bin/env python3
"""
Demo Script WITHOUT API Key Required
Pre-computed results for hackathon presentation
"""

import json
import time

# Pre-computed demo results
DEMO_RESULTS = {
    "1": {
        "title": "ML Deployment Challenge",
        "summary": "You worked on deploying your ML recommendation model to production but are stuck on scaling issues, slow response times, and crashes under load",
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
                "reason": "Sarah has deep expertise in production ML systems from her time at Google. She specializes in MLOps, scaling data pipelines, and optimizing model serving - exactly the challenges you're facing with response times and crashes."
            },
            {
                "id": "f004",
                "name": "Alex Kim",
                "company": "DevTools Inc",
                "expertise": ["developer tools", "CI/CD", "Kubernetes"],
                "reason": "Alex built CI/CD infrastructure used by 10,000+ companies and is an expert in containerization with Docker and Kubernetes orchestration, which will help you set up proper load balancing."
            },
            {
                "id": "f009",
                "name": "Carlos Martinez",
                "company": "EdgeCompute",
                "expertise": ["distributed systems", "microservices", "Go"],
                "reason": "Carlos built real-time systems at Uber and specializes in distributed architecture and high-performance systems that can handle multiple concurrent users without crashing."
            }
        ]
    },
    "2": {
        "title": "Fundraising Preparation",
        "summary": "You've reached 1000 MAU with 40% retention and need to raise a $1-2M seed round, but you're unsure how to build a compelling pitch deck and connect with investors",
        "needs": [
            "Fundraising strategy",
            "Pitch deck creation",
            "Understanding investor metrics",
            "VC networking and meetings",
            "Cap table and term sheets"
        ],
        "matchedFounders": [
            {
                "id": "f011",
                "name": "Ryan O'Brien",
                "company": "FundRaiser Pro",
                "expertise": ["fundraising", "pitch decks", "investor relations"],
                "reason": "Ryan has raised $50M+ across multiple startups and is an expert in fundraising strategy, pitch deck storytelling, and investor networking. He can guide you through your entire seed round process."
            },
            {
                "id": "f007",
                "name": "David Thompson",
                "company": "SaaS Builder",
                "expertise": ["SaaS architecture", "subscription billing", "product management"],
                "reason": "David built and sold 2 SaaS companies and understands the metrics investors care about. He can help you frame your retention and MAU numbers in the most compelling way."
            },
            {
                "id": "f005",
                "name": "Priya Patel",
                "company": "GrowthMetrics",
                "expertise": ["growth hacking", "marketing analytics", "conversion optimization"],
                "reason": "Priya scaled 3 startups to $1M ARR and knows how to present growth metrics and projections that resonate with seed-stage investors."
            }
        ]
    },
    "3": {
        "title": "Mobile App Performance",
        "summary": "You're building a React Native social fitness app but struggling with laggy scrolling, slow image loading, crashes on older devices, and messy Redux state management",
        "needs": [
            "React Native optimization",
            "Mobile app performance tuning",
            "State management cleanup",
            "Push notifications implementation",
            "Deep linking setup",
            "App store optimization"
        ],
        "matchedFounders": [
            {
                "id": "f006",
                "name": "Jordan Lee",
                "company": "MobileFirst",
                "expertise": ["mobile development", "React Native", "iOS"],
                "reason": "Jordan built mobile apps with 5M+ downloads and is an expert in React Native performance optimization, mobile UX, and app store optimization - perfect for your fitness app challenges."
            },
            {
                "id": "f009",
                "name": "Carlos Martinez",
                "company": "EdgeCompute",
                "expertise": ["distributed systems", "real-time data", "WebSockets"],
                "reason": "Carlos specializes in real-time systems and can help you optimize your social feed's performance and implement efficient push notifications."
            },
            {
                "id": "f012",
                "name": "Aisha Mohammed",
                "company": "DesignLab",
                "expertise": ["UI/UX design", "design systems", "accessibility"],
                "reason": "Aisha was design lead at Airbnb and can help you create a smooth, beautiful user experience that works well even on older devices."
            }
        ]
    },
    "4": {
        "title": "Security & Compliance",
        "summary": "You have an enterprise customer interested in your HR SaaS product but they're asking about SOC 2 compliance, penetration testing, and security practices that you haven't documented",
        "needs": [
            "SOC 2 compliance",
            "Penetration testing",
            "Data encryption standards",
            "PII handling",
            "Incident response planning",
            "Enterprise security standards"
        ],
        "matchedFounders": [
            {
                "id": "f008",
                "name": "Nina Ivanova",
                "company": "SecureStack",
                "expertise": ["cybersecurity", "penetration testing", "OAuth"],
                "reason": "Nina was security lead at Microsoft and specializes in application security, compliance frameworks, and SOC 2 preparation. She can help you meet enterprise security requirements."
            },
            {
                "id": "f007",
                "name": "David Thompson",
                "company": "SaaS Builder",
                "expertise": ["SaaS architecture", "subscription billing", "customer success"],
                "reason": "David has sold B2B SaaS to enterprise customers and understands what security documentation and practices they expect. He can help you prepare for the sales process."
            },
            {
                "id": "f003",
                "name": "Elena Rodriguez",
                "company": "HealthConnect",
                "expertise": ["healthtech", "HIPAA compliance", "patient data"],
                "reason": "Elena built a HIPAA-compliant platform and is an expert in handling sensitive personal data, privacy regulations, and building trust with enterprise customers."
            }
        ]
    },
    "5": {
        "title": "Growth & User Acquisition",
        "summary": "You have 50 users who love your product but need to figure out how to grow beyond friends and family, with failed attempts at social media and paid ads",
        "needs": [
            "User acquisition strategies",
            "Growth marketing",
            "Analytics and metrics setup",
            "SEO and content marketing",
            "Efficient paid advertising",
            "Repeatable growth engine"
        ],
        "matchedFounders": [
            {
                "id": "f005",
                "name": "Priya Patel",
                "company": "GrowthMetrics",
                "expertise": ["growth hacking", "marketing analytics", "SEO"],
                "reason": "Priya scaled 3 startups from 0 to $1M ARR and is an expert in product-led growth, data-driven marketing, and building repeatable acquisition channels for early-stage startups."
            },
            {
                "id": "f007",
                "name": "David Thompson",
                "company": "SaaS Builder",
                "expertise": ["SaaS architecture", "customer success", "product management"],
                "reason": "David understands SaaS metrics inside and out. He can help you set up proper analytics to measure what's working and optimize your conversion funnels."
            },
            {
                "id": "f012",
                "name": "Aisha Mohammed",
                "company": "DesignLab",
                "expertise": ["UI/UX design", "user research", "accessibility"],
                "reason": "Aisha specializes in user research and can help you understand why users love your product, so you can communicate that value proposition effectively in your marketing."
            }
        ]
    }
}

SCENARIOS = {
    "1": {
        "title": "ML Deployment Challenge",
        "transcript": """
        Hey team, weekly check-in here. This week I've been working on getting our 
        machine learning recommendation model into production. The model works great 
        in development - we're getting 95% accuracy on our test set. 
        
        But here's where I'm stuck: when I try to deploy it and serve predictions 
        to real users, everything falls apart. The response times are terrible - 
        like 5+ seconds per prediction. And when multiple users hit it at once, 
        it just crashes.
        
        I think I need to containerize it with Docker and maybe set up some kind 
        of load balancing? But I've never done MLOps at scale before. Our data 
        pipeline is also a mess - it takes hours to retrain the model on new data.
        
        Really need someone who's built production ML systems before and knows 
        about data engineering, model serving, and scaling. Any help would be amazing!
        """
    },
    "2": {
        "title": "Fundraising Preparation",
        "transcript": """
        Hi everyone, checking in for the week. So we've been making great progress 
        on the product - we hit 1000 monthly active users! Our retention is looking 
        solid at 40% month-over-month.
        
        But now I'm at a point where I need to start fundraising. I want to raise 
        a seed round, maybe $1-2M, but I have no idea where to start. Like, how do 
        I build a compelling pitch deck? What metrics do investors actually care about? 
        How do I even get meetings with VCs?
        
        I've never raised money before and I'm feeling pretty overwhelmed. I need 
        someone who's been through the fundraising process, knows how to tell a good 
        story, and can help me understand what investors are looking for. 
        
        Also need help with cap table stuff and understanding term sheets. This is 
        all new territory for me.
        """
    },
    "3": {
        "title": "Mobile App Performance",
        "transcript": """
        Weekly update: I'm building a React Native app for our startup - it's a 
        social fitness app where users can share workouts and compete with friends.
        
        The app works, but the performance is really bad. Scrolling through the feed 
        is laggy, images take forever to load, and it crashes on older devices. 
        I'm also struggling with state management - we're using Redux but the code 
        is getting messy and hard to maintain.
        
        Plus, I need to figure out push notifications and deep linking, but the 
        documentation is confusing and I keep running into issues.
        
        I could really use help from someone who's shipped successful mobile apps 
        before, knows React Native inside and out, and can help me optimize 
        performance and clean up the architecture. Also need advice on app store 
        optimization and getting our first users.
        """
    },
    "4": {
        "title": "Security & Compliance",
        "transcript": """
        Hey, checking in. We're building a B2B SaaS product for HR teams, and this 
        week we got our first enterprise customer interested - a company with 5000 
        employees! Super exciting!
        
        But they're asking about SOC 2 compliance, penetration testing, and our 
        security practices, and honestly I don't know how to answer. We have basic 
        authentication with JWT tokens, but I'm not sure if that's secure enough.
        
        They also want to know about data encryption, how we handle PII, and our 
        incident response plan. We don't have any of that documented.
        
        I'm stuck because I don't want to lose this customer, but I also don't know 
        what security standards we need to meet for enterprise clients. Need help 
        from someone who understands application security, compliance frameworks, 
        and how to build secure systems that enterprises will trust.
        """
    },
    "5": {
        "title": "Growth & User Acquisition",
        "transcript": """
        Weekly check-in! Our product is live and we have about 50 users from friends 
        and family. The feedback is great - people love it. But now I need to figure 
        out how to actually grow this thing.
        
        I've tried posting on Twitter and Reddit but got basically zero traction. 
        We have a blog but no traffic. I set up Google Ads but burned through $500 
        in two days with only 3 signups.
        
        I don't know if I should focus on SEO, content marketing, paid ads, or 
        something else entirely. How do I even measure what's working? What metrics 
        should I track?
        
        Really need someone who's done growth for early-stage startups before. 
        Someone who knows how to acquire users efficiently, set up analytics 
        properly, and build a repeatable growth engine. I feel like I'm just 
        throwing stuff at the wall and nothing's sticking.
        """
    }
}


def simulate_analysis(scenario_id: str):
    """Simulate AI analysis with pre-computed results"""
    print("🔍 Analyzing check-in transcript...")
    time.sleep(1)
    
    print("📊 Extracting structured information...")
    time.sleep(1)
    
    print("🔎 Searching for matching founders...")
    time.sleep(1)
    
    print("💡 Generating personalized recommendations...")
    time.sleep(1)
    print()
    
    return DEMO_RESULTS[scenario_id]


def run_scenario(scenario_id: str):
    """Run a single demo scenario"""
    scenario = SCENARIOS[scenario_id]
    
    print("\n" + "=" * 80)
    print(f"📋 SCENARIO: {scenario['title']}")
    print("=" * 80)
    print("\n📝 Check-in Transcript:")
    print("-" * 80)
    print(scenario['transcript'])
    print("-" * 80)
    print()
    
    result = simulate_analysis(scenario_id)
    
    print("\n" + "=" * 80)
    print("✨ MATCHING RESULTS")
    print("=" * 80)
    print()
    
    print(f"📊 Summary: {result['summary']}")
    print()
    
    print("🎯 Identified Needs:")
    for need in result['needs']:
        print(f"  • {need}")
    print()
    
    print("👥 Matched Founders:")
    print()
    for i, founder in enumerate(result['matchedFounders'], 1):
        print(f"{i}. {founder['name']} - {founder['company']}")
        print(f"   Expertise: {', '.join(founder['expertise'])}")
        print(f"   💡 Why: {founder['reason']}")
        print()
    
    return result


def main():
    """Run the interactive demo"""
    
    print("\n" + "🚀" * 40)
    print(" " * 25 + "FOUNDER MATCHING AGENT")
    print(" " * 28 + "Interactive Demo")
    print(" " * 22 + "(Demo Mode - No API Key Needed)")
    print("🚀" * 40 + "\n")
    
    print("This demo shows how the AI agent analyzes voice check-ins")
    print("and matches founders with relevant experts.\n")
    print("⚡ Running in DEMO MODE with pre-computed results")
    print("   (Perfect for hackathon presentations!)\n")
    
    while True:
        print("\n" + "=" * 80)
        print("Available Scenarios:")
        print("=" * 80)
        for key, scenario in SCENARIOS.items():
            print(f"  {key}. {scenario['title']}")
        print(f"  6. Run all scenarios")
        print(f"  7. Exit")
        print()
        
        choice = input("Select a scenario (1-7): ").strip()
        
        if choice == "7":
            print("\n👋 Thanks for trying the demo!\n")
            break
        elif choice == "6":
            print("\n🎬 Running all scenarios...\n")
            for key in sorted(SCENARIOS.keys()):
                run_scenario(key)
                if key != max(SCENARIOS.keys()):
                    input("\n⏸️  Press Enter to continue to next scenario...")
            print("\n✅ All scenarios completed!")
        elif choice in SCENARIOS:
            run_scenario(choice)
        else:
            print("❌ Invalid choice. Please select 1-7.")
    
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!\n")













#!/usr/bin/env python3
"""
Interactive Demo Script for Founder Matching Agent
Shows different scenarios and use cases
"""

import asyncio
from agent import FounderMatchingAgent

# Demo check-in scenarios
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


async def run_scenario(agent: FounderMatchingAgent, scenario: dict):
    """Run a single demo scenario"""
    print("\n" + "=" * 80)
    print(f"📋 SCENARIO: {scenario['title']}")
    print("=" * 80)
    print("\n📝 Check-in Transcript:")
    print("-" * 80)
    print(scenario['transcript'])
    print("-" * 80)
    print()
    
    result = await agent.analyze_checkin(scenario['transcript'])
    
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


async def main():
    """Run the interactive demo"""
    
    print("\n" + "🚀" * 40)
    print(" " * 25 + "FOUNDER MATCHING AGENT")
    print(" " * 28 + "Interactive Demo")
    print("🚀" * 40 + "\n")
    
    print("This demo shows how the AI agent analyzes voice check-ins")
    print("and matches founders with relevant experts.\n")
    
    agent = FounderMatchingAgent()
    
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
                await run_scenario(agent, SCENARIOS[key])
                if key != max(SCENARIOS.keys()):
                    input("\n Press Enter to continue to next scenario...")
            print("\n✅ All scenarios completed!")
        elif choice in SCENARIOS:
            await run_scenario(agent, SCENARIOS[choice])
        else:
            print("❌ Invalid choice. Please select 1-7.")
    
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!\n")













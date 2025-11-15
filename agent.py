#!/usr/bin/env python3
"""
AI Matching Agent
Analyzes founder voice check-ins and matches them with relevant founders
"""

import os
import json
import asyncio
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class FounderMatchingAgent:
    """Agent that processes voice check-ins and finds matching founders"""
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
    async def analyze_checkin(self, transcript: str) -> dict:
        """
        Analyze a voice check-in transcript and match with founders
        
        Args:
            transcript: The transcribed voice check-in text
            
        Returns:
            Dictionary with summary, needs, and matched founders
        """
        
        # Step 1: Extract structured information from the transcript
        extraction_prompt = f"""You are analyzing a startup founder's weekly voice check-in.

Extract the following information from the transcript:
1. What they worked on this week
2. Where they are stuck or facing challenges
3. What help or expertise they need
4. Key topics and skill areas involved

Transcript:
{transcript}

Respond in JSON format:
{{
  "worked_on": "summary of what they worked on",
  "stuck_on": "what challenges or blockers they're facing",
  "needs_help_with": ["list", "of", "specific", "needs"],
  "topics": ["relevant", "topic", "areas"],
  "skills_needed": ["specific", "skills", "or", "expertise"]
}}"""

        print("🔍 Analyzing check-in transcript...\n")
        
        extraction_response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": extraction_prompt}]
        )
        
        extracted_info = json.loads(extraction_response.content[0].text)
        print("📊 Extracted Information:")
        print(json.dumps(extracted_info, indent=2))
        print()
        
        # Step 2: Create search query for founders
        search_queries = []
        
        # Combine needs and skills for comprehensive search
        all_needs = extracted_info.get("needs_help_with", [])
        all_skills = extracted_info.get("skills_needed", [])
        stuck_on = extracted_info.get("stuck_on", "")
        
        # Create a detailed search description for vector search
        search_description = f"""
        The founder is working on: {extracted_info.get('worked_on', '')}
        
        They are stuck on: {stuck_on}
        
        They need help with: {', '.join(all_needs)}
        
        Skills and expertise needed: {', '.join(all_skills)}
        
        Topics: {', '.join(extracted_info.get('topics', []))}
        """
        
        # For demo purposes, we'll simulate the MCP tool calls
        # In production, these would be actual MCP tool calls
        print("🔎 Searching for matching founders...\n")
        
        # Load founder database for simulation
        with open("founders_db.json", "r") as f:
            db = json.load(f)
            founders = db["founders"]
        
        # Simple matching logic (in production, this would use vector_search tool)
        matches = []
        search_terms = all_needs + all_skills + extracted_info.get("topics", [])
        
        for founder in founders:
            score = 0
            searchable = (
                " ".join(founder["expertise"]) + " " +
                " ".join(founder["helpfulIn"]) + " " +
                founder["bio"]
            ).lower()
            
            for term in search_terms:
                if term.lower() in searchable:
                    score += searchable.count(term.lower())
            
            if score > 0:
                matches.append({
                    "founder": founder,
                    "score": score
                })
        
        # Sort by score and get top 3
        matches.sort(key=lambda x: x["score"], reverse=True)
        top_matches = matches[:3]
        
        print(f"✅ Found {len(top_matches)} matching founders\n")
        
        # Step 3: Generate reasons for each match
        matched_founders = []
        
        for match in top_matches:
            founder = match["founder"]
            
            # Generate personalized reason
            reason_prompt = f"""Given this founder's needs and this expert's profile, write a short 1-2 sentence explanation of why this is a good match.

Founder needs:
- Stuck on: {stuck_on}
- Needs help with: {', '.join(all_needs)}
- Skills needed: {', '.join(all_skills)}

Expert profile:
- Name: {founder['name']}
- Company: {founder['company']}
- Expertise: {', '.join(founder['expertise'])}
- Helpful in: {', '.join(founder['helpfulIn'])}
- Bio: {founder['bio']}

Write a short, friendly reason why this expert can help. Be specific about the skill match."""

            reason_response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=150,
                messages=[{"role": "user", "content": reason_prompt}]
            )
            
            reason = reason_response.content[0].text.strip()
            
            matched_founders.append({
                "id": founder["id"],
                "name": founder["name"],
                "company": founder["company"],
                "expertise": founder["expertise"][:3],
                "reason": reason
            })
        
        # Step 4: Create summary
        summary = f"You worked on {extracted_info.get('worked_on', 'your project')} but are stuck on {stuck_on}. You need help with {', '.join(all_needs[:2])}."
        
        # Final output
        result = {
            "summary": summary,
            "needs": all_needs,
            "matchedFounders": matched_founders
        }
        
        return result
    
    def format_output(self, result: dict) -> str:
        """Format the result as a nice JSON string"""
        return json.dumps(result, indent=2)


async def main():
    """Demo the agent with a sample check-in"""
    
    # Example voice check-in transcript
    sample_transcript = """
    Hey, this is my weekly check-in. So this week I've been working on deploying 
    our machine learning model to production. We have this recommendation model 
    that works great locally, but I'm really stuck on how to scale it. Like, 
    when we try to serve predictions to multiple users simultaneously, the 
    response time just explodes. 
    
    I think we need to set up some kind of model serving infrastructure, maybe 
    use Docker or Kubernetes? But honestly, I'm not sure about the best practices 
    here. We're also running into issues with our data pipeline - it's taking 
    forever to process new data and retrain the model.
    
    So yeah, I really need help from someone who's done ML deployment at scale 
    before. Someone who knows about MLOps, production ML systems, and how to 
    build reliable data pipelines. That would be super helpful right now.
    """
    
    print("=" * 70)
    print("🚀 FOUNDER MATCHING AGENT - Demo")
    print("=" * 70)
    print()
    
    agent = FounderMatchingAgent()
    result = await agent.analyze_checkin(sample_transcript)
    
    print("=" * 70)
    print("📋 FINAL MATCHING RESULT")
    print("=" * 70)
    print()
    print(agent.format_output(result))
    print()
    
    return result


if __name__ == "__main__":
    asyncio.run(main())













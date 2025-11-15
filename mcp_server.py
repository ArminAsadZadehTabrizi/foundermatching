#!/usr/bin/env python3
"""
MCP Server for Founder Matching System
Provides tools for extracting needs/learnings and matching startup founders
"""

import json
import asyncio
from typing import Any, Sequence
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from anthropic import Anthropic

# Load founder database
with open("founders_db.json", "r") as f:
    db = json.load(f)
    FOUNDERS = db["founders"]
    NEEDS = db.get("needs", [])
    LEARNINGS = db.get("learnings", [])

# Initialize embedding model for semantic search
print("Loading embedding model...", flush=True)
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Pre-compute embeddings for all founders
founder_texts = []
for founder in FOUNDERS:
    # Create a rich text representation for each founder
    text = f"{founder['name']} {founder['company']} {' '.join(founder['expertise'])} {' '.join(founder['helpfulIn'])} {founder['bio']}"
    founder_texts.append(text)

print("Computing founder embeddings...", flush=True)
founder_embeddings = embedding_model.encode(founder_texts)

# Initialize Anthropic client for AI extraction
anthropic_client = None
if os.getenv("ANTHROPIC_API_KEY"):
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    print("Anthropic client initialized", flush=True)
else:
    print("Warning: No ANTHROPIC_API_KEY found - extract_needs_learnings will use simple extraction", flush=True)

# Create MCP server
app = Server("founder-matching-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools for founder matching"""
    return [
        Tool(
            name="extract_needs_learnings",
            description="Extract structured needs and learnings from a founder's weekly free-text or voice-transcribed check-in. Identifies 1-3 concrete needs (things they need help with) and 1-3 learnings/skills (things they can teach or help with). Assigns each a category like sales, marketing, product, fundraising, branding, UX, technical, AI, hiring, or strategy.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The free-text or voice-transcribed weekly check-in from the founder describing what they worked on, what they're stuck on, and what they learned"
                    },
                    "user_id": {
                        "type": "string",
                        "description": "The ID of the founder submitting the check-in (optional, for context)",
                        "default": "unknown"
                    }
                },
                "required": ["text"]
            }
        ),
        Tool(
            name="compute_matches",
            description="Compute potential matches between founders based on needs and learnings. Uses semantic similarity and category matching to find founders whose learnings/skills can help with other founders' needs. Returns matches with confidence scores and reasons.",
            inputSchema={
                "type": "object",
                "properties": {
                    "needs": {
                        "type": "array",
                        "description": "Array of need objects from the database, each with id, user_id, label, and category",
                        "items": {
                            "type": "object"
                        }
                    },
                    "learnings": {
                        "type": "array",
                        "description": "Array of learning objects from the database, each with id, user_id, label, and category",
                        "items": {
                            "type": "object"
                        }
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of matches to return per need (default: 3)",
                        "default": 3
                    }
                },
                "required": ["needs", "learnings"]
            }
        ),
        Tool(
            name="search_founders",
            description="Search for founders by keywords in their expertise, industry, or bio. Returns founders matching the query.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'machine learning', 'fundraising', 'mobile development')"
                    },
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of results to return (default: 5)",
                        "default": 5
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="vector_search",
            description="Semantic search using embeddings to find founders most relevant to a description or need. Best for matching based on meaning rather than exact keywords.",
            inputSchema={
                "type": "object",
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "Natural language description of what help is needed (e.g., 'I need help deploying my ML model to production and scaling it')"
                    },
                    "top_k": {
                        "type": "number",
                        "description": "Number of top matches to return (default: 3)",
                        "default": 3
                    }
                },
                "required": ["description"]
            }
        ),
        Tool(
            name="get_founder_by_id",
            description="Get detailed information about a specific founder by their ID",
            inputSchema={
                "type": "object",
                "properties": {
                    "founder_id": {
                        "type": "string",
                        "description": "The founder's ID (e.g., 'f001')"
                    }
                },
                "required": ["founder_id"]
            }
        ),
        Tool(
            name="list_all_founders",
            description="List all founders in the database with basic information",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="filter_by_expertise",
            description="Filter founders by specific expertise areas",
            inputSchema={
                "type": "object",
                "properties": {
                    "expertise": {
                        "type": "string",
                        "description": "Expertise area to filter by (e.g., 'machine learning', 'fintech')"
                    }
                },
                "required": ["expertise"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """Handle tool calls"""
    
    if name == "extract_needs_learnings":
        text = arguments["text"]
        user_id = arguments.get("user_id", "unknown")
        
        # Use AI extraction if available, otherwise fall back to keyword-based
        if anthropic_client:
            try:
                # Use Claude to extract structured needs and learnings
                prompt = f"""You are analyzing a startup founder's weekly check-in. Extract concrete needs (things they need help with) and learnings/skills (things they learned or can help others with).

Rules:
- Identify 1-3 concrete Needs (challenges, blockers, help requests)
- Identify 1-3 Learnings or Skills (things they learned, completed, or can teach)
- Assign each a category from: sales, marketing, product, fundraising, branding, UX, technical, AI, hiring, strategy
- Be specific and actionable

Check-in text:
{text}

Respond with ONLY valid JSON in this exact format:
{{
  "needs": [
    {{"label": "specific need description", "category": "category_name"}}
  ],
  "learnings": [
    {{"label": "specific learning or skill", "category": "category_name"}}
  ]
}}"""

                response = anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                result = json.loads(response.content[0].text)
                
                return [TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            except Exception as e:
                # Fall back to simple extraction if AI fails
                print(f"AI extraction failed: {e}, using fallback", flush=True)
        
        # Fallback: Simple keyword-based extraction
        text_lower = text.lower()
        needs = []
        learnings = []
        
        # Keyword patterns for needs
        if any(word in text_lower for word in ["stuck", "struggling", "need help", "challenge", "problem", "issue"]):
            if "ml" in text_lower or "machine learning" in text_lower:
                needs.append({"label": "Machine learning deployment and scaling", "category": "technical"})
            if "fundrais" in text_lower or "investor" in text_lower:
                needs.append({"label": "Fundraising and investor relations", "category": "fundraising"})
            if "market" in text_lower or "growth" in text_lower:
                needs.append({"label": "Growth and marketing strategy", "category": "marketing"})
        
        # Keyword patterns for learnings
        if any(word in text_lower for word in ["learned", "completed", "built", "launched", "achieved", "figured out"]):
            if "product" in text_lower or "feature" in text_lower:
                learnings.append({"label": "Product development and feature launch", "category": "product"})
            if "user" in text_lower or "customer" in text_lower:
                learnings.append({"label": "User research and customer feedback", "category": "UX"})
        
        # Default if nothing found
        if not needs:
            needs.append({"label": "General startup guidance", "category": "strategy"})
        if not learnings:
            learnings.append({"label": "Weekly progress and insights", "category": "product"})
        
        result = {
            "needs": needs[:3],
            "learnings": learnings[:3]
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]
    
    elif name == "compute_matches":
        needs = arguments["needs"]
        learnings = arguments["learnings"]
        limit = arguments.get("limit", 3)
        
        matches = []
        
        # For each need, find learnings that could help
        for need in needs:
            need_id = need.get("id", "")
            need_user_id = need.get("user_id", "")
            need_label = need.get("label", "")
            need_category = need.get("category", "")
            
            # Compute embedding for this need
            need_embedding = embedding_model.encode([need_label])[0]
            
            scored_learnings = []
            
            for learning in learnings:
                learning_user_id = learning.get("user_id", "")
                
                # Don't match a founder with themselves
                if learning_user_id == need_user_id:
                    continue
                
                learning_label = learning.get("label", "")
                learning_category = learning.get("category", "")
                
                # Compute semantic similarity
                learning_embedding = embedding_model.encode([learning_label])[0]
                similarity = np.dot(need_embedding, learning_embedding) / (
                    np.linalg.norm(need_embedding) * np.linalg.norm(learning_embedding)
                )
                
                # Category bonus
                category_bonus = 0.2 if need_category == learning_category else 0
                
                # Final score
                score = float(similarity) + category_bonus
                
                # Generate reason
                if need_category == learning_category:
                    reason = f"Both focus on {need_category}. Semantic match on: {learning_label}"
                else:
                    reason = f"Semantic similarity: learning about {learning_label} can help with {need_label}"
                
                scored_learnings.append({
                    "need_id": need_id,
                    "expert_user_id": learning_user_id,
                    "score": round(score, 3),
                    "reason": reason,
                    "matched_learning": learning_label
                })
            
            # Sort by score and take top N
            scored_learnings.sort(key=lambda x: x["score"], reverse=True)
            matches.extend(scored_learnings[:limit])
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "total_matches": len(matches),
                "matches": matches
            }, indent=2)
        )]
    
    elif name == "search_founders":
        query = arguments["query"].lower()
        limit = arguments.get("limit", 5)
        
        # Search in expertise, helpfulIn, bio, and industry
        results = []
        for founder in FOUNDERS:
            score = 0
            searchable_text = (
                " ".join(founder["expertise"]) + " " +
                " ".join(founder["helpfulIn"]) + " " +
                founder["bio"] + " " +
                founder["industry"]
            ).lower()
            
            # Simple keyword matching with scoring
            query_words = query.split()
            for word in query_words:
                if word in searchable_text:
                    score += searchable_text.count(word)
            
            if score > 0:
                results.append({
                    "founder": founder,
                    "score": score
                })
        
        # Sort by score and limit
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:limit]
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "query": query,
                "found": len(results),
                "results": [r["founder"] for r in results]
            }, indent=2)
        )]
    
    elif name == "vector_search":
        description = arguments["description"]
        top_k = arguments.get("top_k", 3)
        
        # Compute embedding for the query
        query_embedding = embedding_model.encode([description])[0]
        
        # Calculate cosine similarity with all founders
        similarities = []
        for idx, founder_emb in enumerate(founder_embeddings):
            similarity = np.dot(query_embedding, founder_emb) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(founder_emb)
            )
            similarities.append({
                "founder": FOUNDERS[idx],
                "similarity": float(similarity)
            })
        
        # Sort by similarity and get top k
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        top_matches = similarities[:top_k]
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "query": description,
                "found": len(top_matches),
                "matches": [
                    {
                        **match["founder"],
                        "similarity_score": round(match["similarity"], 3)
                    }
                    for match in top_matches
                ]
            }, indent=2)
        )]
    
    elif name == "get_founder_by_id":
        founder_id = arguments["founder_id"]
        founder = next((f for f in FOUNDERS if f["id"] == founder_id), None)
        
        if founder:
            return [TextContent(
                type="text",
                text=json.dumps(founder, indent=2)
            )]
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Founder with ID {founder_id} not found"})
            )]
    
    elif name == "list_all_founders":
        summary = [
            {
                "id": f["id"],
                "name": f["name"],
                "company": f["company"],
                "expertise": f["expertise"][:3],  # First 3 areas
                "industry": f["industry"]
            }
            for f in FOUNDERS
        ]
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "total": len(FOUNDERS),
                "founders": summary
            }, indent=2)
        )]
    
    elif name == "filter_by_expertise":
        expertise_query = arguments["expertise"].lower()
        
        matches = []
        for founder in FOUNDERS:
            expertise_text = " ".join(founder["expertise"]).lower()
            helpful_text = " ".join(founder["helpfulIn"]).lower()
            
            if expertise_query in expertise_text or expertise_query in helpful_text:
                matches.append(founder)
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "expertise": expertise_query,
                "found": len(matches),
                "founders": matches
            }, indent=2)
        )]
    
    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"})
        )]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())


# 🚀 AI Founder Matching Agent

An intelligent agent that analyzes startup founder voice check-ins and matches them with relevant expert founders who can help.

Built for hackathon - demonstrates MCP (Model Context Protocol) tools, semantic search, and AI-powered matching.

## 🎯 What It Does

1. **Receives** transcribed voice check-ins from founders
2. **Extracts** key information:
   - What they worked on
   - Where they're stuck
   - What help they need
   - Relevant topics/skills
3. **Searches** a founder database using semantic similarity
4. **Matches** with the best 1-3 expert founders
5. **Returns** structured recommendations with reasons
6. **Schedules** coffee chats between matched founders
7. **Generates** Jitsi video meeting links for seamless video calls

## ✨ Key Features

### 🤖 AI-Powered Matching
- Uses Claude 3.5 Sonnet for intelligent extraction
- Semantic search with vector embeddings
- Personalized match explanations

### 🎤 Voice Input Support
- Multi-language voice recognition (English, German, Spanish, French)
- Real-time transcription in browser
- No external APIs needed for voice

### 📅 Coffee Chat Scheduling
- Expert proposes 3 time slots
- Requester selects preferred time
- Automatic status tracking

### 🎥 **Integrated Video Meetings** (NEW!)
- **Automatic Jitsi meeting link generation**
- No account or installation required
- Join directly from browser
- Secure, private video rooms
- Screen sharing, chat, and more

[Learn more about the Jitsi integration →](JITSI_MEETING_FEATURE.md)

### 🔐 User Authentication
- Simple email-based login
- Session management
- Role-based access (founders, admin)

### 📊 Admin Dashboard
- View all matches and coffee chats
- Monitor platform statistics
- Manage users and connections

## 🏗️ Architecture

```
┌─────────────────┐
│  Voice Check-in │
│   (Transcript)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI Agent       │
│  (Claude)       │──► Extract needs & topics
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  MCP Tools      │
│  - search       │──► Find matching founders
│  - vector_search│
│  - filters      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Founder DB     │
│  (12 founders)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Matched Results│
│  (JSON output)  │
└─────────────────┘
```

## 📦 Components

### 1. `founders_db.json`
Database of 12 sample founders across different industries:
- ML/AI, FinTech, HealthTech, DevOps, Growth, Mobile, SaaS, Security, etc.
- Each with expertise areas, bio, and areas they can help with

### 2. `mcp_server.py`
MCP server providing 5 tools:
- `search_founders` - Keyword search
- `vector_search` - Semantic search using embeddings
- `get_founder_by_id` - Get specific founder details
- `list_all_founders` - List all founders
- `filter_by_expertise` - Filter by expertise area

### 3. `agent.py`
Main AI agent that:
- Analyzes transcripts using Claude
- Extracts structured information
- Calls MCP tools (simulated in standalone mode)
- Generates personalized match reasons
- Returns JSON output

### 4. `demo.py`
Interactive demo script with multiple test scenarios

## 🚀 Quick Start

### Installation

```bash
# Clone/navigate to project
cd hackathon

# Install dependencies
pip install -r requirements.txt

# Set up your API key
export ANTHROPIC_API_KEY="your-key-here"
```

### Run Demo

```bash
# Run the agent with a sample check-in
python agent.py

# Or use the interactive demo
python demo.py
```

### Expected Output

```json
{
  "summary": "You worked on deploying ML models but are stuck on scaling...",
  "needs": [
    "ML deployment at scale",
    "MLOps best practices",
    "data pipeline optimization"
  ],
  "matchedFounders": [
    {
      "id": "f001",
      "name": "Sarah Chen",
      "company": "DataFlow AI",
      "expertise": ["machine learning", "data pipelines", "MLOps"],
      "reason": "Sarah has deep expertise in production ML systems and scaling data pipelines from her time at Google. She specializes in MLOps and can help you optimize your model serving infrastructure."
    }
  ]
}
```

## 🛠️ MCP Server Usage

Run the MCP server standalone:

```bash
python mcp_server.py
```

The server provides tools that can be called via MCP protocol. Tools include:

- **search_founders(query, limit)** - Keyword-based search
- **vector_search(description, top_k)** - Semantic similarity search
- **get_founder_by_id(founder_id)** - Get specific founder
- **list_all_founders()** - List all available founders
- **filter_by_expertise(expertise)** - Filter by expertise area

## 📝 Example Use Cases

### Use Case 1: ML Deployment Help
**Input:** "I'm stuck deploying my ML model to production..."  
**Matches:** Sarah Chen (MLOps expert), Alex Kim (DevOps/infra)

### Use Case 2: Fundraising Advice
**Input:** "I need help preparing my Series A pitch deck..."  
**Matches:** Ryan O'Brien (fundraising expert)

### Use Case 3: Mobile App Development
**Input:** "Building a React Native app, need help with performance..."  
**Matches:** Jordan Lee (mobile dev expert)

## 🎓 Technical Details

### Vector Search
- Uses `sentence-transformers` with `all-MiniLM-L6-v2` model
- Pre-computes embeddings for all founders
- Cosine similarity matching for semantic search
- Fast and accurate matching based on meaning, not just keywords

### AI Analysis
- Powered by Claude 3.5 Sonnet
- Two-stage process:
  1. Extract structured info from transcript
  2. Generate personalized match reasons
- JSON-structured input/output

### Extensibility
- Easy to add more founders to `founders_db.json`
- MCP tools can be extended with more search capabilities
- Agent logic can be customized for different matching criteria

## 🔮 Future Enhancements

- [ ] Real database (PostgreSQL + pgvector)
- [ ] Live voice transcription integration
- [ ] Match confidence scores
- [ ] Founder availability/scheduling
- [ ] Match history and feedback loop
- [ ] Web UI for founders
- [ ] Slack/Discord bot integration
- [ ] Multi-language support

## 📄 Files

```
hackathon/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── founders_db.json       # Founder database
├── mcp_server.py         # MCP tools server
├── agent.py              # Main matching agent
└── demo.py               # Interactive demo
```

## 🤝 Contributing

This is a hackathon project! Feel free to:
- Add more founders to the database
- Improve matching algorithms
- Add new MCP tools
- Build integrations

## 📜 License

MIT License - Built for hackathon

## 🙏 Acknowledgments

- Built with [MCP (Model Context Protocol)](https://modelcontextprotocol.io/)
- Powered by [Anthropic Claude](https://anthropic.com/)
- Embeddings by [Sentence Transformers](https://www.sbert.net/)

---

**Made with ❤️ for the startup community**









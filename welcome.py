#!/usr/bin/env python3
"""
Welcome script - shows project info and next steps
"""

import os

def print_banner():
    """Print welcome banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║           🚀  FOUNDER MATCHING AGENT  🚀                      ║
    ║                                                               ║
    ║     AI-Powered Founder-to-Expert Matching System             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_features():
    """Print key features"""
    features = """
    ✨ KEY FEATURES:
    
    🎤  Voice Check-in Analysis    Extract needs from natural language
    🧠  Semantic Search            AI-powered matching with embeddings
    🎯  Smart Recommendations      Top 3 experts with personalized reasons
    🛠️   MCP Tools                 5 search tools for flexible queries
    📊  Production Ready           Clean code, full documentation
    """
    print(features)

def print_quick_start():
    """Print quick start instructions"""
    quick_start = """
    🚀 QUICK START:
    
    1️⃣  Setup (2 minutes)
        ./setup.sh
        source venv/bin/activate
        export ANTHROPIC_API_KEY='your-key-here'
    
    2️⃣  Run Demo (1 minute)
        python3 demo.py          # Interactive demo with 5 scenarios
        python3 agent.py         # Quick test with sample check-in
        python3 test_basic.py    # Basic functionality tests
    
    3️⃣  Read Docs
        README.md                # Full documentation
        QUICKSTART.md           # 5-minute setup guide
        HACKATHON_PITCH.md      # Presentation materials
    """
    print(quick_start)

def print_project_info():
    """Print project information"""
    info = """
    📦 PROJECT INFO:
    
    • Database:  12 expert founders across industries
    • Tools:     5 MCP tools (search, vector search, filters)
    • Scenarios: 5 demo scenarios built-in
    • Tech:      Claude 3.5, Sentence Transformers, MCP
    • Code:      ~690 lines of clean, documented Python
    • Docs:      Complete guides and documentation
    """
    print(info)

def check_setup():
    """Check if setup is complete"""
    print("\n    🔍 SYSTEM CHECK:\n")
    
    checks = [
        ("Python 3", "python3 --version"),
        ("Dependencies installed", "pip show anthropic"),
        ("API Key set", "echo $ANTHROPIC_API_KEY"),
    ]
    
    for name, cmd in checks:
        result = os.system(f"{cmd} > /dev/null 2>&1")
        status = "✅" if result == 0 else "❌"
        print(f"    {status}  {name}")
    
    print()

def print_footer():
    """Print footer"""
    footer = """
    ═══════════════════════════════════════════════════════════════
    
    📚  Documentation:  README.md, QUICKSTART.md
    🎬  Demo:          python3 demo.py
    💡  Quick Test:    python3 agent.py
    
    ═══════════════════════════════════════════════════════════════
    
    Built with ❤️  for the startup community
    
    """
    print(footer)

def main():
    """Main welcome function"""
    os.system('clear' if os.name != 'nt' else 'cls')
    
    print_banner()
    print_features()
    print_project_info()
    print_quick_start()
    check_setup()
    print_footer()
    
    print("    Ready to get started? Run: python3 demo.py\n")

if __name__ == "__main__":
    main()













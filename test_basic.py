#!/usr/bin/env python3
"""
Basic test to verify the system works
"""

import json

# Test 1: Load founder database
print("Test 1: Loading founder database...")
try:
    with open("founders_db.json", "r") as f:
        db = json.load(f)
    print(f"✅ Loaded {len(db['founders'])} founders")
    print(f"   Sample: {db['founders'][0]['name']} - {db['founders'][0]['company']}")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Test 2: Check if embedding model can be imported
print("Test 2: Checking dependencies...")
try:
    from sentence_transformers import SentenceTransformer
    print("✅ sentence-transformers available")
    
    from anthropic import Anthropic
    print("✅ anthropic available")
    
    import numpy as np
    print("✅ numpy available")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Test 3: Test simple matching logic
print("Test 3: Testing basic matching logic...")
try:
    with open("founders_db.json", "r") as f:
        db = json.load(f)
        founders = db["founders"]
    
    # Search for ML expertise
    query = "machine learning"
    matches = []
    
    for founder in founders:
        searchable = " ".join(founder["expertise"]).lower()
        if query.lower() in searchable:
            matches.append(founder["name"])
    
    print(f"✅ Found {len(matches)} founders with ML expertise:")
    for name in matches:
        print(f"   - {name}")
except Exception as e:
    print(f"❌ Error: {e}")

print()

# Test 4: Verify file structure
print("Test 4: Checking file structure...")
import os
required_files = [
    "requirements.txt",
    "founders_db.json", 
    "mcp_server.py",
    "agent.py",
    "demo.py",
    "README.md"
]

for file in required_files:
    if os.path.exists(file):
        print(f"✅ {file}")
    else:
        print(f"❌ {file} missing")

print()
print("=" * 60)
print("Basic tests complete!")
print("=" * 60)
print()
print("To run the full demo:")
print("  1. Install dependencies: pip install -r requirements.txt")
print("  2. Set ANTHROPIC_API_KEY environment variable")
print("  3. Run: python demo.py")
print()













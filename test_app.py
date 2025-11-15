#!/usr/bin/env python3
"""
Simple test script to verify the application works
"""

import sys
import json

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    try:
        import flask
        print("  ✓ Flask")
        import anthropic
        print("  ✓ Anthropic")
        from sentence_transformers import SentenceTransformer
        print("  ✓ Sentence Transformers")
        import numpy
        print("  ✓ NumPy")
        from db_manager import DatabaseManager
        print("  ✓ Database Manager")
        print("✅ All imports successful!\n")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database():
    """Test database operations"""
    print("Testing database...")
    try:
        from db_manager import DatabaseManager
        db = DatabaseManager("database.json")
        
        # Test read operations
        users = db.get_all_users()
        print(f"  ✓ Found {len(users)} users")
        
        needs = db.get_all_active_needs()
        print(f"  ✓ Found {len(needs)} active needs")
        
        learnings = db.get_all_active_learnings()
        print(f"  ✓ Found {len(learnings)} active learnings")
        
        matches = db.get_all_matches()
        print(f"  ✓ Found {len(matches)} matches")
        
        stats = db.get_dashboard_stats()
        print(f"  ✓ Dashboard stats: {stats['total_users']} users, {stats['total_matches']} matches")
        
        print("✅ Database tests passed!\n")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_mcp_extraction():
    """Test MCP extraction function"""
    print("Testing MCP extraction...")
    try:
        from app import extract_needs_learnings_tool
        
        test_text = "I'm stuck on ML deployment and scaling. I learned how to set up CI/CD."
        result = extract_needs_learnings_tool(test_text)
        
        print(f"  ✓ Extracted {len(result.get('needs', []))} needs")
        print(f"  ✓ Extracted {len(result.get('learnings', []))} learnings")
        
        if result.get('needs'):
            print(f"    Sample need: {result['needs'][0]['label']}")
        if result.get('learnings'):
            print(f"    Sample learning: {result['learnings'][0]['label']}")
        
        print("✅ Extraction tests passed!\n")
        return True
    except Exception as e:
        print(f"❌ Extraction error: {e}")
        return False

def test_mcp_matching():
    """Test MCP matching function"""
    print("Testing MCP matching...")
    try:
        from app import compute_matches_tool
        
        needs = [
            {
                "id": "n001",
                "user_id": "u001",
                "label": "ML deployment help",
                "category": "technical"
            }
        ]
        
        learnings = [
            {
                "id": "l001",
                "user_id": "u002",
                "label": "Scaled ML models to production",
                "category": "technical"
            }
        ]
        
        result = compute_matches_tool(needs, learnings)
        
        print(f"  ✓ Computed {result['total_matches']} matches")
        
        if result['matches']:
            match = result['matches'][0]
            print(f"    Match score: {match['score']}")
            print(f"    Reason: {match['reason'][:60]}...")
        
        print("✅ Matching tests passed!\n")
        return True
    except Exception as e:
        print(f"❌ Matching error: {e}")
        return False

def test_app_startup():
    """Test that Flask app can be created"""
    print("Testing Flask app creation...")
    try:
        from app import app
        
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            assert response.status_code == 200
            print("  ✓ Health endpoint working")
            
            # Test main page
            response = client.get('/')
            assert response.status_code == 200
            print("  ✓ Main page loads")
            
            # Test admin page
            response = client.get('/admin')
            assert response.status_code == 200
            print("  ✓ Admin page loads")
            
            # Test API endpoint
            response = client.get('/api/users')
            assert response.status_code == 200
            data = json.loads(response.data)
            print(f"  ✓ API endpoint working: {len(data['users'])} users")
        
        print("✅ Flask app tests passed!\n")
        return True
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 FOUNDER MATCHING PLATFORM - Test Suite")
    print("="*60)
    print()
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Database", test_database()))
    results.append(("MCP Extraction", test_mcp_extraction()))
    results.append(("MCP Matching", test_mcp_matching()))
    results.append(("Flask App", test_app_startup()))
    
    print("="*60)
    print("📊 Test Results Summary")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    print()
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("✅ All tests passed! App is ready to run!")
        print()
        print("Next steps:")
        print("  1. Run: python app.py")
        print("  2. Visit: http://localhost:5000")
        print("  3. Try the demo workflow")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())











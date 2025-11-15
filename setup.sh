#!/bin/bash
# Setup script for Founder Matching Agent

echo "🚀 Setting up Founder Matching Agent..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Set your Anthropic API key:"
echo "     export ANTHROPIC_API_KEY='your-key-here'"
echo ""
echo "  3. Run the demo:"
echo "     python3 demo.py"
echo ""
echo "  Or run a quick test:"
echo "     python3 agent.py"
echo ""













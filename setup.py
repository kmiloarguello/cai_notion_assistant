#!/usr/bin/env python3
"""
Setup script for Notion AI Assistant
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("Error output:", e.stderr)
        return False

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = ".env"
    if not os.path.exists(env_path):
        print("❌ .env file not found")
        create_env_template()
        return False
    
    required_vars = ["NOTION_API_KEY", "NOTION_DATABASE_ID", "OPENAI_API_KEY"]
    missing_vars = []
    
    with open(env_path, 'r') as f:
        content = f.read()
    
    for var in required_vars:
        if f"{var}=" not in content or f"{var}=\n" in content:
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Missing or empty environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease update your .env file with the required values.")
        return False
    
    print("✅ Environment variables configured")
    return True

def create_env_template():
    """Create a template .env file."""
    template = """# Notion AI Assistant Configuration
# Get your Notion API key from: https://www.notion.so/my-integrations
NOTION_API_KEY=your_notion_api_key_here

# Get your database ID from the Notion URL
# Example: if URL is https://www.notion.so/myworkspace/a8aec43384f447ed84390e8e42c2e089?v=...
# Then DATABASE_ID is: a8aec43384f447ed84390e8e42c2e089
NOTION_DATABASE_ID=your_notion_database_id_here

# Get your OpenAI API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Groq API key for alternative LLM
# GROQ_API_KEY=your_groq_api_key_here
"""
    
    with open(".env", "w") as f:
        f.write(template)
    
    print("📝 Created .env template file")
    print("Please edit .env and add your API keys")

def main():
    """Main setup function."""
    print("🚀 Setting up Notion AI Assistant...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check environment file
    env_ok = check_env_file()
    
    print("\n" + "=" * 50)
    
    if env_ok:
        print("✅ Setup completed successfully!")
        print("\nYou can now run the assistant with:")
        print("   python app.py")
        print("   or")
        print("   python run.py")
    else:
        print("⚠️  Setup partially completed")
        print("Please configure your .env file and run setup again")
        print("\nSteps to complete setup:")
        print("1. Edit .env file with your API keys")
        print("2. Run: python setup.py")
        print("3. Run: python app.py")

if __name__ == "__main__":
    main()

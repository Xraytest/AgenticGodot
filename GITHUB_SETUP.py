#!/usr/bin/env python3
"""
Quick setup guide for pushing AgenticGodot to GitHub
"""

import subprocess
import sys


GITHUB_SETUP = """
╔════════════════════════════════════════════════════════════════════════════╗
║                    AgenticGodot GitHub Setup Guide                         ║
╚════════════════════════════════════════════════════════════════════════════╝

STEP 1: Create GitHub Repository
================================
1. Go to https://github.com/new
2. Create a new repository:
   - Name: agentic-godot
   - Description: Godot Engine integrated with MCP servers (674+ tools)
   - Visibility: Public/Private (your choice)
   - DO NOT initialize with README (we have one)
   - DO NOT add .gitignore (we have one)

STEP 2: Add Remote and Push
===========================

Option A: Using HTTPS (password-protected)
-------------------------------------------
git remote add origin https://github.com/YOUR_USERNAME/agentic-godot.git
git branch -M main
git push -u origin main

You'll be prompted for username and password/token.

Option B: Using SSH (key-based authentication)
-----------------------------------------------
1. Generate SSH key (if you don't have one):
   ssh-keygen -t ed25519 -C "your-email@example.com"

2. Add SSH key to GitHub:
   - Go to https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your public key (~/.ssh/id_ed25519.pub)

3. Add remote and push:
   git remote add origin git@github.com:YOUR_USERNAME/agentic-godot.git
   git branch -M main
   git push -u origin main

STEP 3: Verify Push
==================
1. Check GitHub website - you should see all files
2. Verify build artifacts:
   git log --oneline --all

STEP 4: Enable GitHub Actions (Optional)
========================================
1. Create .github/workflows/build.yml
2. Set up automated builds on push
3. Enable branch protection rules

═══════════════════════════════════════════════════════════════════════════════

Current Repository Status:
- Location: c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot
- Git initialized: ✓
- Initial commit: ✓ (3613853)
- Files ready: ✓ (17 files, 7890+ lines)
- Tools defined: ✓ (674 MCP tools)
- Build scripts: ✓ (master_build.py)

Next Steps:
1. Create GitHub repository
2. Update the remote URL below
3. Run: git push -u origin main

Remote Configuration:
=====================
To set the remote URL, run:

  git remote set-url origin https://github.com/YOUR_USERNAME/agentic-godot.git

Then push:

  git push -u origin main

For automation, you can use the github_integration.py script:

  python scripts/github_integration.py \\
    --repo-url https://github.com/YOUR_USERNAME/agentic-godot.git \\
    --commit "Build: <message>" \\
    --push

═══════════════════════════════════════════════════════════════════════════════
"""

print(GITHUB_SETUP)

# Show current status
print("\n✓ Current Git Status:")
try:
    result = subprocess.run(['git', 'config', '--get', 'remote.origin.url'],
                          capture_output=True, text=True,
                          cwd='c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot')
    if result.stdout.strip():
        print(f"  Remote: {result.stdout.strip()}")
    else:
        print("  Remote: NOT SET (use instructions above)")
except:
    print("  Remote: Cannot determine")

try:
    result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                          capture_output=True, text=True,
                          cwd='c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot')
    print(f"  Branch: {result.stdout.strip()}")
except:
    pass

try:
    result = subprocess.run(['git', 'log', '-1', '--pretty=format:%H %s'],
                          capture_output=True, text=True,
                          cwd='c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot')
    print(f"  Latest: {result.stdout.strip()}")
except:
    pass

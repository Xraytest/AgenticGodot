#!/usr/bin/env python3
"""
GitHub Integration Script
Initializes repository and handles automated commits/pushes
"""

import os
import subprocess
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('GitHubIntegration')


class GitHubIntegration:
    def __init__(self, repo_url: str = None, local_path: str = None):
        self.repo_url = repo_url
        self.local_path = Path(local_path) if local_path else Path.cwd()
        self.git_dir = self.local_path / '.git'
    
    def is_git_repo(self) -> bool:
        """Check if current directory is a git repository"""
        return self.git_dir.exists()
    
    def initialize_repo(self, repo_url: str) -> bool:
        """Initialize a git repository"""
        logger.info("[*] Initializing git repository...")
        
        os.chdir(self.local_path)
        
        try:
            # Git init
            subprocess.run(['git', 'init'], check=True, capture_output=True)
            logger.info("[+] Git initialized")
            
            # Add remote
            subprocess.run(['git', 'remote', 'add', 'origin', repo_url], 
                         check=True, capture_output=True)
            logger.info(f"[+] Remote added: {repo_url}")
            
            # Configure user
            subprocess.run(['git', 'config', 'user.email', 'agentic@godot.local'],
                         check=True, capture_output=True)
            subprocess.run(['git', 'config', 'user.name', 'AgenticGodot'],
                         check=True, capture_output=True)
            logger.info("[+] Git user configured")
            
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Git initialization failed: {e}")
            return False
    
    def add_all_files(self) -> bool:
        """Add all files to git staging"""
        logger.info("[*] Adding files to git...")
        
        try:
            subprocess.run(['git', 'add', '.'], check=True, capture_output=True, cwd=self.local_path)
            logger.info("[+] Files added to staging")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Failed to add files: {e}")
            return False
    
    def commit(self, message: str) -> bool:
        """Commit staged files"""
        logger.info(f"[*] Creating commit: {message}")
        
        try:
            subprocess.run(['git', 'commit', '-m', message], 
                         check=True, capture_output=True, cwd=self.local_path)
            logger.info("[+] Commit created")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Commit failed: {e}")
            return False
    
    def push(self, branch: str = 'main', force: bool = False) -> bool:
        """Push to remote repository"""
        logger.info(f"[*] Pushing to {branch}...")
        
        try:
            cmd = ['git', 'push', '-u', 'origin', branch]
            if force:
                cmd.insert(2, '--force')
            
            subprocess.run(cmd, check=True, capture_output=True, cwd=self.local_path)
            logger.info(f"[+] Pushed to {branch}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Push failed: {e}")
            return False
    
    def create_gitignore(self) -> bool:
        """Create .gitignore file"""
        logger.info("[*] Creating .gitignore...")
        
        gitignore_content = """# Build artifacts
bin/
build/
*.o
*.a
*.so
*.exe
*.dll
*.dylib

# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
.directory

# Godot
.godot/
*.import
export_presets.cfg
.mono/
mono_crash.*.json

# MCP
*.log
mcp_server/logs/

# Sensitive
*.key
*.pem
ssh_config
credentials.json
"""
        
        gitignore_path = self.local_path / '.gitignore'
        
        try:
            gitignore_path.write_text(gitignore_content)
            logger.info("[+] .gitignore created")
            return True
        except Exception as e:
            logger.error(f"[!] Failed to create .gitignore: {e}")
            return False
    
    def commit_and_push(self, message: str, branch: str = 'main') -> bool:
        """Add all files, commit, and push"""
        logger.info("[*] Starting commit and push process...")
        
        if not self.add_all_files():
            return False
        
        if not self.commit(message):
            return False
        
        if not self.push(branch):
            return False
        
        logger.info("[+] Commit and push completed")
        return True


def main():
    parser = argparse.ArgumentParser(description='GitHub integration for AgenticGodot')
    parser.add_argument('--repo-url', help='GitHub repository URL')
    parser.add_argument('--local-path', default='.', help='Local repository path')
    parser.add_argument('--init', action='store_true', help='Initialize new repository')
    parser.add_argument('--commit', help='Commit message')
    parser.add_argument('--push', action='store_true', help='Push to remote')
    parser.add_argument('--branch', default='main', help='Git branch')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("GitHub Integration")
    logger.info("=" * 60)
    
    integration = GitHubIntegration(repo_url=args.repo_url, local_path=args.local_path)
    
    if args.init and args.repo_url:
        # Initialize new repository
        if not integration.initialize_repo(args.repo_url):
            exit(1)
        
        # Create .gitignore
        integration.create_gitignore()
        
        # Initial commit
        if not integration.commit_and_push(
            "Initial commit: AgenticGodot foundation with 600+ MCP tools",
            branch=args.branch
        ):
            exit(1)
        
        logger.info("[+] Repository initialized and pushed")
    
    elif args.commit:
        # Commit and optionally push
        if not integration.is_git_repo():
            logger.error("[!] Not a git repository")
            exit(1)
        
        if not integration.add_all_files():
            exit(1)
        
        if not integration.commit(args.commit):
            exit(1)
        
        if args.push:
            if not integration.push(branch=args.branch):
                exit(1)
    
    logger.info("[+] GitHub integration completed")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Godot MCP Launcher
Starts the MCP server and Godot together
Supports both GUI and headless modes
"""

import os
import sys
import subprocess
import time
import argparse
import logging
from pathlib import Path
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('GodotMCPLauncher')


class GodotMCPLauncher:
    def __init__(self, godot_binary: str, mcp_port: int = 6005, headless: bool = False):
        self.godot_binary = godot_binary
        self.mcp_port = mcp_port
        self.headless = headless
        self.mcp_process = None
        self.godot_process = None
        self.tools_dir = str(Path(__file__).parent.parent / "tools_definition")
    
    def start_mcp_server(self):
        """Start the MCP server before Godot"""
        logger.info("[*] Starting MCP server...")
        
        mcp_script = str(Path(__file__).parent / "godot_mcp_server.py")
        
        env = os.environ.copy()
        env['GODOT_MCP_PORT'] = str(self.mcp_port)
        env['GODOT_TOOLS_DIR'] = self.tools_dir
        
        try:
            self.mcp_process = subprocess.Popen(
                [sys.executable, mcp_script],
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info(f"[+] MCP server started (PID: {self.mcp_process.pid})")
            
            # Wait for MCP server to be ready
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"[!] Failed to start MCP server: {e}")
            return False
    
    def start_godot(self, project_path: str = None, scene: str = None):
        """Start Godot with MCP enabled"""
        logger.info("[*] Starting Godot...")
        
        cmd = [self.godot_binary]
        
        # Add headless flag if needed
        if self.headless:
            cmd.append("--headless")
            logger.info("[*] Running in headless mode")
        
        # Add project path
        if project_path:
            cmd.append(f"--path={project_path}")
        
        # Add scene to play
        if scene:
            cmd.append(scene)
        
        # Set environment variables
        env = os.environ.copy()
        env['GODOT_MCP_PORT'] = str(self.mcp_port)
        env['GODOT_MCP_ENABLED'] = '1'
        
        try:
            self.godot_process = subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            logger.info(f"[+] Godot started (PID: {self.godot_process.pid})")
            logger.info(f"[*] MCP server available at localhost:{self.mcp_port}")
            return True
        except Exception as e:
            logger.error(f"[!] Failed to start Godot: {e}")
            return False
    
    def wait_for_completion(self):
        """Wait for both processes to complete"""
        try:
            logger.info("[*] Waiting for Godot to complete...")
            self.godot_process.wait()
            logger.info("[+] Godot process completed")
        except KeyboardInterrupt:
            logger.info("[*] Received interrupt signal")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown both MCP server and Godot"""
        logger.info("[*] Shutting down...")
        
        if self.godot_process:
            try:
                self.godot_process.terminate()
                self.godot_process.wait(timeout=5)
                logger.info("[+] Godot process terminated")
            except:
                self.godot_process.kill()
                logger.warning("[!] Godot process killed")
        
        if self.mcp_process:
            try:
                self.mcp_process.terminate()
                self.mcp_process.wait(timeout=5)
                logger.info("[+] MCP server terminated")
            except:
                self.mcp_process.kill()
                logger.warning("[!] MCP server killed")


def main():
    parser = argparse.ArgumentParser(description='Launch Godot with MCP server')
    parser.add_argument('godot_binary', help='Path to Godot executable')
    parser.add_argument('--project', '-p', help='Project directory path')
    parser.add_argument('--scene', '-s', help='Scene to play')
    parser.add_argument('--port', type=int, default=6005, help='MCP server port (default: 6005)')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Godot MCP Launcher")
    logger.info("=" * 60)
    
    # Create launcher
    launcher = GodotMCPLauncher(
        godot_binary=args.godot_binary,
        mcp_port=args.port,
        headless=args.headless
    )
    
    # Start MCP server
    if not launcher.start_mcp_server():
        logger.error("[!] Failed to start MCP server")
        sys.exit(1)
    
    # Start Godot
    if not launcher.start_godot(project_path=args.project, scene=args.scene):
        logger.error("[!] Failed to start Godot")
        launcher.shutdown()
        sys.exit(1)
    
    # Wait for completion
    launcher.wait_for_completion()
    
    logger.info("[+] Launcher shutdown complete")


if __name__ == "__main__":
    main()

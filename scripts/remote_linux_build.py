#!/usr/bin/env python3
"""
Remote Linux Build Script
Compiles Godot for Linux ARM64 on remote server
"""

import os
import sys
import subprocess
import argparse
import logging
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('RemoteLinuxBuild')


class RemoteBuilder:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.remote_dir = '/tmp/agentic_godot_build'
    
    def execute_remote_command(self, command: str) -> bool:
        """Execute command on remote server via SSH"""
        # Using SSH to execute command
        ssh_cmd = [
            'ssh',
            f'-p{self.port}',
            f'{self.username}@{self.host}',
            command
        ]
        
        logger.info(f"[>] Remote: {command}")
        
        try:
            result = subprocess.run(ssh_cmd, check=True, capture_output=True, text=True)
            if result.stdout:
                logger.info(f"[<] {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Remote command failed: {e}")
            if e.stderr:
                logger.error(f"[<] {e.stderr}")
            return False
    
    def setup_remote_build_environment(self) -> bool:
        """Setup build environment on remote server"""
        logger.info("[*] Setting up remote build environment...")
        
        # Create remote directory
        if not self.execute_remote_command(f'mkdir -p {self.remote_dir}'):
            return False
        
        # Install dependencies
        commands = [
            'apt-get update',
            'apt-get install -y build-essential scons pkg-config libx11-dev libxcursor-dev libxinerama-dev libgl-dev python3 python3-pip',
            'pip3 install scons',
        ]
        
        for cmd in commands:
            if not self.execute_remote_command(cmd):
                logger.warning(f"[!] Command failed: {cmd}")
        
        logger.info("[+] Remote build environment ready")
        return True
    
    def transfer_source(self, local_source_dir: str) -> bool:
        """Transfer Godot source to remote server"""
        logger.info("[*] Transferring Godot source to remote server...")
        
        # Using rsync for efficient transfer
        rsync_cmd = [
            'rsync',
            '-avz',
            '--exclude=.git',
            '--exclude=bin',
            '--exclude=build',
            f'{local_source_dir}/',
            f'{self.username}@{self.host}:{self.remote_dir}/godot_source/'
        ]
        
        logger.info(f"[>] Running: rsync")
        
        try:
            subprocess.run(rsync_cmd, check=True)
            logger.info("[+] Source transferred successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Transfer failed: {e}")
            return False
    
    def build_linux_arm64(self, target: str = 'release') -> bool:
        """Build Godot for Linux ARM64"""
        logger.info(f"[*] Building Godot for Linux ARM64 ({target})...")
        
        build_cmd = (
            f'cd {self.remote_dir}/godot_source && '
            f'scons platform=linuxbsd target={target} arch=arm64 disable_3d=no progress=yes -j4'
        )
        
        if not self.execute_remote_command(build_cmd):
            return False
        
        logger.info("[+] Build completed successfully")
        return True
    
    def build_linux_x86_64(self, target: str = 'release', headless: bool = True) -> bool:
        """Build Godot for Linux x86_64"""
        logger.info(f"[*] Building Godot for Linux x86_64 ({target}, headless={headless})...")
        
        build_cmd = (
            f'cd {self.remote_dir}/godot_source && '
            f'scons platform=linuxbsd target={target} arch=x86_64 disable_3d=no progress=yes -j4'
        )
        
        if not self.execute_remote_command(build_cmd):
            return False
        
        logger.info("[+] Build completed successfully")
        return True
    
    def transfer_build_output(self, local_build_dir: str) -> bool:
        """Transfer compiled binaries back to local machine"""
        logger.info("[*] Transferring build output from remote server...")
        
        rsync_cmd = [
            'rsync',
            '-avz',
            f'{self.username}@{self.host}:{self.remote_dir}/godot_source/bin/',
            f'{local_build_dir}/'
        ]
        
        logger.info(f"[>] Running: rsync")
        
        try:
            subprocess.run(rsync_cmd, check=True)
            logger.info("[+] Build output transferred successfully")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Transfer failed: {e}")
            return False
    
    def cleanup_remote(self) -> bool:
        """Cleanup remote build directory"""
        logger.info("[*] Cleaning up remote server...")
        
        return self.execute_remote_command(f'rm -rf {self.remote_dir}')


def main():
    parser = argparse.ArgumentParser(description='Build Godot for Linux on remote server')
    parser.add_argument('--host', required=True, help='Remote server host')
    parser.add_argument('--port', type=int, default=22, help='SSH port')
    parser.add_argument('--username', required=True, help='SSH username')
    parser.add_argument('--password', help='SSH password (if needed)')
    parser.add_argument('--source', default='c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot\\godot_source',
                       help='Local Godot source directory')
    parser.add_argument('--build-dir', default='c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot\\build',
                       help='Local build output directory')
    parser.add_argument('--target', choices=['debug', 'release'], default='release',
                       help='Build target')
    parser.add_argument('--arch', choices=['arm64', 'x86_64'], default='arm64',
                       help='Target architecture')
    parser.add_argument('--headless', action='store_true', help='Build headless')
    parser.add_argument('--cleanup', action='store_true', help='Cleanup remote after build')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Remote Linux Build System")
    logger.info("=" * 60)
    
    builder = RemoteBuilder(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password
    )
    
    try:
        # Setup
        if not builder.setup_remote_build_environment():
            sys.exit(1)
        
        # Transfer source
        if not builder.transfer_source(args.source):
            sys.exit(1)
        
        # Build
        if args.arch == 'arm64':
            if not builder.build_linux_arm64(target=args.target):
                sys.exit(1)
        else:
            if not builder.build_linux_x86_64(target=args.target, headless=args.headless):
                sys.exit(1)
        
        # Transfer output
        Path(args.build_dir).mkdir(parents=True, exist_ok=True)
        if not builder.transfer_build_output(args.build_dir):
            sys.exit(1)
        
        logger.info("[+] Remote build completed successfully")
        logger.info(f"[*] Output: {args.build_dir}")
        
    finally:
        if args.cleanup:
            builder.cleanup_remote()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Remote Linux Build Script v2 - Clones from GitHub then builds
"""
import os, sys, subprocess, argparse, logging, time, json
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('RemoteLinuxBuildV2')

class RemoteBuilderV2:
    def __init__(self, host, port, username, password, repo_url, branch="main"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.repo_url = repo_url
        self.branch = branch
        self.remote_dir = '/tmp/agentic_godot_build'

    def _ssh_cmd(self, cmd):
        full_cmd = f'ssh -o StrictHostKeyChecking=no -p {self.port} {self.username}@{self.host} "{cmd}"'
        logger.info(f"[>] {cmd[:100]}...")
        try:
            result = subprocess.run(full_cmd, shell=True, check=True, capture_output=True, text=True, timeout=600)
            if result.stdout.strip():
                logger.info(f"[<] {result.stdout.strip()[-200:]}")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] SSH failed: {e.stderr[-300:] if e.stderr else 'no stderr'}")
            return False, e.stderr
        except subprocess.TimeoutExpired:
            logger.error("[!] SSH timeout")
            return False, "timeout"

    def run(self, arch="x86_64", target="release", headless=True):
        logger.info(f"[*] Building Godot for Linux {arch} ({target}, headless={headless}) on {self.host}")
        
        commands = [
            f'mkdir -p {self.remote_dir} && cd {self.remote_dir} && rm -rf godot && git clone --depth 1 --branch {self.branch} {self.repo_url} godot 2>&1',
            f'cd {self.remote_dir}/godot/godot_source && scons platform=linuxbsd target={target} arch={arch} disable_3d=no progress=yes -j$(nproc) 2>&1',
            f'ls -la {self.remote_dir}/godot/godot_source/bin/ 2>&1',
        ]
        
        for i, cmd in enumerate(commands):
            logger.info(f"[*] Step {i+1}/{len(commands)}")
            success, output = self._ssh_cmd(cmd)
            if not success:
                logger.error(f"[!] Step {i+1} failed")
                return False
        
        logger.info("[+] Build completed successfully")
        return True

def main():
    parser = argparse.ArgumentParser(description='Remote Linux Godot Build v2')
    parser.add_argument('--host', default='192.168.1.3', help='Remote host')
    parser.add_argument('--port', type=int, default=22, help='SSH port')
    parser.add_argument('--username', default='xray4668', help='SSH username')
    parser.add_argument('--password', default='18248745', help='SSH password')
    parser.add_argument('--repo', default='https://github.com/Xraytest/AgenticGodot.git', help='Git repo URL')
    parser.add_argument('--branch', default='main', help='Git branch')
    parser.add_argument('--arch', default='x86_64', choices=['x86_64', 'arm64'])
    parser.add_argument('--target', default='release', choices=['debug', 'release'])
    parser.add_argument('--headless', action='store_true', default=True)
    
    args = parser.parse_args()
    builder = RemoteBuilderV2(args.host, args.port, args.username, args.password, args.repo, args.branch)
    success = builder.run(arch=args.arch, target=args.target, headless=args.headless)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
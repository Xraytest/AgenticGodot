#!/usr/bin/env python3
"""
Godot Build System for AgenticGodot
Supports multiple platforms with MCP server integration
"""

import os
import subprocess
import sys
import json
import shutil
from pathlib import Path
import platform
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('GodotBuildSystem')


class GodotBuilder:
    def __init__(self, godot_source_dir: str, build_dir: str):
        self.godot_source_dir = Path(godot_source_dir)
        self.build_dir = Path(build_dir)
        self.build_dir.mkdir(parents=True, exist_ok=True)
        self.system = platform.system()
    
    def check_dependencies(self) -> bool:
        """Check if build dependencies are installed"""
        logger.info("[*] Checking build dependencies...")
        
        required_tools = {
            'scons': 'SCons build system',
            'python': 'Python 3.7+',
        }
        
        if self.system == 'Windows':
            required_tools['cl'] = 'Visual C++ compiler'
        elif self.system == 'Linux':
            required_tools['gcc'] = 'GCC compiler'
            required_tools['g++'] = 'G++ compiler'
        
        missing = []
        for tool, desc in required_tools.items():
            if not shutil.which(tool):
                missing.append(f"{tool} ({desc})")
        
        if missing:
            logger.error(f"[!] Missing dependencies: {', '.join(missing)}")
            return False
        
        logger.info("[+] All dependencies found")
        return True
    
    def build_windows(self, target: str = 'release', arch: str = 'x86_64') -> bool:
        """Build Godot for Windows"""
        logger.info(f"[*] Building Godot for Windows ({arch}, {target})...")
        
        if not self.check_dependencies():
            return False
        
        os.chdir(self.godot_source_dir)
        
        # Build command
        cmd = [
            'scons',
            f'platform=windows',
            f'target={target}',
            f'arch={arch}',
            'progress=yes',
            '-j4',  # Use 4 cores
        ]
        
        logger.info(f"[>] Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True)
            
            # Find and copy the built executable
            bin_dir = self.godot_source_dir / 'bin'
            if bin_dir.exists():
                exe_name = f'godot.windows.{target}.{arch}.exe'
                exe_path = bin_dir / exe_name
                
                if exe_path.exists():
                    output_path = self.build_dir / 'godot_windows.exe'
                    shutil.copy2(exe_path, output_path)
                    logger.info(f"[+] Built executable: {output_path}")
                    return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Build failed: {e}")
            return False
        
        return False
    
    def build_linux(self, target: str = 'release', arch: str = 'x86_64', headless: bool = True) -> bool:
        """Build Godot for Linux"""
        logger.info(f"[*] Building Godot for Linux ({arch}, {target}, headless={headless})...")
        
        if not self.check_dependencies():
            return False
        
        os.chdir(self.godot_source_dir)
        
        # Build command
        cmd = [
            'scons',
            f'platform=linux',
            f'target={target}',
            f'arch={arch}',
            'progress=yes',
            '-j4',
        ]
        
        if headless:
            cmd.append('disable_3d=no')
            cmd.append('disable_2d=no')
        
        logger.info(f"[>] Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, check=True)
            
            # Find and copy the built executable
            bin_dir = self.godot_source_dir / 'bin'
            if bin_dir.exists():
                exe_name = f'godot.linuxbsd.{target}.{arch}'
                exe_path = bin_dir / exe_name
                
                if exe_path.exists():
                    suffix = '_headless' if headless else ''
                    output_path = self.build_dir / f'godot_linux{suffix}'
                    shutil.copy2(exe_path, output_path)
                    os.chmod(output_path, 0o755)
                    logger.info(f"[+] Built executable: {output_path}")
                    return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Build failed: {e}")
            return False
        
        return False
    
    def build_web(self, target: str = 'release') -> bool:
        """Build Godot for Web (Emscripten)"""
        logger.info(f"[*] Building Godot for Web ({target})...")
        
        os.chdir(self.godot_source_dir)
        
        cmd = [
            'scons',
            f'platform=web',
            f'target={target}',
            'progress=yes',
            '-j4',
        ]
        
        logger.info(f"[>] Running: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, check=True)
            logger.info("[+] Web build completed")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Build failed: {e}")
            return False
    
    def build_android(self, target: str = 'release') -> bool:
        """Build Godot for Android"""
        logger.info(f"[*] Building Godot for Android ({target})...")
        
        os.chdir(self.godot_source_dir)
        
        cmd = [
            'scons',
            f'platform=android',
            f'target={target}',
            'progress=yes',
            '-j4',
        ]
        
        logger.info(f"[>] Running: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, check=True)
            logger.info("[+] Android build completed")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"[!] Build failed: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Build Godot for AgenticGodot')
    parser.add_argument('--source', default='c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot\\godot_source',
                       help='Godot source directory')
    parser.add_argument('--build-dir', default='c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot\\build',
                       help='Build output directory')
    parser.add_argument('--target', choices=['debug', 'release'], default='release',
                       help='Build target (debug or release)')
    parser.add_argument('--platform', choices=['windows', 'linux', 'web', 'android', 'all'],
                       default='windows', help='Target platform')
    parser.add_argument('--arch', choices=['x86_64', 'arm64', 'x86_32'], default='x86_64',
                       help='Target architecture')
    parser.add_argument('--headless', action='store_true', help='Build headless mode for Linux')
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Godot Build System for AgenticGodot")
    logger.info("=" * 60)
    
    builder = GodotBuilder(args.source, args.build_dir)
    
    success = True
    
    if args.platform in ['windows', 'all']:
        if not builder.build_windows(target=args.target, arch=args.arch):
            success = False
    
    if args.platform in ['linux', 'all']:
        if not builder.build_linux(target=args.target, arch=args.arch, headless=args.headless):
            success = False
    
    if args.platform in ['web', 'all']:
        if not builder.build_web(target=args.target):
            success = False
    
    if args.platform in ['android', 'all']:
        if not builder.build_android(target=args.target):
            success = False
    
    if success:
        logger.info("[+] All builds completed successfully")
        logger.info(f"[*] Output: {args.build_dir}")
        sys.exit(0)
    else:
        logger.error("[!] Some builds failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

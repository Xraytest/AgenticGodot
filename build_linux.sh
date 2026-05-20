#!/bin/bash
# Linux Build Script
# Quick build script for Linux platform

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║              AgenticGodot - Linux Build Script                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[!] Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check SCons
if ! command -v scons &> /dev/null; then
    echo "[!] SCons not found. Installing..."
    pip3 install scons
fi

# Create output directory
mkdir -p build

# Check for remote build flag
if [ "$1" == "--remote" ]; then
    echo "[*] Starting remote Linux build on 192.168.1.3..."
    python3 scripts/master_build.py --linux-only --push-github
else
    echo "[*] Starting local Linux build..."
    python3 scripts/master_build.py --linux-only --skip-tests
fi

if [ $? -ne 0 ]; then
    echo "[!] Build failed!"
    exit 1
fi

echo ""
echo "[+] Build completed successfully!"
echo "[*] Output: ./build/"
echo ""

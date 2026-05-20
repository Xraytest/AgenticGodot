#!/usr/bin/env bash
# Windows Build Script
# Quick build script for Windows platform

@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

echo.
echo ╔════════════════════════════════════════════════════════════════════════════╗
echo ║              AgenticGodot - Windows Build Script                           ║
echo ╚════════════════════════════════════════════════════════════════════════════╝
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [!] Python not found. Please install Python 3.8+
    exit /b 1
)

REM Check SCons
scons --version >nul 2>&1
if errorlevel 1 (
    echo [!] SCons not found. Installing...
    pip install scons
)

REM Create output directory
if not exist "build" mkdir build

REM Run master build
echo [*] Starting Windows build...
python scripts/master_build.py --windows-only --skip-tests

if errorlevel 1 (
    echo [!] Build failed!
    exit /b 1
)

echo.
echo [+] Build completed successfully!
echo [*] Output: build\godot_windows.exe
echo.

pause

#!/usr/bin/env python3
"""
AgenticGodot - Getting Started Guide
Provides setup instructions and quick start examples
"""

GETTING_STARTED = """
╔════════════════════════════════════════════════════════════════════════════╗
║                     AgenticGodot Getting Started                           ║
║                                                                            ║
║    Godot Engine + MCP Protocol Integration                                ║
║    674 Controllable Tools (306 Visual + 368 Control)                      ║
╚════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TABLE OF CONTENTS
=================
1. Prerequisites & Installation
2. Building Godot
3. Running the MCP Server
4. Connecting Clients
5. Example Workflows
6. Troubleshooting

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. PREREQUISITES & INSTALLATION
===============================

System Requirements:
  • Windows 10+ / Linux (Ubuntu 20.04+) / macOS
  • Python 3.8+
  • 50GB+ disk space (for Godot compilation)
  • 8GB+ RAM (for compilation)

Install Python Dependencies:
  $ pip install -r requirements.txt

Verify Installation:
  $ python --version
  $ scons --version
  $ git --version

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2. BUILDING GODOT
================

Quick Build (Windows):
  $ python scripts/master_build.py --windows-only

Quick Build (Linux local):
  $ python scripts/master_build.py --linux-only

Quick Build (Linux remote on 192.168.1.3):
  $ python scripts/master_build.py --linux-only --push-github

Build All Platforms:
  $ python scripts/master_build.py

Advanced Options:
  --config FILE          Use custom build configuration
  --skip-tests          Skip test execution
  --push-github         Commit and push to GitHub
  --no-validate         Skip tool validation

Build Process (typical):
  1. Validates tools (674 definitions)
  2. Compiles Godot for selected platforms
  3. Runs optional tests
  4. Creates build manifest
  5. Optionally commits to GitHub

Estimated Times:
  • Windows (clean): 30-60 minutes
  • Linux (clean): 45-90 minutes
  • Remote Linux: 60-120 minutes (depending on network)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3. RUNNING THE MCP SERVER
=========================

With Godot GUI (Windows/Linux Desktop):
  $ python mcp_server/godot_mcp_launcher.py build/godot_windows.exe \\
      --project /path/to/project \\
      --port 6005

Headless Mode (Linux Server):
  $ python mcp_server/godot_mcp_launcher.py build/godot_linux_arm64 \\
      --headless \\
      --port 6005

The launcher will:
  1. Start MCP server on port 6005
  2. Wait for MCP to be ready
  3. Launch Godot process
  4. Expose 674 tools via MCP protocol

Server Output Example:
  [2026-05-20 10:15:30] - GodotMCP - INFO - Starting MCP server on port 6005
  [2026-05-20 10:15:32] - GodotMCP - INFO - Loaded 674 tools total
  [2026-05-20 10:15:33] - GodotMCP - INFO - MCP server listening on port 6005...
  [2026-05-20 10:15:35] - GodotMCPLauncher - INFO - MCP server started (PID: 1234)
  [2026-05-20 10:15:40] - GodotMCPLauncher - INFO - Godot started (PID: 5678)
  [2026-05-20 10:15:40] - GodotMCPLauncher - INFO - MCP server available at localhost:6005

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4. CONNECTING CLIENTS
====================

Python Client Example:
  import socket
  import json
  
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect(('localhost', 6005))
  
  # Request tool list
  request = {
      "jsonrpc": "2.0",
      "method": "tools/list",
      "id": 1
  }
  
  sock.send(json.dumps(request).encode('utf-8'))
  response = json.loads(sock.recv(4096).decode('utf-8'))
  print(response)

Call a Visual Tool:
  request = {
      "jsonrpc": "2.0",
      "method": "tool/call",
      "params": {
          "tool_id": "vis_render_visual_viewport_camera",
          "arguments": {}
      },
      "id": 2
  }
  sock.send(json.dumps(request).encode('utf-8'))
  response = json.loads(sock.recv(4096).decode('utf-8'))
  print(f"Preview: {response['result']['preview']}")

Call a Control Tool:
  request = {
      "jsonrpc": "2.0",
      "method": "tool/call",
      "params": {
          "tool_id": "ctrl_prop_control_position",
          "arguments": {
              "value": [10, 20, 30]
          }
      },
      "id": 3
  }

Get Visual Tools Only:
  request = {
      "jsonrpc": "2.0",
      "method": "tools/visual/list",
      "id": 4
  }

Get Control Tools Only:
  request = {
      "jsonrpc": "2.0",
      "method": "tools/control/list",
      "id": 5
  }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. EXAMPLE WORKFLOWS
===================

Workflow 1: Automated Scene Control
-----------------------------------
goal: Programmatically create and control nodes in Godot

Steps:
  1. Connect MCP client to localhost:6005
  2. Call "ctrl_node_control_create_Node3D" with arguments
  3. Call "ctrl_prop_control_position" to set node position
  4. Call "vis_node_visual_Node3D" to get node preview
  5. Repeat for other nodes

Workflow 2: Camera Control
--------------------------
goal: Control viewport camera programmatically

Steps:
  1. Call "ctrl_camera_orbit_left" to rotate view
  2. Call "ctrl_camera_zoom_in" to zoom
  3. Call "vis_render_visual_viewport_camera" to get preview
  4. Use preview for feedback

Workflow 3: Animation Control
-----------------------------
goal: Create and modify animations via MCP

Steps:
  1. Call "ctrl_anim_control_add_keyframe" to add keyframes
  2. Call "ctrl_anim_control_modify_keyframe_value" to edit
  3. Call "vis_anim_visual_timeline" to get timeline preview
  4. Call "ctrl_anim_control_playback_position" to seek

Workflow 4: Build and Test
--------------------------
goal: Build project and run tests via MCP

Steps:
  1. Call "ctrl_build_build_project"
  2. Call "ctrl_build_run_tests"
  3. Call "vis_monitor_performance_metrics" to check results

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6. TROUBLESHOOTING
=================

Issue: MCP server won't start
  Solution:
    1. Check port 6005 is not in use: netstat -an | grep 6005
    2. Verify Python version: python --version (should be 3.8+)
    3. Check logs in build/build.log
    4. Try different port: --port 6006

Issue: Connection refused on port 6005
  Solution:
    1. Verify MCP server is running
    2. Wait 3-5 seconds after launch (startup time)
    3. Check firewall settings
    4. Look for error messages in console

Issue: Tools not loading
  Solution:
    1. Verify tools_definition/ directory exists
    2. Check JSON files are valid: python -m json.tool tools_definition/visual/tools.json
    3. Review tool count in project_config.json
    4. Check MCP server logs

Issue: Build fails on Windows
  Solution:
    1. Install Visual C++ Build Tools
    2. Verify SCons: pip install --upgrade scons
    3. Run: scons --version
    4. Check build logs: build/build.log

Issue: Remote Linux build fails
  Solution:
    1. Test SSH connection: ssh -p 22 xray4668@192.168.1.3
    2. Verify space on remote: ssh xray4668@192.168.1.3 'df -h'
    3. Check build timeout (increase in build_config.json)
    4. Review remote build logs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DIRECTORY STRUCTURE
===================
AgenticGodot/
  ├── godot_source/              # Godot 4.3.1 source (11K files)
  ├── mcp_server/                # MCP server & launcher
  ├── tools_definition/          # 674 tool definitions
  │   ├── visual/               # 310 visual tools
  │   └── control/              # 364 control tools
  ├── scripts/                   # Build & automation
  ├── build/                     # Compiled binaries
  ├── build_config.json          # Build settings
  ├── project_config.json        # Project metadata
  ├── README.md                  # Full documentation
  └── requirements.txt           # Python dependencies

KEY FILES
=========
godot_mcp_launcher.py           Main entry point for running Godot + MCP
godot_mcp_server.py             MCP protocol server
master_build.py                 Complete build orchestration
build_godot.py                  Platform-specific compilation
remote_linux_build.py           Remote SSH compilation

USEFUL COMMANDS
===============
$ python scripts/master_build.py --windows-only
  - Build Windows version locally

$ python scripts/master_build.py --linux-only
  - Build Linux version locally

$ python scripts/build_godot.py --platform linux --arch arm64 --headless
  - Build headless Linux for ARM64

$ python mcp_server/godot_mcp_launcher.py build/godot_windows.exe
  - Launch Godot with MCP server

$ python scripts/analyze_godot_api.py
  - Re-analyze Godot source for tool definitions

$ python scripts/github_integration.py --commit "message" --push
  - Commit and push to GitHub

QUICK REFERENCE
===============
Port:           6005 (MCP server)
Protocol:       JSON-RPC 2.0 over TCP
Tools:          674 (310 visual + 364 control)
Godot Version:  4.3.1 RC
Build Time:     30-90 minutes (depending on platform)
Min Disk:       50GB

╔════════════════════════════════════════════════════════════════════════════╗
║                         Happy Building! 🚀                                 ║
║                                                                            ║
║    For detailed documentation, see README.md in the project root          ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(GETTING_STARTED)

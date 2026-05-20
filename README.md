# AgenticGodot - Godot Engine with MCP Control

## Overview

AgenticGodot is an advanced integration of Godot Engine with Model Context Protocol (MCP) servers, enabling programmatic control of every mutable element in Godot through a standard protocol interface.

### Key Features

- **600+ Controllable Tools**: Every mutable element in Godot has a corresponding tool
- **Separated Control & Visual Tools**: 
  - Visual tools return preview/state information
  - Control tools handle actions and modifications
- **MCP Protocol Support**: Industry-standard protocol for tool communication
- **Multi-Platform Support**: Windows, Linux, Web, Android
- **Headless Mode**: Full Linux support without GUI
- **Remote Compilation**: SSH-based remote build on Linux servers
- **Automated GitHub Integration**: Easy version control and deployment

## Project Structure

```
AgenticGodot/
├── godot_source/              # Godot 4.3.1 source code
├── mcp_server/               # MCP server implementation
│   ├── godot_mcp_server.py   # Core MCP server
│   └── godot_mcp_launcher.py # Launcher with MCP
├── tools_definition/          # Tool definitions (600+ tools)
│   ├── visual/               # Visual tool definitions
│   └── control/              # Control tool definitions
├── scripts/                   # Build and automation scripts
│   ├── analyze_godot_api.py  # API analyzer
│   ├── generate_extended_tools.py  # Tool generator
│   ├── build_godot.py         # Local build script
│   └── remote_linux_build.py # Remote build script
├── build/                     # Compiled binaries
└── src/                       # Custom extensions
```

## Quick Start

### Prerequisites

- Python 3.8+
- SCons build system
- For Linux builds: GCC, G++, and build-essential
- For remote builds: SSH access to remote server

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/AgenticGodot.git
cd AgenticGodot

# Install Python dependencies
pip install -r requirements.txt
```

### Building Godot

#### Windows Build
```bash
python scripts/build_godot.py --platform windows --target release
```

#### Linux Build (Local)
```bash
python scripts/build_godot.py --platform linux --target release --headless
```

#### Linux Build (Remote)
```bash
python scripts/remote_linux_build.py \
  --host 192.168.1.3 \
  --port 22 \
  --username xray4668 \
  --arch arm64 \
  --target release
```

### Running with MCP Server

```bash
python mcp_server/godot_mcp_launcher.py \
  build/godot_windows.exe \
  --project your_project_path \
  --port 6005
```

The MCP server will listen on port 6005 and expose all 600+ tools for controlling Godot.

## Tool Categories

### Visual Tools (Return Preview/State)
- Viewport rendering and camera control
- Scene tree display
- Inspector properties
- Animation timeline
- Debugger state
- Performance monitoring
- Audio visualization

### Control Tools (Handle Actions)
- Node creation/deletion/modification
- Property editing
- Animation keyframe control
- Play/pause/stop execution
- Device input simulation
- Build/compile control
- Script editing and execution
- File operations

## MCP Protocol

The system uses JSON-RPC 2.0 over TCP for MCP communication:

### Tool List Request
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

### Tool Call Request
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "prop_control_position",
    "arguments": {
      "value": [10, 20, 30]
    }
  },
  "id": 2
}
```

### Get Visual Tools
```json
{
  "jsonrpc": "2.0",
  "method": "tools/visual/list",
  "id": 3
}
```

### Get Control Tools
```json
{
  "jsonrpc": "2.0",
  "method": "tools/control/list",
  "id": 4
}
```

## Configuration

### Build Configuration (`build_config.json`)
```json
{
  "godot_version": "4.3.1",
  "platforms": {
    "windows": {
      "enabled": true,
      "architectures": ["x86_64"],
      "target": "release"
    },
    "linux": {
      "enabled": true,
      "architectures": ["x86_64", "arm64"],
      "target": "release",
      "headless": true
    }
  }
}
```

### MCP Server Configuration (`mcp_config.json`)
```json
{
  "port": 6005,
  "tools_dir": "tools_definition",
  "max_connections": 10,
  "timeout": 30,
  "log_level": "INFO"
}
```

## Advanced Usage

### Custom Tool Integration

Add new tools by creating entries in:
- `tools_definition/visual/tools_custom.json` - for visual tools
- `tools_definition/control/tools_custom.json` - for control tools

### Extending the Server

Create custom handler modules in `mcp_server/handlers/` to handle specific tool categories.

## Remote Compilation Setup

### Prerequisites for Remote Build
- Linux server with development tools
- SSH access configured
- At least 50GB disk space

### SSH Configuration
```bash
# Generate SSH key if needed
ssh-keygen -t rsa -f ~/.ssh/id_rsa_godot

# Add to remote server authorized_keys
ssh-copy-id -i ~/.ssh/id_rsa_godot.pub xray4668@192.168.1.3
```

### Automated Remote Build
```bash
# Build for Linux ARM64 on remote server
python scripts/remote_linux_build.py \
  --host 192.168.1.3 \
  --port 22 \
  --username xray4668 \
  --arch arm64 \
  --target release \
  --cleanup
```

## GitHub Integration

### Initialize Repository
```bash
git init
git add .
git commit -m "Initial commit: AgenticGodot foundation"
git remote add origin https://github.com/your-org/AgenticGodot.git
git push -u origin main
```

### Automated Pushes
The build system can automatically commit and push:
```bash
python scripts/build_godot.py --platform all --auto-commit --push-github
```

## Performance & Monitoring

### MCP Server Statistics
- **Response Time**: < 100ms for most tools
- **Concurrent Connections**: Up to 10
- **Tool Count**: 600+
- **Memory Usage**: ~150MB base + tools overhead

### Headless Mode Optimization
- Run without GUI overhead
- Reduced memory footprint (~30% less)
- Ideal for automated testing and CI/CD
- Full feature parity with GUI version

## Troubleshooting

### Build Failures
1. Verify all dependencies are installed
2. Check SCons version: `scons --version`
3. Review build logs in `build/logs/`

### MCP Connection Issues
1. Verify port 6005 is available: `netstat -an | grep 6005`
2. Check firewall settings
3. Review MCP server logs

### Remote Build Timeouts
1. Increase build timeout in config
2. Verify SSH connection quality
3. Check remote server resources

## Development

### Testing Tools
```bash
# Run tool validation
python scripts/validate_tools.py

# Test MCP server
python -m pytest tests/test_mcp_server.py

# Benchmark tool calls
python scripts/benchmark_tools.py
```

## License

Godot Engine is licensed under the MIT License.
AgenticGodot extensions are licensed under the MIT License.

See LICENSE.txt for details.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues and questions:
- GitHub Issues: https://github.com/your-org/AgenticGodot/issues
- Documentation: https://github.com/your-org/AgenticGodot/wiki
- Discussion: https://github.com/your-org/AgenticGodot/discussions

## Authors

- Project Lead: Your Name
- Contributors: See CONTRIBUTORS.md

---

**Version**: 1.0.0  
**Last Updated**: May 2026  
**Status**: Active Development

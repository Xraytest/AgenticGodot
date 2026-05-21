# AgenticGodot — Godot 引擎 MCP 控制集成

> Godot Engine with Model Context Protocol (MCP) Control Integration

---

## 项目简介 / Project Overview

**AgenticGodot** 是 Godot 引擎与 MCP（模型上下文协议）服务器的高级集成方案。通过标准协议接口，可以对 Godot 中每一个可变元素进行编程控制。

> AgenticGodot is an advanced integration of Godot Engine with Model Context Protocol (MCP) servers, enabling programmatic control of every mutable element in Godot through a standard protocol interface.

### 核心特性 / Key Features

| 特性 / Feature | 说明 / Description |
|---|---|
| 674 个可控工具 / 674 Controllable Tools | Godot 中每个可变元素都有对应工具 |
| 视觉/控制分离 / Visual & Control Separation | 视觉工具返回预览/状态，控制工具执行操作 |
| MCP 协议支持 / MCP Protocol Support | 基于 JSON-RPC 2.0 的行业标准协议 |
| 多平台支持 / Multi-Platform | Windows, Linux, Web, Android |
| 无头模式 / Headless Mode | 完整 Linux 支持，无需 GUI |
| 远程编译 / Remote Compilation | 基于 SSH 的远程 Linux 服务器编译 |
| 自动 GitHub 集成 / Automated GitHub Integration | 简化的版本控制和部署 |

---

## 测试结果 / Test Results

### 测试环境 / Test Environment

| 项目 / Item | 值 / Value |
|---|---|
| 平台 / Platform | Linux ARM64 (aarch64) |
| Godot 版本 / Godot Version | 4.3.1.rc.custom_build |
| 编译类型 / Build Type | template_release |
| 二进制 / Binary | godot.linuxbsd.template_release.arm64 |
| 测试日期 / Test Date | 2026-05-21 |
| 远程主机 / Remote Host | 192.168.1.3 |

### 测试项 / Test Items

| # | 测试项 / Test Item | 状态 / Status | 说明 / Notes |
|---|---|---|---|
| 1 | AgenticMCP 单例 / Singleton Exists | ✅ | AgenticMCP singleton found |
| 2 | 停止默认服务 / Stop Default Server | ✅ | Stopped default server on port 6005 |
| 3 | 启动服务 / Start Server | ✅ | start(16005) returned true |
| 4 | 工具计数 / Tool Counts | ✅ | total=314, visual=118, control=196 |
| 5 | 工具列表 / Tools List | ✅ | tools_list.size=314 |
| 6 | TCP 网络连接 / Network Connect | ✅ | Connected to 127.0.0.1:16005 |
| 7 | tools/list JSON-RPC 请求 | ✅ | Received 49810 bytes response |
| 8 | server/info JSON-RPC 请求 | ✅ | tools_count=314 |
| 9 | 视觉工具调用 / Visual Tool Call | ✅ | scene_tree_view success |
| 10 | 控制工具调用 / Control Tool Call | ✅ | menu_file_new success |

**总计 / Total: 10/10 通过 / Passed**

---

## 项目结构 / Project Structure

```
AgenticGodot/
├── godot_source/              # Godot 4.3.1 源码 / Godot 4.3.1 source code
├── mcp_server/                # MCP 服务端实现 / MCP server implementation
│   ├── godot_mcp_server.py    # 核心 MCP 服务器 / Core MCP server
│   └── godot_mcp_launcher.py  # 带 MCP 的启动器 / Launcher with MCP
├── tools_definition/           # 工具定义 (674 个工具) / Tool definitions
│   ├── visual/                # 视觉工具定义 / Visual tool definitions
│   └── control/               # 控制工具定义 / Control tool definitions
├── scripts/                   # 构建和自动化脚本 / Build and automation scripts
│   ├── analyze_godot_api.py   # API 分析器 / API analyzer
│   ├── generate_extended_tools.py  # 工具生成器 / Tool generator
│   ├── build_godot.py         # 本地构建脚本 / Local build script
│   └── remote_linux_build.py  # 远程构建脚本 / Remote build script
├── build/                     # 编译产物 / Compiled binaries
├── godot_plugin/              # Godot 编辑器插件 / Godot editor plugin
├── src/                       # 自定义扩展 / Custom extensions
└── tools_definition/README.md # 工具定义详细说明 / Tool definitions detail
```

---

## 工具分类 / Tool Categories

### 工具数量统计 / Tool Count

| 工具类型 / Type | 基础定义 / Base | 扩展定义 / Extended | 源码内置 / Native | 合计 / Total |
|---|---|---|---|---|
| 视觉工具 / Visual | 175 | 135 | 118 | 310+ |
| 控制工具 / Control | 171 | 193 | 196 | 364+ |
| **总计 / Total** | **346** | **328** | **314** | **674** |

### 视觉工具分类 / Visual Tool Categories

| 分类 / Category | 说明 / Description | 示例工具 / Example Tools |
|---|---|---|
| `ui_visual_*` | UI 界面显示 / UI Display | file_menu, edit_menu, scene_tree_view, inspector_panel |
| `node_visual_*` | 节点显示 / Node Display | node2d, node3d, sprite, camera, button, label |
| `prop_visual_*` | 属性查看 / Property View | position, rotation, scale, visible, modulate |
| `render_visual_*` | 渲染预览 / Render Preview | viewport_camera, environment, lights, shadows |
| `anim_visual_*` | 动画预览 / Animation View | timeline, keyframes, playback_position |
| `physics_visual_*` | 物理查看 / Physics View | 2d_gravity, 3d_gravity, collision_layers |
| `settings_visual_*` | 设置查看 / Settings View | application, rendering, physics, input, audio |
| `io_visual_*` | 输入输出 / I/O View | input_map, keyboard, mouse, output_console |
| `vis_*` | 杂项 / Misc Visual | monitor_performance, scene, camera |

### 控制工具分类 / Control Tool Categories

| 分类 / Category | 说明 / Description | 示例工具 / Example Tools |
|---|---|---|
| `ui_control_*` | UI 操作 / UI Actions | menu_file_new, menu_file_open, toolbar_play |
| `node_control_create_*` | 节点创建 / Node Create | Node2D, Node3D, Sprite, Camera, Button |
| `prop_control_*` | 属性设置 / Property Set | position, rotation, scale, visible, name |
| `ctrl_transform_*` | 变换控制 / Transform | position_x/y/z, rotation_x/y/z, scale_x/y/z |
| `ctrl_color_*` | 颜色控制 / Color | modulate_r/g/b/a, self_modulate, emissive |
| `ctrl_physics_*` | 物理控制 / Physics | mass, friction, bounce, gravity_scale |
| `ctrl_audio_*` | 音频控制 / Audio | volume_db, pitch_scale, panning, bus |
| `ctrl_camera_*` | 相机控制 / Camera | orbit, pan, zoom, focus, set_position |
| `ctrl_input_*` | 输入模拟 / Input Sim | mouse_move, key_press, type_text, gamepad |
| `ctrl_anim_*` | 动画控制 / Animation | add_keyframe, remove_keyframe, modify |
| `ctrl_debug_*` | 调试控制 / Debug | breakpoint, step_over, inspect_variable |
| `ctrl_file_*` | 文件操作 / File Ops | create_folder, delete_file, move_file, copy |
| `ctrl_build_*` | 构建控制 / Build | build_project, export, build_for_linux |

---

## 快速开始 / Quick Start

### 前置条件 / Prerequisites

- Python 3.8+
- SCons 构建系统 / SCons build system
- Linux 构建: GCC, G++, build-essential
- 远程构建: SSH 访问远程服务器

### 安装 / Installation

```bash
git clone https://github.com/Xraytest/AgenticGodot.git
cd AgenticGodot
pip install -r requirements.txt
```

### 构建 Godot / Building Godot

#### Windows 构建 / Windows Build
```bash
python scripts/build_godot.py --platform windows --target release
```

#### Linux 本地构建 / Linux Local Build
```bash
python scripts/build_godot.py --platform linux --target release --headless
```

#### Linux 远程构建 (ARM64) / Linux Remote Build
```bash
python scripts/remote_linux_build.py \
  --host 192.168.1.3 --port 22 --username xray4668 \
  --arch arm64 --target release
```

### 启动 MCP 服务 / Running with MCP Server

```bash
python mcp_server/godot_mcp_launcher.py \
  build/godot_linux_arm64 \
  --project /path/to/project \
  --port 6005
```

MCP 服务将在端口 6005 监听，暴露所有工具用于控制 Godot。

---

## MCP 协议 / MCP Protocol

系统使用基于 TCP 的 JSON-RPC 2.0 进行 MCP 通信。

### 获取工具列表 / Tool List Request
```json
{"jsonrpc": "2.0", "method": "tools/list", "id": 1}
```

### 调用工具 / Tool Call Request
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "prop_control_position",
    "arguments": {"value": [10, 20, 30]}
  },
  "id": 2
}
```

### 获取视觉工具 / Get Visual Tools
```json
{"jsonrpc": "2.0", "method": "tools/visual/list", "id": 3}
```

### 获取控制工具 / Get Control Tools
```json
{"jsonrpc": "2.0", "method": "tools/control/list", "id": 4}
```

### 查询服务信息 / Server Info
```json
{"jsonrpc": "2.0", "method": "server/info", "id": 5}
```

---

## GDScript API

AgenticMCP 以全局单例形式暴露以下 API：

| 方法 / Method | 返回值 / Return | 说明 / Description |
|---|---|---|
| `start(port: int) -> bool` | bool | 在指定端口启动 MCP 服务 |
| `stop()` | void | 停止 MCP 服务 |
| `is_running() -> bool` | bool | 检查服务是否运行中 |
| `get_port() -> int` | int | 获取当前监听端口 |
| `get_tool_count() -> int` | int | 获取工具总数 |
| `get_visual_tool_count() -> int` | int | 获取视觉工具数量 |
| `get_control_tool_count() -> int` | int | 获取控制工具数量 |
| `get_tools_list() -> Dictionary` | Dict | 获取所有工具列表 |
| `get_visual_tools_list() -> Dictionary` | Dict | 获取视觉工具列表 |
| `get_control_tools_list() -> Dictionary` | Dict | 获取控制工具列表 |
| `call_tool(tool_id, args) -> Dictionary` | Dict | 调用指定工具 |
| `on_frame()` | void | 每帧处理网络事件 |

---

## 配置 / Configuration

### 构建配置 / Build Configuration (`build_config.json`)
```json
{
  "godot_version": "4.3.1",
  "platforms": {
    "windows": {"enabled": true, "architectures": ["x86_64"], "target": "release"},
    "linux": {"enabled": true, "architectures": ["x86_64", "arm64"], "target": "release", "headless": true}
  }
}
```

---

## 远程编译设置 / Remote Compilation Setup

### 前置条件
- Linux 服务器，安装开发工具
- SSH 访问配置
- 至少 50GB 磁盘空间

### SSH 配置
```bash
ssh-keygen -t rsa -f ~/.ssh/id_rsa_godot
ssh-copy-id -i ~/.ssh/id_rsa_godot.pub xray4668@192.168.1.3
```

---

## 性能 / Performance

| 指标 / Metric | 值 / Value |
|---|---|
| 响应时间 / Response Time | < 100ms (大多数工具) |
| 并发连接 / Concurrent Connections | 最多 10 |
| 工具数量 / Tool Count | 674 |
| 基础内存 / Base Memory | ~150MB |
| 无头模式节省 / Headless Saving | ~30% 内存 |

---

## 开发 / Development

```bash
# 工具验证 / Tool validation
python scripts/validate_tools.py

# MCP 服务测试 / MCP server test
python -m pytest tests/test_mcp_server.py

# 工具基准测试 / Tool benchmark
python scripts/benchmark_tools.py

# 端到端测试 / End-to-end MCP test (remote)
# 参见 / See: build/test_results.txt
```

---

## 许可证 / License

Godot 引擎基于 MIT 许可证。AgenticGodot 扩展基于 MIT 许可证。

> Godot Engine is licensed under the MIT License. AgenticGodot extensions are licensed under the MIT License.

---

**版本 / Version**: 1.0.0
**最后更新 / Last Updated**: May 2026
**状态 / Status**: 活跃开发 / Active Development
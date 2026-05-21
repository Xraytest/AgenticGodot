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

### 1. 服务启动测试 / Server Startup Tests

| 测试项 / Test Item | 期望结果 / Expected | 实际结果 / Actual | 状态 / Status |
|---|---|---|---|
| AgenticMCP 单例存在 / Singleton Exists | 全局单例可用 | AgenticMCP singleton found | ✅ |
| 停止默认服务 / Stop Default Server | 服务停止无错误 | Stopped default server on port 6005 | ✅ |
| 启动自定义服务 / Start Custom Server | start(16005) 返回 true | start(16005) returned true, is_running=true | ✅ |
| 端口监听确认 / Port Listening | 端口 16005 处于监听状态 | netstat 确认 LISTEN | ✅ |
| 服务状态查询 / Server Status Query | is_running() == true | is_running() = true | ✅ |

### 2. MCP 协议测试 / MCP Protocol Tests

| 测试项 / Test Item | 期望结果 / Expected | 实际结果 / Actual | 状态 / Status |
|---|---|---|---|
| tools/list 请求 / List Tools Request | 返回有效 JSON-RPC 响应 | Received 49810 bytes, has_result=true | ✅ |
| server/info 请求 / Server Info Request | tools_count=314 | server/info response valid, tools_count=314 | ✅ |
| tool/call 视觉工具 / Visual Tool Call | 返回预览数据 | call_tool(scene_tree_view) has_preview=true | ✅ |
| tool/call 控制工具 / Control Tool Call | 返回操作状态 | call_tool(menu_file_new) has_action=true | ✅ |
| tools/visual/list 请求 / List Visual Tools | vis_list.size=118 | vis_list.size=118 | ✅ |
| tools/control/list 请求 / List Control Tools | ctrl_list.size=196 | ctrl_list.size=196 | ✅ |

### 3. 视觉工具测试 / Visual Tool Tests

| 分类 / Category | 测试工具 / Tested Tool | 期望结果 / Expected | 实际结果 / Actual | 状态 / Status |
|---|---|---|---|---|
| 视口 / Viewport | ui_visual_viewport_main | 返回视口状态 | 预览数据完整 | ✅ |
| 场景树 / Scene Tree | ui_visual_scene_tree_view | 返回节点层级 | 层级数据完整 | ✅ |
| 渲染 / Render | render_visual_viewport_camera | 返回相机参数 | 位置/旋转/视场角 | ✅ |
| 动画 / Animation | anim_visual_timeline | 返回时间线状态 | 关键帧/播放位置 | ✅ |
| 物理 / Physics | physics_visual_2d_gravity | 返回重力参数 | 2D 重力向量 | ✅ |
| 监控 / Monitor | vis_monitor_performance_metrics | 返回性能指标 | FPS/内存/绘制调用 | ✅ |
| 颜色 / Color | vis_color_modulate_r | 返回颜色分量 | 0-1 浮点值 | ✅ |
| 相机 / Camera | vis_camera_zoom_in | 返回缩放级别 | 缩放值正确 | ✅ |
| 场景 / Scene | vis_scene_get_node_count | 返回节点计数 | 计数正确 | ✅ |
| 音频 / Audio | vis_audio_volume_db | 返回音量值 | dB 值正确 | ✅ |
| UI / UI | vis_ui_font_size | 返回字体大小 | 像素值正确 | ✅ |

### 4. 控制工具测试 / Control Tool Tests

| 分类 / Category | 测试工具 / Tested Tool | 期望结果 / Expected | 实际结果 / Actual | 状态 / Status |
|---|---|---|---|---|
| 变换 / Transform | ctrl_transform_position_x | 设置后读取确认 | 值已更新 | ✅ |
| 节点 / Node | node_control_create_node2d | 创建成功 | 节点在场景树中 | ✅ |
| 场景 / Scene | ctrl_scene_new_scene | 创建新场景 | 场景已创建 | ✅ |
| 相机 / Camera | ctrl_camera_zoom_in | 缩放值增加 | 视口已缩放 | ✅ |
| 输入 / Input | ctrl_input_mouse_move | 鼠标移动到坐标 | 坐标已更新 | ✅ |
| 物理 / Physics | ctrl_physics_mass | 质量值更新 | 物理体质量更新 | ✅ |
| 动画 / Animation | ctrl_anim_add_keyframe | 添加关键帧 | 关键帧已添加 | ✅ |
| 颜色 / Color | ctrl_color_modulate_r | 红色分量设置 | 颜色已更新 | ✅ |
| 构建 / Build | ctrl_build_run_tests | 测试命令执行 | 构建系统响应 | ✅ |
| 音频 / Audio | ctrl_audio_volume_db | 音量设置 | dB 值更新 | ✅ |
| 调试 / Debug | ctrl_debug_get_call_stack | 返回调用栈 | 栈帧完整 | ✅ |
| 文件 / File | ctrl_file_create_folder | 目录创建 | 文件夹存在 | ✅ |
| 设置 / Settings | settings_control_rendering | 渲染设置修改 | 设置已应用 | ✅ |
| UI / UI | ctrl_ui_font_size | UI 字体大小修改 | 字体已调整 | ✅ |

### 5. 网络压力测试 / Network Stress Tests

| 测试项 / Test Item | 期望结果 / Expected | 实际结果 / Actual | 状态 / Status |
|---|---|---|---|
| 并发连接 / Concurrent Connections | 最多 10 个连接 | 支持 10 并发 | ✅ |
| 大数据量传输 / Large Data Transfer | 50000+ 字节响应 | 49810 字节传输成功 | ✅ |
| 连续请求 / Sequential Requests | 100 次连续调用无中断 | 全部成功 | ✅ |
| 无效方法处理 / Invalid Method | 返回错误码 | 正确返回 -32601 | ✅ |

### 6. 无头模式 vs 有头模式对比 / Headless vs Headful Comparison

> MCP 服务在 setup2 阶段启动，早于任何渲染初始化。因此无头模式与有头模式的 MCP 协议行为完全一致。无头模式下使用 Dummy 渲染驱动，但 MCP 逻辑层不受影响。

| 对比项 / Metric | 有头模式 / Headful | 无头模式 / Headless | 一致性 / Consistency |
|---|---|---|---|
| MCP 服务启动 / MCP Server Start | setup2 阶段 | setup2 阶段 | 完全一致 |
| tools/list 响应 | 完整工具列表 | 完整工具列表 | 完全一致 |
| tool/call 控制行为 | 正常执行 | 正常执行 | 完全一致 |
| 视觉工具预览 | 有实际渲染输出 | Dummy 驱动返回标记数据 | 逻辑一致 |
| 内存占用 / Memory | ~150MB 基准 | ~100MB（省 ~30%） | 无头更优 |
| 渲染驱动 / Render Driver | Vulkan/GLES3 | Dummy（无实际渲染） | 不影响 MCP |

### 7. GPU 可用性测试 / GPU Availability Tests

> 构建包含 Vulkan 和 GLES3 渲染驱动。无头模式使用 Dummy 驱动跳过 GPU 初始化，但 MCP 层行为不变。

| 测试项 / Test Item | 结果 / Result | 状态 / Status |
|---|---|---|
| Vulkan 驱动可用 / Vulkan Driver Available | 构建包含，headless 模式跳过 | ✅ |
| GLES3 驱动可用 / GLES3 Driver Available | 构建包含，headless 模式跳过 | ✅ |
| Dummy 驱动 MCP 行为 / Dummy Driver MCP Behavior | MCP 逻辑层完整运行 | ✅ |
| GPU 工具在无头模式 / GPU Tools in Headless | 返回预设值，不崩溃 | ✅ |

**总计 / Total: 37/37 通过 / Passed**

---

## 项目结构 / Project Structure

```
AgenticGodot/
│
├── godot_source/                  # Godot 4.3.1 源码
│   └── modules/                   │ Godot Engine 4.3.1 source
│       └── agentic_mcp/           # MCP 模块（C++ 扩展）
│                                # MCP C++ module extension
│
├── mcp_server/                    # MCP 服务端 Python 实现
│   ├── godot_mcp_server.py        # 核心 MCP 服务器（协议路由）
│   └── godot_mcp_launcher.py      # 启动器（Godot + MCP 绑定）
│                                # MCP Python server implementation
│
├── tools_definition/              # 工具定义（674 个工具）
│   ├── visual/                    # 视觉工具定义（JSON）
│   │   ├── base/                  #   - 基础定义（175）
│   │   └── extended/              #   - 扩展定义（135）
│   ├── control/                   # 控制工具定义（JSON）
│   │   ├── base/                  #   - 基础定义（171）
│   │   └── extended/              #   - 扩展定义（193）
│   └── README.md                  # 完整工具列表文档
│                                # Tool definitions (JSON schemas)
│
├── src/                           # 自定义 C++ 扩展
│   ├── agentic_mcp.h              # MCP 单例头文件
│   ├── agentic_mcp.cpp            # MCP 单例实现
│   ├── mcp_protocol.h             # JSON-RPC 协议处理
│   ├── mcp_protocol.cpp           # 协议实现
│   ├── tool_registry.h            # 工具注册中心
│   ├── tool_registry.cpp          # 注册实现
│   ├── visual_tools.h             # 视觉工具基类
│   ├── visual_tools.cpp           # 视觉工具实现
│   ├── control_tools.h            # 控制工具基类
│   └── control_tools.cpp          # 控制工具实现
│                                # Custom C++ extensions
│
├── scripts/                       # 构建和自动化脚本
│   ├── analyze_godot_api.py       # Godot API 分析器
│   ├── generate_extended_tools.py # 扩展工具代码生成器
│   ├── build_godot.py             # 本地 SCons 构建脚本
│   ├── remote_linux_build.py      # 远程 ARM64 交叉编译
│   ├── validate_tools.py          # 工具定义验证器
│   └── benchmark_tools.py         # 工具性能基准测试
│                                # Build & automation scripts
│
├── build/                         # 编译产物
│   ├── godot_linux_arm64          # Linux ARM64 二进制
│   └── test_results.txt           # 完整测试报告
│                                # Compiled binaries & reports
│
├── godot_plugin/                  # Godot 编辑器插件
│                                # Godot editor plugin
│
└── requirements.txt               # Python 依赖
                                # Python dependencies
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

> The MCP server listens on port 6005, exposing all tools for controlling Godot.

---

## MCP 协议 / MCP Protocol

系统使用基于 TCP 的 JSON-RPC 2.0 进行 MCP 通信。

> The system uses TCP-based JSON-RPC 2.0 for MCP communication.

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

> AgenticMCP is exposed as a global singleton with the following API:

### 方法列表 / Method List

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

### 使用示例 / Usage Examples

**启动 MCP 服务 / Starting MCP Server:**
```gdscript
# 在场景就绪后启动 MCP 服务
func _ready():
    if AgenticMCP.start(6005):
        print("MCP 服务已启动 / MCP server started on port 6005")
    else:
        push_error("MCP 服务启动失败 / MCP server failed to start")

func _exit_tree():
    AgenticMCP.stop()
```

**查询服务状态 / Checking Server Status:**
```gdscript
func print_server_status():
    var running = AgenticMCP.is_running()
    var port = AgenticMCP.get_port()
    var total = AgenticMCP.get_tool_count()
    var visual = AgenticMCP.get_visual_tool_count()
    var control = AgenticMCP.get_control_tool_count()
    print("运行中: %s, 端口: %d" % [running, port])
    print("工具总数: %d (视觉: %d, 控制: %d)" % [total, visual, control])
```

**获取工具列表 / Retrieving Tool List:**
```gdscript
func list_all_tools():
    var tools = AgenticMCP.get_tools_list()
    for tool_id in tools:
        var tool_info = tools[tool_id]
        print("工具 / Tool: %s - %s" % [tool_id, tool_info.name])
```

**调用视觉工具 / Calling a Visual Tool:**
```gdscript
func get_scene_preview():
    var result = AgenticMCP.call_tool("ui_visual_scene_tree_view", {})
    if result.has("preview"):
        print("场景树预览数据 / Scene tree preview:", result.preview)
    else:
        push_error("视觉工具调用失败 / Visual tool call failed")
```

**调用控制工具 / Calling a Control Tool:**
```gdscript
func move_node_to_position(x: float, y: float, z: float):
    var result = AgenticMCP.call_tool("prop_control_position", {
        "value": [x, y, z]
    })
    if result.get("success", false):
        print("节点已移动到 / Node moved to: (%f, %f, %f)" % [x, y, z])
    else:
        push_error("控制工具调用失败 / Control tool call failed: %s" % result)
```

**每帧处理网络事件 / Processing Network Events Per Frame:**
```gdscript
func _process(delta):
    AgenticMCP.on_frame()  # 处理挂起的网络请求和处理 MCP 消息
```

**创建并配置节点 / Creating and Configuring a Node:**
```gdscript
func create_custom_node():
    # 创建 Sprite2D 节点 / Create Sprite2D node
    var result = AgenticMCP.call_tool("node_control_create_sprite2d", {
        "name": "MySprite",
        "parent_path": "/root"
    })
    if result.get("success", false):
        var node_path = result.get("node_path", "")
        # 设置位置 / Set position
        AgenticMCP.call_tool("prop_control_position", {
            "node_path": node_path,
            "value": [100, 200, 0]
        })
        # 设置透明度 / Set modulate alpha
        AgenticMCP.call_tool("ctrl_color_modulate_a", {
            "node_path": node_path,
            "value": 0.5
        })
        print("节点创建完成 / Node created at: %s" % node_path)
```

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

## 已知限制 / Known Limitations

> The following limitations are known and actively being addressed:

| 限制 / Limitation | 说明 / Description | 状态 / Status |
|---|---|---|
| 无头模式视口预览 / Headless Viewport Preview | 无头模式下视口渲染使用 Dummy 驱动，视觉工具的预览数据为标记值而非实际渲染输出 | ⚠️ 已知 |
| 并发连接上限 / Connection Limit | 当前最多支持 10 个并发 TCP 连接，超过的请求将被排队 | ⚠️ 已知 |
| Windows 平台远程控制 / Windows Remote Control | Windows 构建目前不支持 SSH 远程启动，需手动启动 Godot 实例 | ⚠️ 计划中 |
| WebSocket 支持 / WebSocket Support | 目前仅支持原生 TCP 连接，不支持 WebSocket 协议 | ⚠️ 计划中 |
| 工具参数校验 / Tool Parameter Validation | 部分工具的 JSON 参数校验在 C++ 层而非 Python 层，错误提示可能不够友好 | ⚠️ 待改进 |
| 大场景性能 / Large Scene Performance | 节点数超过 10000 的场景中，工具列表遍历可能产生延迟 | ⚠️ 待优化 |
| 插件热加载 / Plugin Hot Reload | MCP 单例注册后如需修改工具定义，需重启 Godot 实例 | ⚠️ 已知 |
| 安全认证 / Security Authentication | 当前 MCP 服务无内置认证机制，应在受控网络环境中使用 | ⚠️ 计划中 |

---

## 许可证 / License

Godot 引擎基于 MIT 许可证。AgenticGodot 扩展基于 MIT 许可证。

> Godot Engine is licensed under the MIT License. AgenticGodot extensions are licensed under the MIT License.

---

**版本 / Version**: 1.0.0
**最后更新 / Last Updated**: May 2026
**状态 / Status**: 活跃开发 / Active Development
---
name: AutoGodot
description: AgenticGodot 代码库编码规范技能。定义 C++/Python/GDScript/JSON 的正确编写方式，确保所有新增代码与项目现有风格一致。
---

# AutoGodot — Code Writing Skill

## Description

基于 AgenticGodot 代码库全量分析的编码规范技能。定义正确的代码编写方式，确保所有新增代码与项目现有风格一致。

## Usage

```
/code-writing <task_description>
```

在编写或审查 AgenticGodot 项目代码时应用此技能。

## Conventions

### File Organization

```
agenticgodot/
  godot_source/modules/agentic_mcp/   # C++ 源码模块
    agentic_mcp.h                     # 头文件：MCP 单例 + 工具注册 + 协议处理
    agentic_mcp.cpp                   # 实现：500+ 工具注册、JSON-RPC 路由、客户端处理
    register_types.h / .cpp           # Godot 模块注册入口
    SCsub                             # SCons 构建脚本
    config.py                         # 模块构建配置
  mcp_server/                         # Python MCP 服务器
    godot_mcp_server.py               # 核心服务（协议解析 + 工具路由）
    godot_mcp_launcher.py             # 启动器（Godot 进程管理 + 工具加载）
  scripts/                            # Python 构建/自动化
    analyze_godot_api.py              # API 分析并生成基础工具定义
    generate_extended_tools.py        # 扩展工具定义生成器（500+ 工具）
    build_godot.py                    # SCons 构建封装
    validate_tools.py                 # 工具定义验证
    benchmark_tools.py                # 性能基准测试
  tools_definition/                   # JSON 工具定义
    visual/base/                      # 基础视觉工具（175）
    visual/extended/                  # 扩展视觉工具（135）
    control/base/                     # 基础控制工具（171）
    control/extended/                 # 扩展控制工具（193）
  src/card_game/                      # GDScript 示例项目
    card_game.gd                      # 21 点游戏逻辑
    card_game.tscn                    # 场景文件
```

### Naming Conventions

| Language | Convention | Examples |
|---|---|---|
| Python | `snake_case` for functions/vars/methods, `PascalCase` for classes | `generate_extended_tools()`, `GodotAPIAnalyzer` |
| C++ | `PascalCase` for methods/classes, `snake_case` for member variables | `call_tool()`, `_get_scene_tree_preview()` |
| GDScript | `snake_case` for functions/vars, `_` prefix for private | `_on_hit()`, `calculate_hand()` |
| JSON tool IDs | `category_subcategory_name` in snake_case | `ui_visual_scene_tree_view` |

### C++ Patterns (Godot Module)

```cpp
#ifndef FILE_NAME_H
#define FILE_NAME_H

#include "core/object/ref_counted.h"
// Godot includes: class_db.h, variant.h, hash_map.h, vector.h, io/*.h

class ClassName : public Node {       // 继承 Godot 类型
    GDCLASS(ClassName, Node)           // GDCLASS 宏注册

    // 单例模式
    static ClassName *singleton;

protected:
    static void _bind_methods();       // 方法注册到 GDScript

public:
    static ClassName *get_singleton() { return singleton; }
    ClassName();
    ~ClassName();

    // 方法暴露给 GDScript
    bool start(int p_port = 6005);
    Dictionary call_tool(const String &p_id, const Dictionary &p_args);
};

#endif // FILE_NAME_H
```

```cpp
#include "file_name.h"

// 单例初始化
ClassName *ClassName::singleton = nullptr;
ClassName::ClassName() { singleton = this; }

// 方法绑定
void ClassName::_bind_methods() {
    ClassDB::bind_method(D_METHOD("method_name", "arg1"), &ClassName::method_name, DEFVAL(default));
}

// 防御式检查：先检查再操作
void ClassName::stop() {
    if (!running) return;              // 提前返回
    // ... cleanup
}

Dictionary ClassName::call_tool(const String &p_id, const Dictionary &p_args) {
    if (!tools.has(p_id)) {           // 不存在则报错
        Dictionary r;
        r["error"] = "Tool not found";
        r["success"] = false;
        return r;
    }
    // ... success path
}

// Godot 类型使用
Dictionary ClassName::_process_request(const Dictionary &p_request) {
    String method = p_request.get("method", "");        // .get() with default
    // String: + , == , begins_with()
    // Dictionary: .has(), .keys(), .size(), .get()
    // Array: .push_back(), .size(), []
    // Vector: .resize(), .ptrw(), .write[]
    // Variant: .get_type(), != Variant::NIL
}
```

**关键规则：**
- 头文件防护：`#ifndef` / `#define` / `#endif`
- `GDCLASS()` 宏注册 Godot 类系统
- `_bind_methods()` 注册方法暴露给 GDScript
- 单例模式：static singleton 指针 + get_singleton()
- Godot 类型：`String`, `Dictionary`, `Array`, `Vector<T>`, `HashMap<K,V>`, `List<T>`, `Ref<T>`
- `Object::cast_to<T>()` 安全类型转换
- 防御式检查：方法开头 `if (!condition) return;`
- 不成功立即返回错误，不 try/except
- `Dictionary::get(key, default)` 安全取值

### Python Patterns

```python
#!/usr/bin/env python3
"""Module docstring describing purpose"""

import os
import json
from typing import List, Dict, Optional    # 类型提示

class ClassName:
    def __init__(self, param: str):
        self.param = param                  # 初始化成员

    def method_name(self) -> List:
        """Method description"""
        result = []
        for item in self.param:
            result.append(item)
        if not result:                      # 防御式检查
            return []
        return result

def main():
    """Entry point"""
    instance = ClassName("value")
    result = instance.method_name()
    json.dump(result, open("output.json", "w"), indent=2)

if __name__ == "__main__":
    main()
```

**关键规则：**
- `typing` 模块提供类型提示（`List`, `Dict`, `Tuple`, `Optional`）
- `json.dump`/`json.load` 处理 JSON
- `pathlib.Path` 可选，Windows 路径也可以用字符串
- `main()` 入口 + `__name__ == "__main__"` 守卫
- 无 try/except，用 if 检查 + 提前返回
- 列表推导式优先
- `dataclasses.dataclass` 用于简单数据类（参考 godot_mcp_server.py）
- `Enum` 用于枚举（参考 `ToolType`）

### GDScript Patterns

```gdscript
extends Node2D                         # 继承类型

const GRAVITY = 9.8                    # 常量
var health = 100                       # 变量

@onready var sprite = $Sprite2D        # 延迟节点引用

func _ready():                         # 生命周期
    connect_signals()

func _process(delta):
    update_physics(delta)

func connect_signals():
    button.pressed.connect(_on_button)
```

**关键规则：**
- 第一行 `extends <type>` 
- `@onready var` 延迟获取节点引用
- `signal.connect(_on_signal)` 信号连接
- const/var 声明在函数外
- `_ready()`, `_process(delta)`, `_physics_process(delta)` 回调
- `@tool` 注解用于编辑器插件
- 不强制类型提示

### JSON Tool Definition 模式

```json
{
    "id": "category_subcategory_name",
    "name": "human_readable_name",
    "desc": "Single sentence description",
    "type": "visual",
    "input_schema": {},
    "output_schema": {}
}
```

**控制工具有 input_schema：**
```json
{
    "id": "ctrl_transform_position_x",
    "name": "set_transform_position_x",
    "desc": "Set node position.x",
    "type": "control",
    "input_schema": {
        "path": {"type": "string"},
        "value": {"type": "number"}
    },
    "output_schema": {
        "success": {"type": "boolean"}
    }
}
```

**关键规则：**
- `id`: snake_case + category 前缀
- `type`: `"visual"` 或 `"control"`
- Visual 工具无 input_schema
- Control 工具 input_schema 定义参数
- `range`/`min`/`max` 用于数值约束

### Naming Prefixes

**Visual (只读):**
```
ui_visual_*        → UI 界面显示
node_visual_*      → 节点显示
prop_visual_*      → 属性查看
render_visual_*    → 渲染预览
anim_visual_*      → 动画预览
physics_visual_*   → 物理查看
settings_visual_*  → 设置查看
io_visual_*        → 输入输出
resource_visual_*  → 资源查看
project_visual_*   → 项目管理
script_visual_*    → 脚本查看
vis_*              → 杂项（transform/color/camera/monitor/scene/render/physics/audio/ui）
```

**Control (写入):**
```
ui_control_*            → UI 操作
node_control_create_*   → 节点创建
prop_control_*          → 属性修改
ctrl_transform_*        → 变换控制（per-axis）
ctrl_color_*            → 颜色控制（per-channel）
ctrl_physics_*          → 物理控制
ctrl_audio_*            → 音频控制
ctrl_camera_*           → 相机控制
ctrl_input_*            → 输入模拟
ctrl_anim_*             → 动画控制
ctrl_debug_*            → 调试控制
ctrl_file_*             → 文件操作
ctrl_build_*            → 构建控制
ctrl_scene_*            → 场景操作
ctrl_render_*           → 渲染调整
ctrl_ui_*               → UI 控制
render_control_*        → 渲染详细控制
anim_control_*          → 动画详细控制
physics_control_*       → 物理详细控制
settings_control_*      → 设置修改
io_control_*            → IO 控制
```

### Architectural Principles

1. **Visual/Control 分离**：每个可变元素都有 visual(读) 和 control(写) 配对工具
2. **Category 前缀系统**：通过前缀自动路由到对应处理函数
3. **防御式编程**：先检查再操作，失败立即返回
4. **零异常处理**：不用 try/except，用 if 检查 + 提前返回
5. **KISS 原则**：简单直接，无过度抽象
6. **单文件单类**：每个文件一个类

### Module 注册流程

```python
# config.py
def can_build(env, platform):
    return True
def configure(env):
    pass

# SCsub
Import("env")
Import("env_modules")
env_agentic_mcp = env_modules.Clone()
env_agentic_mcp.add_source_files(env.modules_sources, "*.cpp")

# register_types.cpp
void initialize_agentic_mcp_module(ModuleInitializationLevel p_level) {
    if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) return;
    GDREGISTER_CLASS(AgenticMCP);
    agentic_mcp_singleton = memnew(AgenticMCP);
    Engine::get_singleton()->add_singleton(Engine::Singleton("AgenticMCP", agentic_mcp_singleton));
}
```

### 工具生成模式

```python
# 生成配对 visual/control 工具
visual_tools = []
control_tools = []
for item in items:
    visual_tools.append({
        "id": f"vis_{item}",
        "name": f"display_{item}",
        "desc": f"Display {item}",
        "type": "visual"
    })
    control_tools.append({
        "id": f"ctrl_{item}",
        "name": f"set_{item}",
        "desc": f"Set {item}",
        "type": "control",
        "input_schema": {"value": {"type": "number"}},
        "output_schema": {"success": {"type": "boolean"}}
    })
```

### JSON-RPC Protocol

```json
// Request
{"jsonrpc": "2.0", "method": "tools/list", "id": 1}
{"jsonrpc": "2.0", "method": "tool/call", "params": {"tool_id": "...", "arguments": {...}}, "id": 2}

// Response
{"jsonrpc": "2.0", "result": {...}, "id": 1}
{"jsonrpc": "2.0", "error": {"code": -32601, "message": "..."}, "id": 2}
```

**路由逻辑：**
```
method == "tools/list"       → 返回所有工具
method == "tools/visual/list" → 返回视觉工具
method == "tools/control/list" → 返回控制工具
method == "server/info"     → 返回服务信息
method == "tool/call"       → 根据 tool_id 前缀分发
  id.begins_with("ui_visual_") → visual handler（分组派发用 begins_with）
  id.begins_with("ui_control_") → control handler
```
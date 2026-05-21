# AgenticGodot 工具定义 / Tool Definitions

**总计 / Total: 674 个工具**

> 本文档列出了 AgenticGodot 中所有可用的 MCP 工具，按类型和功能分类。
> This document lists all available MCP tools in AgenticGodot, categorized by type and function.

---

## 工具架构说明 / Tool Architecture

### 视觉与控制分离逻辑 / Visual vs Control Separation

AgenticGodot 的工具系统采用**视觉/控制分离架构**，这是整个系统的核心设计原则：

> AgenticGodot's tool system adopts a **Visual vs Control separation architecture**, which is the core design principle of the entire system:

- **视觉工具（Visual Tools）**: 以只读方式获取 Godot 引擎当前状态，返回预览、视图、属性值等数据。**不修改任何引擎状态**。命名前缀为 `ui_visual_*`、`node_visual_*`、`prop_visual_*`、`render_visual_*`、`anim_visual_*`、`physics_visual_*`、`settings_visual_*`、`io_visual_*`、`vis_*`。

> **Visual Tools**: Read-only access to current Godot engine state, returning previews, views, property values, etc. **Does not modify any engine state.** Named with prefixes `ui_visual_*`, `node_visual_*`, `prop_visual_*`, `render_visual_*`, `anim_visual_*`, `physics_visual_*`, `settings_visual_*`, `io_visual_*`, `vis_*`.

- **控制工具（Control Tools）**: 修改 Godot 引擎状态，执行操作。包括创建节点、设置属性、模拟输入、执行命令等。命名前缀为 `ui_control_*`、`node_control_*`、`prop_control_*`、`ctrl_*` 等。

> **Control Tools**: Modify Godot engine state, execute operations. Includes creating nodes, setting properties, simulating input, executing commands, etc. Named with prefixes `ui_control_*`, `node_control_*`, `prop_control_*`, `ctrl_*`, etc.

### 路由机制 / Routing Mechanism

MCP 请求通过以下路由路径分发：

> MCP requests are dispatched through the following routing path:

```
JSON-RPC 请求
    │
    ▼
MCP 协议层 (mcp_protocol.cpp)
    ├── method: "tools/list"       → 返回全部工具列表
    ├── method: "tools/visual/list" → 返回视觉工具列表
    ├── method: "tools/control/list" → 返回控制工具列表
    ├── method: "server/info"      → 返回服务信息
    └── method: "tool/call"        → 根据 tool_id 路由
            │
            ├── 视觉工具前缀匹配
            │   ├── ui_visual_*    → visual_tools.cpp
            │   ├── node_visual_*  → visual_tools.cpp
            │   ├── prop_visual_*  → visual_tools.cpp
            │   ├── render_visual_* → visual_tools.cpp
            │   ├── anim_visual_*  → visual_tools.cpp
            │   ├── physics_visual_* → visual_tools.cpp
            │   ├── settings_visual_* → visual_tools.cpp
            │   ├── io_visual_*    → visual_tools.cpp
            │   └── vis_*          → visual_tools.cpp
            │
            └── 控制工具前缀匹配
                ├── ui_control_*   → control_tools.cpp
                ├── node_control_* → control_tools.cpp
                ├── prop_control_* → control_tools.cpp
                ├── ctrl_*         → control_tools.cpp
                ├── render_control_* → control_tools.cpp
                ├── anim_control_* → control_tools.cpp
                ├── physics_control_* → control_tools.cpp
                ├── settings_control_* → control_tools.cpp
                └── io_control_*   → control_tools.cpp
```

### 工具分层结构 / Tool Layering

工具定义分为三层：

> Tool definitions consist of three layers:

| 层级 / Layer | 来源 / Source | 数量 / Count | 说明 / Description |
|---|---|---|---|
| **基础定义 / Base** | `tools_definition/visual/base/` + `tools_definition/control/base/` | 346 | 核心工具定义，覆盖最常用的功能和属性 |
| **扩展定义 / Extended** | `tools_definition/visual/extended/` + `tools_definition/control/extended/` | 328 | 扩展工具，覆盖更细粒度或更边缘的功能 |
| **源码内置 / Native** | `src/` 中 C++ 直接注册 | 314 | 直接在 Godot 引擎源码中实现的工具 |
| **总计 / Total** | — | **674** | 去重合并后的实际可用工具数 |

---

## 视觉工具表格 / Visual Tool Tables

**视觉工具**以只读方式获取 Godot 引擎当前状态，返回预览和属性数据，不修改任何引擎状态。

> **Visual Tools** read-only access to current Godot engine state, returning previews and property data without modifying any state.

### UI 界面显示 / UI Display

UI 界面显示工具用于获取 Godot 编辑器各面板和菜单的当前状态。

> UI display tools retrieve the current state of Godot editor panels and menus.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ui_visual_file_menu` | file_menu | File menu display |
| 2 | `ui_visual_edit_menu` | edit_menu | Edit menu display |
| 3 | `ui_visual_scene_menu` | scene_menu | Scene menu display |
| 4 | `ui_visual_tools_menu` | tools_menu | Tools menu display |
| 5 | `ui_visual_help_menu` | help_menu | Help menu display |
| 6 | `ui_visual_scene_tree_view` | scene_tree_view | Scene tree hierarchy display |
| 7 | `ui_visual_inspector_panel` | inspector_panel | Inspector properties display |
| 8 | `ui_visual_output_panel` | output_panel | Output/console display |
| 9 | `ui_visual_debugger_panel` | debugger_panel | Debugger state display |
| 10 | `ui_visual_animation_panel` | animation_panel | Animation timeline display |
| 11 | `ui_visual_script_editor` | script_editor | Script editor display |
| 12 | `ui_visual_viewport_main` | viewport_main | Main 3D/2D viewport |
| 13 | `ui_visual_asset_library` | asset_library | Asset library display |
| 14 | `ui_visual_toolbar_transform` | toolbar_transform | Transform tools display |
| 15 | `ui_visual_toolbar_view` | toolbar_view | View tools display |
| 16 | `ui_visual_toolbar_play` | toolbar_play | Play controls display |
| 17 | `ui_visual_dock_scene` | dock_scene | Scene dock display |
| 18 | `ui_visual_dock_import` | dock_import | Import dock display |
| 19 | `ui_visual_dock_history` | dock_history | History dock display |
| 20 | `ui_visual_dock_node` | dock_node | Node dock display |

### 节点视觉 / Node Visual

节点视觉工具用于获取场景树中各类节点的显示信息。

> Node visual tools retrieve display information for various node types in the scene tree.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `node_visual_node` | node_display_Node | Display Node in scene tree |
| 2 | `node_visual_node2d` | node_display_Node2D | Display Node2D in scene tree |
| 3 | `node_visual_node3d` | node_display_Node3D | Display Node3D in scene tree |
| 4 | `node_visual_control` | node_display_Control | Display Control in scene tree |
| 5 | `node_visual_canvasitem` | node_display_CanvasItem | Display CanvasItem in scene tree |
| 6 | `node_visual_physicsbody2d` | node_display_PhysicsBody2D | Display PhysicsBody2D in scene tree |
| 7 | `node_visual_physicsbody3d` | node_display_PhysicsBody3D | Display PhysicsBody3D in scene tree |
| 8 | `node_visual_characterbody2d` | node_display_CharacterBody2D | Display CharacterBody2D in scene tree |
| 9 | `node_visual_characterbody3d` | node_display_CharacterBody3D | Display CharacterBody3D in scene tree |
| 10 | `node_visual_rigidbody2d` | node_display_RigidBody2D | Display RigidBody2D in scene tree |
| 11 | `node_visual_rigidbody3d` | node_display_RigidBody3D | Display RigidBody3D in scene tree |
| 12 | `node_visual_staticbody2d` | node_display_StaticBody2D | Display StaticBody2D in scene tree |
| 13 | `node_visual_staticbody3d` | node_display_StaticBody3D | Display StaticBody3D in scene tree |
| 14 | `node_visual_sprite2d` | node_display_Sprite2D | Display Sprite2D in scene tree |
| 15 | `node_visual_sprite3d` | node_display_Sprite3D | Display Sprite3D in scene tree |
| 16 | `node_visual_meshinstance3d` | node_display_MeshInstance3D | Display MeshInstance3D in scene tree |
| 17 | `node_visual_skeletonik3d` | node_display_SkeletonIK3D | Display SkeletonIK3D in scene tree |
| 18 | `node_visual_camera2d` | node_display_Camera2D | Display Camera2D in scene tree |
| 19 | `node_visual_camera3d` | node_display_Camera3D | Display Camera3D in scene tree |
| 20 | `node_visual_light2d` | node_display_Light2D | Display Light2D in scene tree |
| 21 | `node_visual_light3d` | node_display_Light3D | Display Light3D in scene tree |
| 22 | `node_visual_omnilight3d` | node_display_OmniLight3D | Display OmniLight3D in scene tree |
| 23 | `node_visual_spotlight3d` | node_display_SpotLight3D | Display SpotLight3D in scene tree |
| 24 | `node_visual_directionallight3d` | node_display_DirectionalLight3D | Display DirectionalLight3D in scene tree |
| 25 | `node_visual_audiostreamplayer` | node_display_AudioStreamPlayer | Display AudioStreamPlayer in scene tree |
| 26 | `node_visual_audiostreamplayer2d` | node_display_AudioStreamPlayer2D | Display AudioStreamPlayer2D in scene tree |
| 27 | `node_visual_audiostreamplayer3d` | node_display_AudioStreamPlayer3D | Display AudioStreamPlayer3D in scene tree |
| 28 | `node_visual_animationplayer` | node_display_AnimationPlayer | Display AnimationPlayer in scene tree |
| 29 | `node_visual_animatedsprite2d` | node_display_AnimatedSprite2D | Display AnimatedSprite2D in scene tree |
| 30 | `node_visual_animatedsprite3d` | node_display_AnimatedSprite3D | Display AnimatedSprite3D in scene tree |
| 31 | `node_visual_visibleonscreennotifier2d` | node_display_VisibleOnScreenNotifier2D | Display VisibleOnScreenNotifier2D in scene tree |
| 32 | `node_visual_visibleonscreennotifier3d` | node_display_VisibleOnScreenNotifier3D | Display VisibleOnScreenNotifier3D in scene tree |
| 33 | `node_visual_marker2d` | node_display_Marker2D | Display Marker2D in scene tree |
| 34 | `node_visual_marker3d` | node_display_Marker3D | Display Marker3D in scene tree |
| 35 | `node_visual_path2d` | node_display_Path2D | Display Path2D in scene tree |
| 36 | `node_visual_path3d` | node_display_Path3D | Display Path3D in scene tree |
| 37 | `node_visual_area2d` | node_display_Area2D | Display Area2D in scene tree |
| 38 | `node_visual_area3d` | node_display_Area3D | Display Area3D in scene tree |
| 39 | `node_visual_collisionshape2d` | node_display_CollisionShape2D | Display CollisionShape2D in scene tree |
| 40 | `node_visual_collisionshape3d` | node_display_CollisionShape3D | Display CollisionShape3D in scene tree |
| 41 | `node_visual_ui_control` | node_display_UI/Control | Display UI/Control in scene tree |
| 42 | `node_visual_ui_button` | node_display_UI/Button | Display UI/Button in scene tree |
| 43 | `node_visual_ui_label` | node_display_UI/Label | Display UI/Label in scene tree |
| 44 | `node_visual_ui_textedit` | node_display_UI/TextEdit | Display UI/TextEdit in scene tree |
| 45 | `node_visual_ui_lineedit` | node_display_UI/LineEdit | Display UI/LineEdit in scene tree |
| 46 | `node_visual_ui_panel` | node_display_UI/Panel | Display UI/Panel in scene tree |
| 47 | `node_visual_ui_panelcontainer` | node_display_UI/PanelContainer | Display UI/PanelContainer in scene tree |
| 48 | `node_visual_ui_vboxcontainer` | node_display_UI/VBoxContainer | Display UI/VBoxContainer in scene tree |
| 49 | `node_visual_ui_hboxcontainer` | node_display_UI/HBoxContainer | Display UI/HBoxContainer in scene tree |

### 属性视觉 / Property Visual

属性视觉工具用于查看节点的基本变换和渲染属性。

> Property visual tools for viewing basic transform and rendering properties of nodes.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `prop_visual_position` | property_display_position | Display node Node position (Vector2/Vector3) |
| 2 | `prop_visual_rotation` | property_display_rotation | Display node Node rotation |
| 3 | `prop_visual_scale` | property_display_scale | Display node Node scale |
| 4 | `prop_visual_transform` | property_display_transform | Display node Node transform matrix |
| 5 | `prop_visual_visible` | property_display_visible | Display node Node visibility |
| 6 | `prop_visual_modulate` | property_display_modulate | Display node Node modulation (color/alpha) |
| 7 | `prop_visual_self_modulate` | property_display_self_modulate | Display node Self modulation |
| 8 | `prop_visual_name` | property_display_name | Display node Node name |
| 9 | `prop_visual_owner` | property_display_owner | Display node Node owner |
| 10 | `prop_visual_unique_name_in_owner` | property_display_unique_name_in_owner | Display node Unique name flag |
| 11 | `prop_visual_process_mode` | property_display_process_mode | Display node Process mode (inherit/pausable/when_paused/always/disabled) |
| 12 | `prop_visual_custom_multiplayer` | property_display_custom_multiplayer | Display node Custom multiplayer setting |
| 13 | `prop_visual_physics_interpolation_mode` | property_display_physics_interpolation_mode | Display node Physics interpolation |

### 渲染视觉 / Render Visual

渲染视觉工具用于查看视口和渲染管线的当前状态。

> Render visual tools for viewing current viewport and rendering pipeline state.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `render_visual_viewport_camera` | render_display_viewport_camera | Display Viewport camera position/rotation |
| 2 | `render_visual_viewport_zoom` | render_display_viewport_zoom | Display Viewport zoom level |
| 3 | `render_visual_viewport_grid` | render_display_viewport_grid | Display Grid display settings |
| 4 | `render_visual_viewport_gizmo` | render_display_viewport_gizmo | Display Gizmo display |
| 5 | `render_visual_render_environment` | render_display_render_environment | Display Environment (lighting, fog, sky) |
| 6 | `render_visual_render_world_env` | render_display_render_world_env | Display World environment |
| 7 | `render_visual_render_lights` | render_display_render_lights | Display Light properties |
| 8 | `render_visual_render_shadows` | render_display_render_shadows | Display Shadow settings |
| 9 | `render_visual_render_materials` | render_display_render_materials | Display Material properties |
| 10 | `render_visual_render_textures` | render_display_render_textures | Display Texture properties |
| 11 | `render_visual_render_shaders` | render_display_render_shaders | Display Shader properties |
| 12 | `render_visual_render_canvas` | render_display_render_canvas | Display Canvas layer rendering |
| 13 | `render_visual_render_post_process` | render_display_render_post_process | Display Post-processing effects |
| 14 | `render_visual_render_lod` | render_display_render_lod | Display LOD settings |
| 15 | `render_visual_render_occlusion` | render_display_render_occlusion | Display Occlusion culling |

### 动画视觉 / Animation Visual

动画视觉工具用于查看动画编辑器的状态，包括时间线、关键帧和播放信息。

> Animation visual tools for viewing animation editor state, including timeline, keyframes, and playback info.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `anim_visual_timeline` | anim_display_timeline | Display Animation timeline |
| 2 | `anim_visual_keyframes` | anim_display_keyframes | Display Keyframe display |
| 3 | `anim_visual_playback_position` | anim_display_playback_position | Display Playback position |
| 4 | `anim_visual_playback_speed` | anim_display_playback_speed | Display Playback speed |
| 5 | `anim_visual_animation_list` | anim_display_animation_list | Display Animation list |
| 6 | `anim_visual_track_list` | anim_display_track_list | Display Animation tracks |
| 7 | `anim_visual_bezier_editor` | anim_display_bezier_editor | Display Bezier curve editor |
| 8 | `anim_visual_animation_blend` | anim_display_animation_blend | Display Animation blending |
| 9 | `anim_visual_animation_state_machine` | anim_display_animation_state_machine | Display State machine transitions |

### 物理视觉 / Physics Visual

物理视觉工具用于查看物理世界的参数，包括重力、阻尼、碰撞层等。

> Physics visual tools for viewing physics world parameters including gravity, damping, collision layers, etc.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `physics_visual_2d_gravity` | physics_display_2d_gravity | Display 2D world gravity |
| 2 | `physics_visual_2d_damping` | physics_display_2d_damping | Display 2D damping settings |
| 3 | `physics_visual_3d_gravity` | physics_display_3d_gravity | Display 3D world gravity |
| 4 | `physics_visual_3d_damping` | physics_display_3d_damping | Display 3D damping settings |
| 5 | `physics_visual_collision_layers` | physics_display_collision_layers | Display Collision layers |
| 6 | `physics_visual_collision_masks` | physics_display_collision_masks | Display Collision masks |
| 7 | `physics_visual_rigid_body_params` | physics_display_rigid_body_params | Display RigidBody parameters |
| 8 | `physics_visual_physics_material` | physics_display_physics_material | Display Physics material properties |
| 9 | `physics_visual_joint_params` | physics_display_joint_params | Display Joint parameters |
| 10 | `physics_visual_vehicle_params` | physics_display_vehicle_params | Display Vehicle parameters |
| 11 | `physics_visual_character_params` | physics_display_character_params | Display Character parameters |

### 设置视觉 / Settings Visual

设置视觉工具用于查看 Godot 项目设置中各分类的当前配置。

> Settings visual tools for viewing current configuration of each category in Godot project settings.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `settings_visual_application` | settings_display_application | Display Application settings |
| 2 | `settings_visual_rendering` | settings_display_rendering | Display Rendering settings |
| 3 | `settings_visual_physics` | settings_display_physics | Display Physics settings |
| 4 | `settings_visual_input` | settings_display_input | Display Input mapping |
| 5 | `settings_visual_display` | settings_display_display | Display Display settings |
| 6 | `settings_visual_audio` | settings_display_audio | Display Audio settings |
| 7 | `settings_visual_debug` | settings_display_debug | Display Debug settings |
| 8 | `settings_visual_network` | settings_display_network | Display Network settings |
| 9 | `settings_visual_localization` | settings_display_localization | Display Localization settings |
| 10 | `settings_visual_gui` | settings_display_gui | Display GUI theme settings |
| 11 | `settings_visual_importer` | settings_display_importer | Display Importer settings |
| 12 | `settings_visual_layer_names_2d` | settings_display_layer_names_2d | Display 2D layer names |
| 13 | `settings_visual_layer_names_3d` | settings_display_layer_names_3d | Display 3D layer names |
| 14 | `settings_visual_physics_layers` | settings_display_physics_layers | Display Physics layers |
| 15 | `settings_visual_shader_globals` | settings_display_shader_globals | Display Shader global variables |

### IO 视觉 / I/O Visual

IO 视觉工具用于查看输入映射和 I/O 状态。

> I/O visual tools for viewing input mappings and I/O state.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `io_visual_input_map` | io_display_input_map | Display Input action mapping |
| 2 | `io_visual_keyboard_input` | io_display_keyboard_input | Display Keyboard input simulation |
| 3 | `io_visual_mouse_input` | io_display_mouse_input | Display Mouse input simulation |
| 4 | `io_visual_gamepad_input` | io_display_gamepad_input | Display Gamepad input simulation |
| 5 | `io_visual_touch_input` | io_display_touch_input | Display Touch input simulation |
| 6 | `io_visual_midi_input` | io_display_midi_input | Display MIDI input handling |
| 7 | `io_visual_joy_input` | io_display_joy_input | Display Joystick input handling |
| 8 | `io_visual_output_console` | io_display_output_console | Display Output console |
| 9 | `io_visual_debug_print` | io_display_debug_print | Display Debug output |
| 10 | `io_visual_profiler` | io_display_profiler | Display Profiler data |
| 11 | `io_visual_network_socket` | io_display_network_socket | Display Network socket control |

### 脚本视觉 / Script Visual

脚本视觉工具用于查看脚本编辑器中的内容和调试信息。

> Script visual tools for viewing script editor content and debug information.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `script_visual_script_edit` | script_display_script_edit | Display Script editor content |
| 2 | `script_visual_script_output` | script_display_script_output | Display Script output/console |
| 3 | `script_visual_breakpoints` | script_display_breakpoints | Display Debugger breakpoints |
| 4 | `script_visual_watch_variables` | script_display_watch_variables | Display Variable watch display |
| 5 | `script_visual_call_stack` | script_display_call_stack | Display Call stack display |
| 6 | `script_visual_memory_profiler` | script_display_memory_profiler | Display Memory profiling |
| 7 | `script_visual_performance_monitor` | script_display_performance_monitor | Display Performance monitoring |
| 8 | `script_visual_gdscript_highlighter` | script_display_gdscript_highlighter | Display GDScript syntax highlighting |
| 9 | `script_visual_csharp_highlighter` | script_display_csharp_highlighter | Display C# syntax highlighting |
| 10 | `script_visual_autocomplete` | script_display_autocomplete | Display Autocomplete suggestions |

### 资源视觉 / Resource Visual

资源视觉工具用于查看资源导入设置和编辑器。

> Resource visual tools for viewing resource import settings and editors.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `resource_visual_texture_import` | resource_display_texture_import | Display Texture import settings |
| 2 | `resource_visual_mesh_import` | resource_display_mesh_import | Display Mesh import settings |
| 3 | `resource_visual_audio_import` | resource_display_audio_import | Display Audio import settings |
| 4 | `resource_visual_scene_import` | resource_display_scene_import | Display Scene import settings |
| 5 | `resource_visual_font_import` | resource_display_font_import | Display Font import settings |
| 6 | `resource_visual_script_import` | resource_display_script_import | Display Script import settings |
| 7 | `resource_visual_material_editor` | resource_display_material_editor | Display Material editor |
| 8 | `resource_visual_shader_editor` | resource_display_shader_editor | Display Shader editor |
| 9 | `resource_visual_tilemap_editor` | resource_display_tilemap_editor | Display Tilemap editor |
| 10 | `resource_visual_polygon_editor` | resource_display_polygon_editor | Display Polygon editor |
| 11 | `resource_visual_resource_list` | resource_display_resource_list | Display Resource list display |

### 项目视觉 / Project Visual

项目视觉工具用于查看项目元数据和编辑器状态。

> Project visual tools for viewing project metadata and editor state.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `project_visual_project_version` | project_display_project_version | Display Project version info |
| 2 | `project_visual_project_name` | project_display_project_name | Display Project name |
| 3 | `project_visual_project_icon` | project_display_project_icon | Display Project icon |
| 4 | `project_visual_project_author` | project_display_project_author | Display Project author info |
| 5 | `project_visual_build_profile` | project_display_build_profile | Display Build profile |
| 6 | `project_visual_export_preset` | project_display_export_preset | Display Export presets |
| 7 | `project_visual_addon_list` | project_display_addon_list | Display Addon list and settings |
| 8 | `project_visual_autoload` | project_display_autoload | Display Autoload list |
| 9 | `project_visual_scene_tabs` | project_display_scene_tabs | Display Open scene tabs |
| 10 | `project_visual_undo_redo_history` | project_display_undo_redo_history | Display Undo/redo history |
| 11 | `project_visual_version_control` | project_display_version_control | Display Version control integration |

### 视觉 - 变换 / Visual - Transform

视觉变换工具用于分别查看位置、旋转、缩放和速度的各分量值。

> Visual transform tools for viewing individual position, rotation, scale, and velocity components.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `vis_transform_position_x` | display_transform_position_x | Display node position.x |
| 2 | `vis_transform_position_y` | display_transform_position_y | Display node position.y |
| 3 | `vis_transform_position_z` | display_transform_position_z | Display node position.z |
| 4 | `vis_transform_rotation_x` | display_transform_rotation_x | Display node rotation.x |
| 5 | `vis_transform_rotation_y` | display_transform_rotation_y | Display node rotation.y |
| 6 | `vis_transform_rotation_z` | display_transform_rotation_z | Display node rotation.z |
| 7 | `vis_transform_scale_x` | display_transform_scale_x | Display node scale.x |
| 8 | `vis_transform_scale_y` | display_transform_scale_y | Display node scale.y |
| 9 | `vis_transform_scale_z` | display_transform_scale_z | Display node scale.z |
| 10 | `vis_transform_velocity_x` | display_transform_velocity_x | Display node velocity.x |
| 11 | `vis_transform_velocity_y` | display_transform_velocity_y | Display node velocity.y |
| 12 | `vis_transform_velocity_z` | display_transform_velocity_z | Display node velocity.z |
| 13 | `vis_transform_angular_velocity_x` | display_transform_angular_velocity_x | Display node angular_velocity.x |
| 14 | `vis_transform_angular_velocity_y` | display_transform_angular_velocity_y | Display node angular_velocity.y |
| 15 | `vis_transform_angular_velocity_z` | display_transform_angular_velocity_z | Display node angular_velocity.z |

### 视觉 - 颜色 / Visual - Color

视觉颜色工具用于查看各种颜色属性的各通道分量。

> Visual color tools for viewing individual channel components of various color properties.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `vis_color_modulate_r` | display_color_modulate_r | Display modulate.r |
| 2 | `vis_color_modulate_g` | display_color_modulate_g | Display modulate.g |
| 3 | `vis_color_modulate_b` | display_color_modulate_b | Display modulate.b |
| 4 | `vis_color_modulate_a` | display_color_modulate_a | Display modulate.a |
| 5 | `vis_color_self_modulate_r` | display_color_self_modulate_r | Display self_modulate.r |
| 6 | `vis_color_self_modulate_g` | display_color_self_modulate_g | Display self_modulate.g |
| 7 | `vis_color_self_modulate_b` | display_color_self_modulate_b | Display self_modulate.b |
| 8 | `vis_color_self_modulate_a` | display_color_self_modulate_a | Display self_modulate.a |
| 9 | `vis_color_emissive_r` | display_color_emissive_r | Display emissive.r |
| 10 | `vis_color_emissive_g` | display_color_emissive_g | Display emissive.g |
| 11 | `vis_color_emissive_b` | display_color_emissive_b | Display emissive.b |
| 12 | `vis_color_emissive_a` | display_color_emissive_a | Display emissive.a |
| 13 | `vis_color_ambient_light_color_r` | display_color_ambient_light_color_r | Display ambient_light_color.r |
| 14 | `vis_color_ambient_light_color_g` | display_color_ambient_light_color_g | Display ambient_light_color.g |
| 15 | `vis_color_ambient_light_color_b` | display_color_ambient_light_color_b | Display ambient_light_color.b |
| 16 | `vis_color_ambient_light_color_a` | display_color_ambient_light_color_a | Display ambient_light_color.a |
| 17 | `vis_color_background_color_r` | display_color_background_color_r | Display background_color.r |
| 18 | `vis_color_background_color_g` | display_color_background_color_g | Display background_color.g |
| 19 | `vis_color_background_color_b` | display_color_background_color_b | Display background_color.b |
| 20 | `vis_color_background_color_a` | display_color_background_color_a | Display background_color.a |
| 21 | `vis_color_fog_color_r` | display_color_fog_color_r | Display fog_color.r |
| 22 | `vis_color_fog_color_g` | display_color_fog_color_g | Display fog_color.g |
| 23 | `vis_color_fog_color_b` | display_color_fog_color_b | Display fog_color.b |
| 24 | `vis_color_fog_color_a` | display_color_fog_color_a | Display fog_color.a |
| 25 | `vis_color_outline_color_r` | display_color_outline_color_r | Display outline_color.r |
| 26 | `vis_color_outline_color_g` | display_color_outline_color_g | Display outline_color.g |
| 27 | `vis_color_outline_color_b` | display_color_outline_color_b | Display outline_color.b |
| 28 | `vis_color_outline_color_a` | display_color_outline_color_a | Display outline_color.a |
| 29 | `vis_color_shadow_color_r` | display_color_shadow_color_r | Display shadow_color.r |
| 30 | `vis_color_shadow_color_g` | display_color_shadow_color_g | Display shadow_color.g |
| 31 | `vis_color_shadow_color_b` | display_color_shadow_color_b | Display shadow_color.b |
| 32 | `vis_color_shadow_color_a` | display_color_shadow_color_a | Display shadow_color.a |

### 视觉 - 相机 / Visual - Camera

视觉相机工具用于查看编辑器中 3D 视口的相机控制状态。

> Visual camera tools for viewing 3D viewport camera control state in the editor.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `vis_camera_orbit_left` | display_camera_orbit_left | Display camera orbit_left |
| 2 | `vis_camera_orbit_right` | display_camera_orbit_right | Display camera orbit_right |
| 3 | `vis_camera_orbit_up` | display_camera_orbit_up | Display camera orbit_up |
| 4 | `vis_camera_orbit_down` | display_camera_orbit_down | Display camera orbit_down |
| 5 | `vis_camera_pan_left` | display_camera_pan_left | Display camera pan_left |
| 6 | `vis_camera_pan_right` | display_camera_pan_right | Display camera pan_right |
| 7 | `vis_camera_pan_up` | display_camera_pan_up | Display camera pan_up |
| 8 | `vis_camera_pan_down` | display_camera_pan_down | Display camera pan_down |
| 9 | `vis_camera_zoom_in` | display_camera_zoom_in | Display camera zoom_in |
| 10 | `vis_camera_zoom_out` | display_camera_zoom_out | Display camera zoom_out |
| 11 | `vis_camera_fit_selection` | display_camera_fit_selection | Display camera fit_selection |
| 12 | `vis_camera_focus_point` | display_camera_focus_point | Display camera focus_point |
| 13 | `vis_camera_toggle_orthogonal` | display_camera_toggle_orthogonal | Display camera toggle_orthogonal |
| 14 | `vis_camera_toggle_perspective` | display_camera_toggle_perspective | Display camera toggle_perspective |
| 15 | `vis_camera_reset_view` | display_camera_reset_view | Display camera reset_view |
| 16 | `vis_camera_set_camera_position` | display_camera_set_camera_position | Display camera set_camera_position |
| 17 | `vis_camera_set_camera_rotation` | display_camera_set_camera_rotation | Display camera set_camera_rotation |
| 18 | `vis_camera_set_camera_fov` | display_camera_set_camera_fov | Display camera set_camera_fov |

### 视觉 - 监控 / Visual - Monitor

视觉监控工具用于查看引擎运行时性能指标。

> Visual monitor tools for viewing engine runtime performance metrics.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `vis_monitor_performance_metrics` | display_monitor_performance_metrics | Display performance_metrics |
| 2 | `vis_monitor_memory_usage` | display_monitor_memory_usage | Display memory_usage |
| 3 | `vis_monitor_frame_time` | display_monitor_frame_time | Display frame_time |
| 4 | `vis_monitor_draw_calls` | display_monitor_draw_calls | Display draw_calls |
| 5 | `vis_monitor_vertex_count` | display_monitor_vertex_count | Display vertex_count |
| 6 | `vis_monitor_triangle_count` | display_monitor_triangle_count | Display triangle_count |
| 7 | `vis_monitor_node_count` | display_monitor_node_count | Display node_count |
| 8 | `vis_monitor_resource_count` | display_monitor_resource_count | Display resource_count |
| 9 | `vis_monitor_physics_bodies` | display_monitor_physics_bodies | Display physics_bodies |
| 10 | `vis_monitor_active_scripts` | display_monitor_active_scripts | Display active_scripts |
| 11 | `vis_monitor_texture_memory` | display_monitor_texture_memory | Display texture_memory |
| 12 | `vis_monitor_buffer_memory` | display_monitor_buffer_memory | Display buffer_memory |
| 13 | `vis_monitor_cpu_time` | display_monitor_cpu_time | Display cpu_time |
| 14 | `vis_monitor_gpu_time` | display_monitor_gpu_time | Display gpu_time |
| 15 | `vis_monitor_frame_rate` | display_monitor_frame_rate | Display frame_rate |

### 视觉 - 场景 / Visual - Scene

视觉场景工具用于查看场景文件和节点的管理状态。

> Visual scene tools for viewing scene file and node management state.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `vis_scene_new_scene` | display_scene_new_scene | Display scene new_scene |
| 2 | `vis_scene_open_scene` | display_scene_open_scene | Display scene open_scene |
| 3 | `vis_scene_save_scene` | display_scene_save_scene | Display scene save_scene |
| 4 | `vis_scene_save_scene_as` | display_scene_save_scene_as | Display scene save_scene_as |
| 5 | `vis_scene_close_scene` | display_scene_close_scene | Display scene close_scene |
| 6 | `vis_scene_close_all_scenes` | display_scene_close_all_scenes | Display scene close_all_scenes |
| 7 | `vis_scene_reload_scene` | display_scene_reload_scene | Display scene reload_scene |
| 8 | `vis_scene_instantiate_scene` | display_scene_instantiate_scene | Display scene instantiate_scene |
| 9 | `vis_scene_clear_dependencies` | display_scene_clear_dependencies | Display scene clear_dependencies |
| 10 | `vis_scene_find_unique_node` | display_scene_find_unique_node | Display scene find_unique_node |
| 11 | `vis_scene_get_node_count` | display_scene_get_node_count | Display scene get_node_count |
| 12 | `vis_scene_get_node_list` | display_scene_get_node_list | Display scene get_node_list |
| 13 | `vis_scene_get_node_path` | display_scene_get_node_path | Display scene get_node_path |

### 视觉 - 渲染 / Visual - Render

视觉渲染工具用于查看渲染环境的高级参数。

> Visual render tools for viewing advanced render environment parameters.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `vis_render_ambient_light_energy` | display_render_ambient_light_energy | Display rendering ambient_light_energy |
| 2 | `vis_render_ambient_light_sky_contribution` | display_render_ambient_light_sky_contribution | Display rendering ambient_light_sky_contribution |
| 3 | `vis_render_reflected_light_source` | display_render_reflected_light_source | Display rendering reflected_light_source |
| 4 | `vis_render_adjustment_brightness` | display_render_adjustment_brightness | Display rendering adjustment_brightness |
| 5 | `vis_render_adjustment_contrast` | display_render_adjustment_contrast | Display rendering adjustment_contrast |
| 6 | `vis_render_adjustment_saturation` | display_render_adjustment_saturation | Display rendering adjustment_saturation |
| 7 | `vis_render_fog_aerial_perspective` | display_render_fog_aerial_perspective | Display rendering fog_aerial_perspective |
| 8 | `vis_render_fog_density` | display_render_fog_density | Display rendering fog_density |
| 9 | `vis_render_tonemap_exposure` | display_render_tonemap_exposure | Display rendering tonemap_exposure |
| 10 | `vis_render_tonemap_white_point` | display_render_tonemap_white_point | Display rendering tonemap_white_point |

### 视觉 - 物理 / Visual - Physics

视觉物理工具用于查看物理体的各项参数。

> Visual physics tools for viewing physics body parameters.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `vis_physics_mass` | display_physics_mass | Display physics mass |
| 2 | `vis_physics_friction` | display_physics_friction | Display physics friction |
| 3 | `vis_physics_bounce` | display_physics_bounce | Display physics bounce |
| 4 | `vis_physics_gravity_scale` | display_physics_gravity_scale | Display physics gravity_scale |
| 5 | `vis_physics_linear_damping` | display_physics_linear_damping | Display physics linear_damping |
| 6 | `vis_physics_angular_damping` | display_physics_angular_damping | Display physics angular_damping |
| 7 | `vis_physics_max_contacts_reported` | display_physics_max_contacts_reported | Display physics max_contacts_reported |
| 8 | `vis_physics_continuous_cd` | display_physics_continuous_cd | Display physics continuous_cd |

### 视觉 - 音频 / Visual - Audio

视觉音频工具用于查看音频播放器的参数。

> Visual audio tools for viewing audio player parameters.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `vis_audio_volume_db` | display_audio_volume_db | Display audio volume_db |
| 2 | `vis_audio_pitch_scale` | display_audio_pitch_scale | Display audio pitch_scale |
| 3 | `vis_audio_panning` | display_audio_panning | Display audio panning |
| 4 | `vis_audio_bus` | display_audio_bus | Display audio bus |
| 5 | `vis_audio_mix_target` | display_audio_mix_target | Display audio mix_target |
| 6 | `vis_audio_max_polyphony` | display_audio_max_polyphony | Display audio max_polyphony |
| 7 | `vis_audio_stream_paused` | display_audio_stream_paused | Display audio stream_paused |

### 视觉 - UI / Visual - UI

视觉 UI 工具用于查看界面控件的排版和字体参数。

> Visual UI tools for viewing layout and font parameters of UI controls.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `vis_ui_font` | display_ui_font | Display UI font |
| 2 | `vis_ui_font_size` | display_ui_font_size | Display UI font_size |
| 3 | `vis_ui_font_color` | display_ui_font_color | Display UI font_color |
| 4 | `vis_ui_outline_size` | display_ui_outline_size | Display UI outline_size |
| 5 | `vis_ui_custom_minimum_size_x` | display_ui_custom_minimum_size_x | Display UI custom_minimum_size_x |
| 6 | `vis_ui_custom_minimum_size_y` | display_ui_custom_minimum_size_y | Display UI custom_minimum_size_y |
| 7 | `vis_ui_text_alignment` | display_ui_text_alignment | Display UI text_alignment |
| 8 | `vis_ui_text_overflow` | display_ui_text_overflow | Display UI text_overflow |
| 9 | `vis_ui_clip_text` | display_ui_clip_text | Display UI clip_text |
| 10 | `vis_ui_margin_left` | display_ui_margin_left | Display UI margin_left |
| 11 | `vis_ui_margin_top` | display_ui_margin_top | Display UI margin_top |
| 12 | `vis_ui_margin_right` | display_ui_margin_right | Display UI margin_right |
| 13 | `vis_ui_margin_bottom` | display_ui_margin_bottom | Display UI margin_bottom |
| 14 | `vis_ui_anchor_left` | display_ui_anchor_left | Display UI anchor_left |
| 15 | `vis_ui_anchor_top` | display_ui_anchor_top | Display UI anchor_top |
| 16 | `vis_ui_anchor_right` | display_ui_anchor_right | Display UI anchor_right |
| 17 | `vis_ui_anchor_bottom` | display_ui_anchor_bottom | Display UI anchor_bottom |

---

## 控制工具表格 / Control Tool Tables

**控制工具**修改 Godot 引擎状态，执行操作。包括创建/删除节点、设置属性、模拟用户输入、执行编辑器命令等。

> **Control Tools** modify Godot engine state and execute operations. Includes creating/deleting nodes, setting properties, simulating user input, executing editor commands, etc.

### UI 控制 / UI Control

UI 控制工具用于操作 Godot 编辑器界面的按钮、菜单和工具栏。

> UI control tools for operating Godot editor interface buttons, menus, and toolbars.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ui_control_menu_file_new` | menu_file_new | Create new project |
| 2 | `ui_control_menu_file_open` | menu_file_open | Open project |
| 3 | `ui_control_menu_file_save` | menu_file_save | Save project |
| 4 | `ui_control_menu_edit_undo` | menu_edit_undo | Undo action |
| 5 | `ui_control_menu_edit_redo` | menu_edit_redo | Redo action |
| 6 | `ui_control_menu_scene_save` | menu_scene_save | Save scene |
| 7 | `ui_control_toolbar_play_scene` | toolbar_play_scene | Play scene button |
| 8 | `ui_control_toolbar_play_project` | toolbar_play_project | Play project button |
| 9 | `ui_control_toolbar_stop` | toolbar_stop | Stop execution button |
| 10 | `ui_control_toolbar_pause` | toolbar_pause | Pause execution button |
| 11 | `ui_control_toolbar_step` | toolbar_step | Step execution button |
| 12 | `ui_control_button_new_node` | button_new_node | Create new node |
| 13 | `ui_control_button_delete_node` | button_delete_node | Delete selected node |
| 14 | `ui_control_button_duplicate_node` | button_duplicate_node | Duplicate node |
| 15 | `ui_control_dock_switch_scene` | dock_switch_scene | Switch to scene dock |
| 16 | `ui_control_dock_switch_import` | dock_switch_import | Switch to import dock |

### 节点控制 / Node Control

节点控制工具用于在场景树中创建各类节点实例。

> Node control tools for creating various node instances in the scene tree.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `node_control_create_node` | node_create_Node | Create Node instance |
| 2 | `node_control_create_node2d` | node_create_Node2D | Create Node2D instance |
| 3 | `node_control_create_node3d` | node_create_Node3D | Create Node3D instance |
| 4 | `node_control_create_control` | node_create_Control | Create Control instance |
| 5 | `node_control_create_canvasitem` | node_create_CanvasItem | Create CanvasItem instance |
| 6 | `node_control_create_physicsbody2d` | node_create_PhysicsBody2D | Create PhysicsBody2D instance |
| 7 | `node_control_create_physicsbody3d` | node_create_PhysicsBody3D | Create PhysicsBody3D instance |
| 8 | `node_control_create_characterbody2d` | node_create_CharacterBody2D | Create CharacterBody2D instance |
| 9 | `node_control_create_characterbody3d` | node_create_CharacterBody3D | Create CharacterBody3D instance |
| 10 | `node_control_create_rigidbody2d` | node_create_RigidBody2D | Create RigidBody2D instance |
| 11 | `node_control_create_rigidbody3d` | node_create_RigidBody3D | Create RigidBody3D instance |
| 12 | `node_control_create_staticbody2d` | node_create_StaticBody2D | Create StaticBody2D instance |
| 13 | `node_control_create_staticbody3d` | node_create_StaticBody3D | Create StaticBody3D instance |
| 14 | `node_control_create_sprite2d` | node_create_Sprite2D | Create Sprite2D instance |
| 15 | `node_control_create_sprite3d` | node_create_Sprite3D | Create Sprite3D instance |
| 16 | `node_control_create_meshinstance3d` | node_create_MeshInstance3D | Create MeshInstance3D instance |
| 17 | `node_control_create_skeletonik3d` | node_create_SkeletonIK3D | Create SkeletonIK3D instance |
| 18 | `node_control_create_camera2d` | node_create_Camera2D | Create Camera2D instance |
| 19 | `node_control_create_camera3d` | node_create_Camera3D | Create Camera3D instance |
| 20 | `node_control_create_light2d` | node_create_Light2D | Create Light2D instance |
| 21 | `node_control_create_light3d` | node_create_Light3D | Create Light3D instance |
| 22 | `node_control_create_omnilight3d` | node_create_OmniLight3D | Create OmniLight3D instance |
| 23 | `node_control_create_spotlight3d` | node_create_SpotLight3D | Create SpotLight3D instance |
| 24 | `node_control_create_directionallight3d` | node_create_DirectionalLight3D | Create DirectionalLight3D instance |
| 25 | `node_control_create_audiostreamplayer` | node_create_AudioStreamPlayer | Create AudioStreamPlayer instance |
| 26 | `node_control_create_audiostreamplayer2d` | node_create_AudioStreamPlayer2D | Create AudioStreamPlayer2D instance |
| 27 | `node_control_create_audiostreamplayer3d` | node_create_AudioStreamPlayer3D | Create AudioStreamPlayer3D instance |
| 28 | `node_control_create_animationplayer` | node_create_AnimationPlayer | Create AnimationPlayer instance |
| 29 | `node_control_create_animatedsprite2d` | node_create_AnimatedSprite2D | Create AnimatedSprite2D instance |
| 30 | `node_control_create_animatedsprite3d` | node_create_AnimatedSprite3D | Create AnimatedSprite3D instance |
| 31 | `node_control_create_visibleonscreennotifier2d` | node_create_VisibleOnScreenNotifier2D | Create VisibleOnScreenNotifier2D instance |
| 32 | `node_control_create_visibleonscreennotifier3d` | node_create_VisibleOnScreenNotifier3D | Create VisibleOnScreenNotifier3D instance |
| 33 | `node_control_create_marker2d` | node_create_Marker2D | Create Marker2D instance |
| 34 | `node_control_create_marker3d` | node_create_Marker3D | Create Marker3D instance |
| 35 | `node_control_create_path2d` | node_create_Path2D | Create Path2D instance |
| 36 | `node_control_create_path3d` | node_create_Path3D | Create Path3D instance |
| 37 | `node_control_create_area2d` | node_create_Area2D | Create Area2D instance |
| 38 | `node_control_create_area3d` | node_create_Area3D | Create Area3D instance |
| 39 | `node_control_create_collisionshape2d` | node_create_CollisionShape2D | Create CollisionShape2D instance |
| 40 | `node_control_create_collisionshape3d` | node_create_CollisionShape3D | Create CollisionShape3D instance |
| 41 | `node_control_create_ui_control` | node_create_UI/Control | Create UI/Control instance |
| 42 | `node_control_create_ui_button` | node_create_UI/Button | Create UI/Button instance |
| 43 | `node_control_create_ui_label` | node_create_UI/Label | Create UI/Label instance |
| 44 | `node_control_create_ui_textedit` | node_create_UI/TextEdit | Create UI/TextEdit instance |
| 45 | `node_control_create_ui_lineedit` | node_create_UI/LineEdit | Create UI/LineEdit instance |
| 46 | `node_control_create_ui_panel` | node_create_UI/Panel | Create UI/Panel instance |
| 47 | `node_control_create_ui_panelcontainer` | node_create_UI/PanelContainer | Create UI/PanelContainer instance |
| 48 | `node_control_create_ui_vboxcontainer` | node_create_UI/VBoxContainer | Create UI/VBoxContainer instance |
| 49 | `node_control_create_ui_hboxcontainer` | node_create_UI/HBoxContainer | Create UI/HBoxContainer instance |

### 属性控制 / Property Control

属性控制工具用于设置节点的基本变换和渲染属性。

> Property control tools for setting basic transform and rendering properties of nodes.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `prop_control_position` | property_set_position | Set node Node position (Vector2/Vector3) |
| 2 | `prop_control_rotation` | property_set_rotation | Set node Node rotation |
| 3 | `prop_control_scale` | property_set_scale | Set node Node scale |
| 4 | `prop_control_transform` | property_set_transform | Set node Node transform matrix |
| 5 | `prop_control_visible` | property_set_visible | Set node Node visibility |
| 6 | `prop_control_modulate` | property_set_modulate | Set node Node modulation (color/alpha) |
| 7 | `prop_control_self_modulate` | property_set_self_modulate | Set node Self modulation |
| 8 | `prop_control_name` | property_set_name | Set node Node name |
| 9 | `prop_control_owner` | property_set_owner | Set node Node owner |
| 10 | `prop_control_unique_name_in_owner` | property_set_unique_name_in_owner | Set node Unique name flag |
| 11 | `prop_control_process_mode` | property_set_process_mode | Set node Process mode (inherit/pausable/when_paused/always/disabled) |
| 12 | `prop_control_custom_multiplayer` | property_set_custom_multiplayer | Set node Custom multiplayer setting |
| 13 | `prop_control_physics_interpolation_mode` | property_set_physics_interpolation_mode | Set node Physics interpolation |

### 渲染控制 / Render Control

渲染控制工具用于修改视口和渲染管线的参数。

> Render control tools for modifying viewport and rendering pipeline parameters.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `render_control_viewport_camera` | render_modify_viewport_camera | Modify Viewport camera position/rotation |
| 2 | `render_control_viewport_zoom` | render_modify_viewport_zoom | Modify Viewport zoom level |
| 3 | `render_control_viewport_grid` | render_modify_viewport_grid | Modify Grid display settings |
| 4 | `render_control_viewport_gizmo` | render_modify_viewport_gizmo | Modify Gizmo display |
| 5 | `render_control_render_environment` | render_modify_render_environment | Modify Environment (lighting, fog, sky) |
| 6 | `render_control_render_world_env` | render_modify_render_world_env | Modify World environment |
| 7 | `render_control_render_lights` | render_modify_render_lights | Modify Light properties |
| 8 | `render_control_render_shadows` | render_modify_render_shadows | Modify Shadow settings |
| 9 | `render_control_render_materials` | render_modify_render_materials | Modify Material properties |
| 10 | `render_control_render_textures` | render_modify_render_textures | Modify Texture properties |
| 11 | `render_control_render_shaders` | render_modify_render_shaders | Modify Shader properties |
| 12 | `render_control_render_canvas` | render_modify_render_canvas | Modify Canvas layer rendering |
| 13 | `render_control_render_post_process` | render_modify_render_post_process | Modify Post-processing effects |
| 14 | `render_control_render_lod` | render_modify_render_lod | Modify LOD settings |
| 15 | `render_control_render_occlusion` | render_modify_render_occlusion | Modify Occlusion culling |

### 动画控制 / Animation Control

动画控制工具用于修改动画编辑器的状态。

> Animation control tools for modifying animation editor state.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `anim_control_timeline` | anim_modify_timeline | Modify Animation timeline |
| 2 | `anim_control_keyframes` | anim_modify_keyframes | Modify Keyframe display |
| 3 | `anim_control_playback_position` | anim_modify_playback_position | Modify Playback position |
| 4 | `anim_control_playback_speed` | anim_modify_playback_speed | Modify Playback speed |
| 5 | `anim_control_animation_list` | anim_modify_animation_list | Modify Animation list |
| 6 | `anim_control_track_list` | anim_modify_track_list | Modify Animation tracks |
| 7 | `anim_control_bezier_editor` | anim_modify_bezier_editor | Modify Bezier curve editor |
| 8 | `anim_control_animation_blend` | anim_modify_animation_blend | Modify Animation blending |
| 9 | `anim_control_animation_state_machine` | anim_modify_animation_state_machine | Modify State machine transitions |

### 物理控制 / Physics Control

物理控制工具用于修改物理世界的参数。

> Physics control tools for modifying physics world parameters.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `physics_control_2d_gravity` | physics_modify_2d_gravity | Modify 2D world gravity |
| 2 | `physics_control_2d_damping` | physics_modify_2d_damping | Modify 2D damping settings |
| 3 | `physics_control_3d_gravity` | physics_modify_3d_gravity | Modify 3D world gravity |
| 4 | `physics_control_3d_damping` | physics_modify_3d_damping | Modify 3D damping settings |
| 5 | `physics_control_collision_layers` | physics_modify_collision_layers | Modify Collision layers |
| 6 | `physics_control_collision_masks` | physics_modify_collision_masks | Modify Collision masks |
| 7 | `physics_control_rigid_body_params` | physics_modify_rigid_body_params | Modify RigidBody parameters |
| 8 | `physics_control_physics_material` | physics_modify_physics_material | Modify Physics material properties |
| 9 | `physics_control_joint_params` | physics_modify_joint_params | Modify Joint parameters |
| 10 | `physics_control_vehicle_params` | physics_modify_vehicle_params | Modify Vehicle parameters |
| 11 | `physics_control_character_params` | physics_modify_character_params | Modify Character parameters |

### 设置控制 / Settings Control

设置控制工具用于修改 Godot 项目设置中各分类的配置。

> Settings control tools for modifying configuration of each category in Godot project settings.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `settings_control_application` | settings_modify_application | Modify Application settings |
| 2 | `settings_control_rendering` | settings_modify_rendering | Modify Rendering settings |
| 3 | `settings_control_physics` | settings_modify_physics | Modify Physics settings |
| 4 | `settings_control_input` | settings_modify_input | Modify Input mapping |
| 5 | `settings_control_display` | settings_modify_display | Modify Display settings |
| 6 | `settings_control_audio` | settings_modify_audio | Modify Audio settings |
| 7 | `settings_control_debug` | settings_modify_debug | Modify Debug settings |
| 8 | `settings_control_network` | settings_modify_network | Modify Network settings |
| 9 | `settings_control_localization` | settings_modify_localization | Modify Localization settings |
| 10 | `settings_control_gui` | settings_modify_gui | Modify GUI theme settings |
| 11 | `settings_control_importer` | settings_modify_importer | Modify Importer settings |
| 12 | `settings_control_layer_names_2d` | settings_modify_layer_names_2d | Modify 2D layer names |
| 13 | `settings_control_layer_names_3d` | settings_modify_layer_names_3d | Modify 3D layer names |
| 14 | `settings_control_physics_layers` | settings_modify_physics_layers | Modify Physics layers |
| 15 | `settings_control_shader_globals` | settings_modify_shader_globals | Modify Shader global variables |

### IO 控制 / I/O Control

IO 控制工具用于操作输入映射和 I/O 设备。

> I/O control tools for operating input mappings and I/O devices.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `io_control_input_map` | io_command_input_map | Control Input action mapping |
| 2 | `io_control_keyboard_input` | io_command_keyboard_input | Control Keyboard input simulation |
| 3 | `io_control_mouse_input` | io_command_mouse_input | Control Mouse input simulation |
| 4 | `io_control_gamepad_input` | io_command_gamepad_input | Control Gamepad input simulation |
| 5 | `io_control_touch_input` | io_command_touch_input | Control Touch input simulation |
| 6 | `io_control_midi_input` | io_command_midi_input | Control MIDI input handling |
| 7 | `io_control_joy_input` | io_command_joy_input | Control Joystick input handling |
| 8 | `io_control_output_console` | io_command_output_console | Control Output console |
| 9 | `io_control_debug_print` | io_command_debug_print | Control Debug output |
| 10 | `io_control_profiler` | io_command_profiler | Control Profiler data |
| 11 | `io_control_network_socket` | io_command_network_socket | Control Network socket control |

### 脚本控制 / Script Control

脚本控制工具用于管理脚本编辑器和调试器。

> Script control tools for managing the script editor and debugger.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `script_control_script_edit` | script_manage_script_edit | Manage Script editor content |
| 2 | `script_control_script_output` | script_manage_script_output | Manage Script output/console |
| 3 | `script_control_breakpoints` | script_manage_breakpoints | Manage Debugger breakpoints |
| 4 | `script_control_watch_variables` | script_manage_watch_variables | Manage Variable watch display |
| 5 | `script_control_call_stack` | script_manage_call_stack | Manage Call stack display |
| 6 | `script_control_memory_profiler` | script_manage_memory_profiler | Manage Memory profiling |
| 7 | `script_control_performance_monitor` | script_manage_performance_monitor | Manage Performance monitoring |
| 8 | `script_control_gdscript_highlighter` | script_manage_gdscript_highlighter | Manage GDScript syntax highlighting |
| 9 | `script_control_csharp_highlighter` | script_manage_csharp_highlighter | Manage C# syntax highlighting |
| 10 | `script_control_autocomplete` | script_manage_autocomplete | Manage Autocomplete suggestions |

### 资源控制 / Resource Control

资源控制工具用于管理资源的导入设置和编辑。

> Resource control tools for managing resource import settings and editing.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `resource_control_texture_import` | resource_manage_texture_import | Manage Texture import settings |
| 2 | `resource_control_mesh_import` | resource_manage_mesh_import | Manage Mesh import settings |
| 3 | `resource_control_audio_import` | resource_manage_audio_import | Manage Audio import settings |
| 4 | `resource_control_scene_import` | resource_manage_scene_import | Manage Scene import settings |
| 5 | `resource_control_font_import` | resource_manage_font_import | Manage Font import settings |
| 6 | `resource_control_script_import` | resource_manage_script_import | Manage Script import settings |
| 7 | `resource_control_material_editor` | resource_manage_material_editor | Manage Material editor |
| 8 | `resource_control_shader_editor` | resource_manage_shader_editor | Manage Shader editor |
| 9 | `resource_control_tilemap_editor` | resource_manage_tilemap_editor | Manage Tilemap editor |
| 10 | `resource_control_polygon_editor` | resource_manage_polygon_editor | Manage Polygon editor |
| 11 | `resource_control_resource_list` | resource_manage_resource_list | Manage Resource list display |

### 项目控制 / Project Control

项目控制工具用于管理项目元数据和编辑器状态。

> Project control tools for managing project metadata and editor state.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `project_control_project_version` | project_manage_project_version | Manage Project version info |
| 2 | `project_control_project_name` | project_manage_project_name | Manage Project name |
| 3 | `project_control_project_icon` | project_manage_project_icon | Manage Project icon |
| 4 | `project_control_project_author` | project_manage_project_author | Manage Project author info |
| 5 | `project_control_build_profile` | project_manage_build_profile | Manage Build profile |
| 6 | `project_control_export_preset` | project_manage_export_preset | Manage Export presets |
| 7 | `project_control_addon_list` | project_manage_addon_list | Manage Addon list and settings |
| 8 | `project_control_autoload` | project_manage_autoload | Manage Autoload list |
| 9 | `project_control_scene_tabs` | project_manage_scene_tabs | Manage Open scene tabs |
| 10 | `project_control_undo_redo_history` | project_manage_undo_redo_history | Manage Undo/redo history |
| 11 | `project_control_version_control` | project_manage_version_control | Manage Version control integration |

### 控制 - 变换 / Control - Transform

控制变换工具用于分别设置位置、旋转、缩放和速度的各分量值。

> Control transform tools for setting individual position, rotation, scale, and velocity components.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_transform_position_x` | set_transform_position_x | Set node position.x |
| 2 | `ctrl_transform_position_y` | set_transform_position_y | Set node position.y |
| 3 | `ctrl_transform_position_z` | set_transform_position_z | Set node position.z |
| 4 | `ctrl_transform_rotation_x` | set_transform_rotation_x | Set node rotation.x |
| 5 | `ctrl_transform_rotation_y` | set_transform_rotation_y | Set node rotation.y |
| 6 | `ctrl_transform_rotation_z` | set_transform_rotation_z | Set node rotation.z |
| 7 | `ctrl_transform_scale_x` | set_transform_scale_x | Set node scale.x |
| 8 | `ctrl_transform_scale_y` | set_transform_scale_y | Set node scale.y |
| 9 | `ctrl_transform_scale_z` | set_transform_scale_z | Set node scale.z |
| 10 | `ctrl_transform_velocity_x` | set_transform_velocity_x | Set node velocity.x |
| 11 | `ctrl_transform_velocity_y` | set_transform_velocity_y | Set node velocity.y |
| 12 | `ctrl_transform_velocity_z` | set_transform_velocity_z | Set node velocity.z |
| 13 | `ctrl_transform_angular_velocity_x` | set_transform_angular_velocity_x | Set node angular_velocity.x |
| 14 | `ctrl_transform_angular_velocity_y` | set_transform_angular_velocity_y | Set node angular_velocity.y |
| 15 | `ctrl_transform_angular_velocity_z` | set_transform_angular_velocity_z | Set node angular_velocity.z |

### 控制 - 颜色 / Control - Color

控制颜色工具用于设置各种颜色属性的各通道分量。

> Control color tools for setting individual channel components of various color properties.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_color_modulate_r` | set_color_modulate_r | Set modulate.r |
| 2 | `ctrl_color_modulate_g` | set_color_modulate_g | Set modulate.g |
| 3 | `ctrl_color_modulate_b` | set_color_modulate_b | Set modulate.b |
| 4 | `ctrl_color_modulate_a` | set_color_modulate_a | Set modulate.a |
| 5 | `ctrl_color_self_modulate_r` | set_color_self_modulate_r | Set self_modulate.r |
| 6 | `ctrl_color_self_modulate_g` | set_color_self_modulate_g | Set self_modulate.g |
| 7 | `ctrl_color_self_modulate_b` | set_color_self_modulate_b | Set self_modulate.b |
| 8 | `ctrl_color_self_modulate_a` | set_color_self_modulate_a | Set self_modulate.a |
| 9 | `ctrl_color_emissive_r` | set_color_emissive_r | Set emissive.r |
| 10 | `ctrl_color_emissive_g` | set_color_emissive_g | Set emissive.g |
| 11 | `ctrl_color_emissive_b` | set_color_emissive_b | Set emissive.b |
| 12 | `ctrl_color_emissive_a` | set_color_emissive_a | Set emissive.a |
| 13 | `ctrl_color_ambient_light_color_r` | set_color_ambient_light_color_r | Set ambient_light_color.r |
| 14 | `ctrl_color_ambient_light_color_g` | set_color_ambient_light_color_g | Set ambient_light_color.g |
| 15 | `ctrl_color_ambient_light_color_b` | set_color_ambient_light_color_b | Set ambient_light_color.b |
| 16 | `ctrl_color_ambient_light_color_a` | set_color_ambient_light_color_a | Set ambient_light_color.a |
| 17 | `ctrl_color_background_color_r` | set_color_background_color_r | Set background_color.r |
| 18 | `ctrl_color_background_color_g` | set_color_background_color_g | Set background_color.g |
| 19 | `ctrl_color_background_color_b` | set_color_background_color_b | Set background_color.b |
| 20 | `ctrl_color_background_color_a` | set_color_background_color_a | Set background_color.a |
| 21 | `ctrl_color_fog_color_r` | set_color_fog_color_r | Set fog_color.r |
| 22 | `ctrl_color_fog_color_g` | set_color_fog_color_g | Set fog_color.g |
| 23 | `ctrl_color_fog_color_b` | set_color_fog_color_b | Set fog_color.b |
| 24 | `ctrl_color_fog_color_a` | set_color_fog_color_a | Set fog_color.a |
| 25 | `ctrl_color_outline_color_r` | set_color_outline_color_r | Set outline_color.r |
| 26 | `ctrl_color_outline_color_g` | set_color_outline_color_g | Set outline_color.g |
| 27 | `ctrl_color_outline_color_b` | set_color_outline_color_b | Set outline_color.b |
| 28 | `ctrl_color_outline_color_a` | set_color_outline_color_a | Set outline_color.a |
| 29 | `ctrl_color_shadow_color_r` | set_color_shadow_color_r | Set shadow_color.r |
| 30 | `ctrl_color_shadow_color_g` | set_color_shadow_color_g | Set shadow_color.g |
| 31 | `ctrl_color_shadow_color_b` | set_color_shadow_color_b | Set shadow_color.b |
| 32 | `ctrl_color_shadow_color_a` | set_color_shadow_color_a | Set shadow_color.a |

### 控制 - 相机 / Control - Camera

控制相机工具用于操作编辑器中 3D 视口的相机。

> Control camera tools for operating the 3D viewport camera in the editor.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_camera_orbit_left` | orbit_left | Camera operation: orbit_left |
| 2 | `ctrl_camera_orbit_right` | orbit_right | Camera operation: orbit_right |
| 3 | `ctrl_camera_orbit_up` | orbit_up | Camera operation: orbit_up |
| 4 | `ctrl_camera_orbit_down` | orbit_down | Camera operation: orbit_down |
| 5 | `ctrl_camera_pan_left` | pan_left | Camera operation: pan_left |
| 6 | `ctrl_camera_pan_right` | pan_right | Camera operation: pan_right |
| 7 | `ctrl_camera_pan_up` | pan_up | Camera operation: pan_up |
| 8 | `ctrl_camera_pan_down` | pan_down | Camera operation: pan_down |
| 9 | `ctrl_camera_zoom_in` | zoom_in | Camera operation: zoom_in |
| 10 | `ctrl_camera_zoom_out` | zoom_out | Camera operation: zoom_out |
| 11 | `ctrl_camera_fit_selection` | fit_selection | Camera operation: fit_selection |
| 12 | `ctrl_camera_focus_point` | focus_point | Camera operation: focus_point |
| 13 | `ctrl_camera_toggle_orthogonal` | toggle_orthogonal | Camera operation: toggle_orthogonal |
| 14 | `ctrl_camera_toggle_perspective` | toggle_perspective | Camera operation: toggle_perspective |
| 15 | `ctrl_camera_reset_view` | reset_view | Camera operation: reset_view |
| 16 | `ctrl_camera_set_camera_position` | set_camera_position | Camera operation: set_camera_position |
| 17 | `ctrl_camera_set_camera_rotation` | set_camera_rotation | Camera operation: set_camera_rotation |
| 18 | `ctrl_camera_set_camera_fov` | set_camera_fov | Camera operation: set_camera_fov |

### 控制 - 动画 / Control - Animation

控制动画工具用于添加、删除和修改关键帧。

> Control animation tools for adding, removing, and modifying keyframes.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_anim_add_keyframe` | add_keyframe | Animation operation: add_keyframe |
| 2 | `ctrl_anim_remove_keyframe` | remove_keyframe | Animation operation: remove_keyframe |
| 3 | `ctrl_anim_modify_keyframe_time` | modify_keyframe_time | Animation operation: modify_keyframe_time |
| 4 | `ctrl_anim_modify_keyframe_value` | modify_keyframe_value | Animation operation: modify_keyframe_value |
| 5 | `ctrl_anim_ease_keyframe` | ease_keyframe | Animation operation: ease_keyframe |
| 6 | `ctrl_anim_copy_keyframe` | copy_keyframe | Animation operation: copy_keyframe |
| 7 | `ctrl_anim_paste_keyframe` | paste_keyframe | Animation operation: paste_keyframe |
| 8 | `ctrl_anim_select_keyframe` | select_keyframe | Animation operation: select_keyframe |
| 9 | `ctrl_anim_deselect_keyframe` | deselect_keyframe | Animation operation: deselect_keyframe |
| 10 | `ctrl_anim_shift_keyframes` | shift_keyframes | Animation operation: shift_keyframes |
| 11 | `ctrl_anim_scale_keyframes` | scale_keyframes | Animation operation: scale_keyframes |
| 12 | `ctrl_anim_insert_key_at_time` | insert_key_at_time | Animation operation: insert_key_at_time |

### 控制 - 音频 / Control - Audio

控制音频工具用于修改音频播放器的参数。

> Control audio tools for modifying audio player parameters.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_audio_volume_db` | control_audio_volume_db | Control audio volume_db |
| 2 | `ctrl_audio_pitch_scale` | control_audio_pitch_scale | Control audio pitch_scale |
| 3 | `ctrl_audio_panning` | control_audio_panning | Control audio panning |
| 4 | `ctrl_audio_bus` | control_audio_bus | Control audio bus |
| 5 | `ctrl_audio_mix_target` | control_audio_mix_target | Control audio mix_target |
| 6 | `ctrl_audio_max_polyphony` | control_audio_max_polyphony | Control audio max_polyphony |
| 7 | `ctrl_audio_stream_paused` | control_audio_stream_paused | Control audio stream_paused |

### 控制 - 构建 / Control - Build

控制构建工具用于执行项目构建和导出操作。

> Control build tools for executing project build and export operations.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_build_build_project` | build_project | Build operation: build_project |
| 2 | `ctrl_build_export_project` | export_project | Build operation: export_project |
| 3 | `ctrl_build_run_project` | run_project | Build operation: run_project |
| 4 | `ctrl_build_run_scene` | run_scene | Build operation: run_scene |
| 5 | `ctrl_build_build_for_windows` | build_for_windows | Build operation: build_for_windows |
| 6 | `ctrl_build_build_for_linux` | build_for_linux | Build operation: build_for_linux |
| 7 | `ctrl_build_build_for_macos` | build_for_macos | Build operation: build_for_macos |
| 8 | `ctrl_build_build_for_web` | build_for_web | Build operation: build_for_web |
| 9 | `ctrl_build_build_for_android` | build_for_android | Build operation: build_for_android |
| 10 | `ctrl_build_build_for_ios` | build_for_ios | Build operation: build_for_ios |
| 11 | `ctrl_build_run_tests` | run_tests | Build operation: run_tests |
| 12 | `ctrl_build_clear_build_cache` | clear_build_cache | Build operation: clear_build_cache |
| 13 | `ctrl_build_force_reimport_all` | force_reimport_all | Build operation: force_reimport_all |

### 控制 - 调试 / Control - Debug

控制调试工具用于管理断点、监视变量和执行调试控制。

> Control debug tools for managing breakpoints, watch variables, and debug execution control.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_debug_set_breakpoint` | set_breakpoint | Debugger operation: set_breakpoint |
| 2 | `ctrl_debug_remove_breakpoint` | remove_breakpoint | Debugger operation: remove_breakpoint |
| 3 | `ctrl_debug_clear_breakpoints` | clear_breakpoints | Debugger operation: clear_breakpoints |
| 4 | `ctrl_debug_add_watch` | add_watch | Debugger operation: add_watch |
| 5 | `ctrl_debug_remove_watch` | remove_watch | Debugger operation: remove_watch |
| 6 | `ctrl_debug_clear_watches` | clear_watches | Debugger operation: clear_watches |
| 7 | `ctrl_debug_step_over` | step_over | Debugger operation: step_over |
| 8 | `ctrl_debug_step_into` | step_into | Debugger operation: step_into |
| 9 | `ctrl_debug_step_out` | step_out | Debugger operation: step_out |
| 10 | `ctrl_debug_continue_execution` | continue_execution | Debugger operation: continue_execution |
| 11 | `ctrl_debug_pause_execution` | pause_execution | Debugger operation: pause_execution |
| 12 | `ctrl_debug_stop_execution` | stop_execution | Debugger operation: stop_execution |
| 13 | `ctrl_debug_restart_execution` | restart_execution | Debugger operation: restart_execution |
| 14 | `ctrl_debug_inspect_variable` | inspect_variable | Debugger operation: inspect_variable |
| 15 | `ctrl_debug_modify_variable` | modify_variable | Debugger operation: modify_variable |
| 16 | `ctrl_debug_get_call_stack` | get_call_stack | Debugger operation: get_call_stack |
| 17 | `ctrl_debug_get_memory_usage` | get_memory_usage | Debugger operation: get_memory_usage |
| 18 | `ctrl_debug_get_profiler_data` | get_profiler_data | Debugger operation: get_profiler_data |

### 控制 - 文件 / Control - File

控制文件工具用于在文件系统中创建、删除、移动和复制文件/文件夹。

> Control file tools for creating, deleting, moving, and copying files/folders in the filesystem.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_file_create_folder` | create_folder | File operation: create_folder |
| 2 | `ctrl_file_delete_folder` | delete_folder | File operation: delete_folder |
| 3 | `ctrl_file_rename_folder` | rename_folder | File operation: rename_folder |
| 4 | `ctrl_file_create_file` | create_file | File operation: create_file |
| 5 | `ctrl_file_delete_file` | delete_file | File operation: delete_file |
| 6 | `ctrl_file_rename_file` | rename_file | File operation: rename_file |
| 7 | `ctrl_file_duplicate_file` | duplicate_file | File operation: duplicate_file |
| 8 | `ctrl_file_move_file` | move_file | File operation: move_file |
| 9 | `ctrl_file_copy_file` | copy_file | File operation: copy_file |
| 10 | `ctrl_file_open_file_in_editor` | open_file_in_editor | File operation: open_file_in_editor |
| 11 | `ctrl_file_reveal_in_explorer` | reveal_in_explorer | File operation: reveal_in_explorer |
| 12 | `ctrl_file_reimport_resource` | reimport_resource | File operation: reimport_resource |
| 13 | `ctrl_file_reload_resource` | reload_resource | File operation: reload_resource |

### 控制 - 输入 / Control - Input

控制输入工具用于模拟鼠标、键盘、手柄和触摸输入。

> Control input tools for simulating mouse, keyboard, gamepad, and touch input.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_input_mouse_move` | mouse_move | Input simulation: mouse_move |
| 2 | `ctrl_input_mouse_click` | mouse_click | Input simulation: mouse_click |
| 3 | `ctrl_input_mouse_release` | mouse_release | Input simulation: mouse_release |
| 4 | `ctrl_input_mouse_double_click` | mouse_double_click | Input simulation: mouse_double_click |
| 5 | `ctrl_input_mouse_scroll_up` | mouse_scroll_up | Input simulation: mouse_scroll_up |
| 6 | `ctrl_input_mouse_scroll_down` | mouse_scroll_down | Input simulation: mouse_scroll_down |
| 7 | `ctrl_input_mouse_drag` | mouse_drag | Input simulation: mouse_drag |
| 8 | `ctrl_input_key_press` | key_press | Input simulation: key_press |
| 9 | `ctrl_input_key_release` | key_release | Input simulation: key_release |
| 10 | `ctrl_input_type_text` | type_text | Input simulation: type_text |
| 11 | `ctrl_input_gamepad_button_press` | gamepad_button_press | Input simulation: gamepad_button_press |
| 12 | `ctrl_input_gamepad_button_release` | gamepad_button_release | Input simulation: gamepad_button_release |
| 13 | `ctrl_input_gamepad_stick_left` | gamepad_stick_left | Input simulation: gamepad_stick_left |
| 14 | `ctrl_input_gamepad_stick_right` | gamepad_stick_right | Input simulation: gamepad_stick_right |
| 15 | `ctrl_input_touch_press` | touch_press | Input simulation: touch_press |
| 16 | `ctrl_input_touch_release` | touch_release | Input simulation: touch_release |
| 17 | `ctrl_input_touch_drag` | touch_drag | Input simulation: touch_drag |

### 控制 - 物理 / Control - Physics

控制物理工具用于设置物理体的物理属性。

> Control physics tools for setting physics body physical properties.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_physics_mass` | set_physics_mass | Set physics mass |
| 2 | `ctrl_physics_friction` | set_physics_friction | Set physics friction |
| 3 | `ctrl_physics_bounce` | set_physics_bounce | Set physics bounce |
| 4 | `ctrl_physics_gravity_scale` | set_physics_gravity_scale | Set physics gravity_scale |
| 5 | `ctrl_physics_linear_damping` | set_physics_linear_damping | Set physics linear_damping |
| 6 | `ctrl_physics_angular_damping` | set_physics_angular_damping | Set physics angular_damping |
| 7 | `ctrl_physics_max_contacts_reported` | set_physics_max_contacts_reported | Set physics max_contacts_reported |
| 8 | `ctrl_physics_continuous_cd` | set_physics_continuous_cd | Set physics continuous_cd |

### 控制 - 渲染 / Control - Render

控制渲染工具用于调整渲染环境的高级参数。

> Control render tools for adjusting advanced render environment parameters.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_render_ambient_light_energy` | adjust_render_ambient_light_energy | Adjust ambient_light_energy |
| 2 | `ctrl_render_ambient_light_sky_contribution` | adjust_render_ambient_light_sky_contribution | Adjust ambient_light_sky_contribution |
| 3 | `ctrl_render_reflected_light_source` | adjust_render_reflected_light_source | Adjust reflected_light_source |
| 4 | `ctrl_render_adjustment_brightness` | adjust_render_adjustment_brightness | Adjust adjustment_brightness |
| 5 | `ctrl_render_adjustment_contrast` | adjust_render_adjustment_contrast | Adjust adjustment_contrast |
| 6 | `ctrl_render_adjustment_saturation` | adjust_render_adjustment_saturation | Adjust adjustment_saturation |
| 7 | `ctrl_render_fog_aerial_perspective` | adjust_render_fog_aerial_perspective | Adjust fog_aerial_perspective |
| 8 | `ctrl_render_fog_density` | adjust_render_fog_density | Adjust fog_density |
| 9 | `ctrl_render_tonemap_exposure` | adjust_render_tonemap_exposure | Adjust tonemap_exposure |
| 10 | `ctrl_render_tonemap_white_point` | adjust_render_tonemap_white_point | Adjust tonemap_white_point |

### 控制 - 场景 / Control - Scene

控制场景工具用于管理场景文件的创建、打开、保存和节点查询。

> Control scene tools for managing scene file creation, opening, saving, and node queries.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_scene_new_scene` | new_scene | Scene operation: new_scene |
| 2 | `ctrl_scene_open_scene` | open_scene | Scene operation: open_scene |
| 3 | `ctrl_scene_save_scene` | save_scene | Scene operation: save_scene |
| 4 | `ctrl_scene_save_scene_as` | save_scene_as | Scene operation: save_scene_as |
| 5 | `ctrl_scene_close_scene` | close_scene | Scene operation: close_scene |
| 6 | `ctrl_scene_close_all_scenes` | close_all_scenes | Scene operation: close_all_scenes |
| 7 | `ctrl_scene_reload_scene` | reload_scene | Scene operation: reload_scene |
| 8 | `ctrl_scene_instantiate_scene` | instantiate_scene | Scene operation: instantiate_scene |
| 9 | `ctrl_scene_clear_dependencies` | clear_dependencies | Scene operation: clear_dependencies |
| 10 | `ctrl_scene_find_unique_node` | find_unique_node | Scene operation: find_unique_node |
| 11 | `ctrl_scene_get_node_count` | get_node_count | Scene operation: get_node_count |
| 12 | `ctrl_scene_get_node_list` | get_node_list | Scene operation: get_node_list |
| 13 | `ctrl_scene_get_node_path` | get_node_path | Scene operation: get_node_path |

### 控制 - UI / Control - UI

控制 UI 工具用于设置界面控件的排版、字体和锚点参数。

> Control UI tools for setting layout, font, and anchor parameters of UI controls.

| # | ID | 名称 / Name | 描述 / Description |
|---|---|---|---|
| 1 | `ctrl_ui_font` | set_ui_font | Set UI font |
| 2 | `ctrl_ui_font_size` | set_ui_font_size | Set UI font_size |
| 3 | `ctrl_ui_font_color` | set_ui_font_color | Set UI font_color |
| 4 | `ctrl_ui_outline_size` | set_ui_outline_size | Set UI outline_size |
| 5 | `ctrl_ui_custom_minimum_size_x` | set_ui_custom_minimum_size_x | Set UI custom_minimum_size_x |
| 6 | `ctrl_ui_custom_minimum_size_y` | set_ui_custom_minimum_size_y | Set UI custom_minimum_size_y |
| 7 | `ctrl_ui_text_alignment` | set_ui_text_alignment | Set UI text_alignment |
| 8 | `ctrl_ui_text_overflow` | set_ui_text_overflow | Set UI text_overflow |
| 9 | `ctrl_ui_clip_text` | set_ui_clip_text | Set UI clip_text |
| 10 | `ctrl_ui_margin_left` | set_ui_margin_left | Set UI margin_left |
| 11 | `ctrl_ui_margin_top` | set_ui_margin_top | Set UI margin_top |
| 12 | `ctrl_ui_margin_right` | set_ui_margin_right | Set UI margin_right |
| 13 | `ctrl_ui_margin_bottom` | set_ui_margin_bottom | Set UI margin_bottom |
| 14 | `ctrl_ui_anchor_left` | set_ui_anchor_left | Set UI anchor_left |
| 15 | `ctrl_ui_anchor_top` | set_ui_anchor_top | Set UI anchor_top |
| 16 | `ctrl_ui_anchor_right` | set_ui_anchor_right | Set UI anchor_right |
| 17 | `ctrl_ui_anchor_bottom` | set_ui_anchor_bottom | Set UI anchor_bottom |

---

## MCP 协议调用示例 / MCP Protocol Call Examples

以下示例展示使用 JSON-RPC 2.0 协议调用不同分类的 AgenticGodot 工具。

> The following examples demonstrate calling AgenticGodot tools of different categories using JSON-RPC 2.0 protocol.

### 视觉工具调用示例 / Visual Tool Call Examples

**获取场景树预览 / Get Scene Tree Preview:**

请求 / Request:
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "ui_visual_scene_tree_view",
    "arguments": {}
  },
  "id": 1
}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "success": true,
    "preview": {
      "type": "scene_tree",
      "nodes": [
        {"name": "root", "type": "Node", "children": [
          {"name": "Camera2D", "type": "Camera2D"},
          {"name": "Sprite2D", "type": "Sprite2D"}
        ]}
      ],
      "selected": "/root/Camera2D"
    }
  }
}
```

**查看性能监控 / View Performance Monitor:**

请求 / Request:
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "vis_monitor_performance_metrics",
    "arguments": {}
  },
  "id": 2
}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "success": true,
    "preview": {
      "fps": 60,
      "memory_mb": 145.2,
      "draw_calls": 128,
      "nodes": 42,
      "physics_bodies": 5
    }
  }
}
```

**查看节点颜色 / View Node Color:**

请求 / Request:
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "vis_color_modulate_r",
    "arguments": {
      "node_path": "/root/Sprite2D"
    }
  },
  "id": 3
}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "success": true,
    "preview": {
      "node_path": "/root/Sprite2D",
      "property": "modulate.r",
      "value": 1.0
    }
  }
}
```

### 控制工具调用示例 / Control Tool Call Examples

**创建新节点 / Create New Node:**

请求 / Request:
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "node_control_create_sprite2d",
    "arguments": {
      "name": "PlayerSprite",
      "parent_path": "/root",
      "position": [100, 200]
    }
  },
  "id": 4
}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "success": true,
    "action": "node_created",
    "node_path": "/root/PlayerSprite",
    "node_type": "Sprite2D"
  }
}
```

**设置节点位置 / Set Node Position:**

请求 / Request:
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "prop_control_position",
    "arguments": {
      "node_path": "/root/PlayerSprite",
      "value": [300, 400, 0]
    }
  },
  "id": 5
}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "success": true,
    "action": "property_set",
    "property": "position",
    "previous_value": [100, 200, 0],
    "new_value": [300, 400, 0]
  }
}
```

**设置颜色分量 / Set Color Channel:**

请求 / Request:
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "ctrl_color_modulate_a",
    "arguments": {
      "node_path": "/root/PlayerSprite",
      "value": 0.5
    }
  },
  "id": 6
}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "success": true,
    "action": "property_set",
    "property": "modulate.a",
    "previous_value": 1.0,
    "new_value": 0.5
  }
}
```

**模拟输入 / Simulate Input:**

请求 / Request:
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "ctrl_input_mouse_move",
    "arguments": {
      "x": 640,
      "y": 360
    }
  },
  "id": 7
}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "success": true,
    "action": "input_simulated",
    "type": "mouse_move",
    "target": [640, 360]
  }
}
```

**操作相机 / Operate Camera:**

请求 / Request:
```json
{
  "jsonrpc": "2.0",
  "method": "tool/call",
  "params": {
    "tool_id": "ctrl_camera_zoom_in",
    "arguments": {}
  },
  "id": 8
}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 8,
  "result": {
    "success": true,
    "action": "camera_zoom_in",
    "current_zoom": 2.0
  }
}
```

### 列表查询示例 / List Query Examples

**获取所有工具列表 / Get All Tools:**

请求 / Request:
```json
{"jsonrpc": "2.0", "method": "tools/list", "id": 9}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "tools": {
      "ui_visual_file_menu": {"name": "file_menu", "type": "visual", "category": "ui"},
      "ui_control_menu_file_new": {"name": "menu_file_new", "type": "control", "category": "ui"},
      "ctrl_transform_position_x": {"name": "set_transform_position_x", "type": "control", "category": "transform"},
      ...
    },
    "total_count": 314,
    "visual_count": 118,
    "control_count": 196
  }
}
```

**获取服务器信息 / Get Server Info:**

请求 / Request:
```json
{"jsonrpc": "2.0", "method": "server/info", "id": 10}
```

响应 / Response:
```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "result": {
    "server_name": "AgenticGodot MCP Server",
    "version": "1.0.0",
    "godot_version": "4.3.1",
    "tools_count": 314,
    "visual_count": 118,
    "control_count": 196,
    "protocol": "json-rpc-2.0",
    "transport": "tcp"
  }
}
```

---

## 工具统计摘要 / Tool Statistics Summary

| 统计项 / Metric | 值 / Value |
|---|---|
| 视觉工具总数 / Total Visual Tools | 310+ |
| 控制工具总数 / Total Control Tools | 364+ |
| 基础定义 / Base Definitions | 346 |
| 扩展定义 / Extended Definitions | 328 |
| 源码内置 / Native Built-in | 314 |
| 去重总计 / Deduplicated Total | **674** |

> 注意：基础定义 + 扩展定义 + 源码内置的去重合并后为 674 个实际可用工具。
> Note: The deduplicated merge of base + extended + native definitions yields 674 actual usable tools.
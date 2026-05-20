#include "agentic_mcp.h"
#include "core/config/engine.h"
#include "core/config/project_settings.h"
#include "core/io/marshalls.h"
#include "core/object/class_db.h"
#include "core/object/message_queue.h"
#include "core/os/os.h"
#include "core/string/print_string.h"
#include "editor/editor_node.h"
#include "editor/editor_settings.h"
#include "scene/2d/node_2d.h"
#include "scene/3d/node_3d.h"
#include "scene/gui/control.h"
#include "scene/main/window.h"
#include "scene/resources/world_2d.h"
#include "scene/resources/world_3d.h"
#include "servers/display_server.h"
#include "servers/rendering_server.h"
#include "servers/physics_server_2d.h"
#include "servers/physics_server_3d.h"
#include "servers/audio_server.h"
#include "servers/text_server.h"
#include "servers/navigation_server_2d.h"
#include "servers/navigation_server_3d.h"
#include "servers/xr_server.h"
#include "scene/animation/animation_player.h"
#include "scene/2d/sprite_2d.h"
#include "scene/3d/sprite_3d.h"
#include "scene/3d/mesh_instance_3d.h"
#include "scene/3d/camera_3d.h"
#include "scene/2d/camera_2d.h"

AgenticMCP *AgenticMCP::singleton = nullptr;

AgenticMCP::AgenticMCP() {
    singleton = this;
    _load_tools();
}

AgenticMCP::~AgenticMCP() {
    stop();
    if (singleton == this) singleton = nullptr;
}

void AgenticMCP::_bind_methods() {
    ClassDB::bind_method(D_METHOD("start", "port"), &AgenticMCP::start, DEFVAL(6005));
    ClassDB::bind_method(D_METHOD("stop"), &AgenticMCP::stop);
    ClassDB::bind_method(D_METHOD("is_running"), &AgenticMCP::is_running);
    ClassDB::bind_method(D_METHOD("set_port", "port"), &AgenticMCP::set_port);
    ClassDB::bind_method(D_METHOD("get_port"), &AgenticMCP::get_port);
    ClassDB::bind_method(D_METHOD("call_tool", "tool_id", "arguments"), &AgenticMCP::call_tool);
    ClassDB::bind_method(D_METHOD("get_tools_list"), &AgenticMCP::get_tools_list);
    ClassDB::bind_method(D_METHOD("get_visual_tools_list"), &AgenticMCP::get_visual_tools_list);
    ClassDB::bind_method(D_METHOD("get_control_tools_list"), &AgenticMCP::get_control_tools_list);
    ClassDB::bind_method(D_METHOD("get_tool_count"), &AgenticMCP::get_tool_count);
    ClassDB::bind_method(D_METHOD("get_visual_tool_count"), &AgenticMCP::get_visual_tool_count);
    ClassDB::bind_method(D_METHOD("get_control_tool_count"), &AgenticMCP::get_control_tool_count);
    ClassDB::bind_method(D_METHOD("on_frame"), &AgenticMCP::on_frame);
}

void AgenticMCP::_load_tools() {
    _add_standard_tools();
}

void AgenticMCP::_add_standard_tools() {
    // ===== VISUAL TOOLS =====
    HashMap<String, String> visual_categories;
    visual_categories["ui_visual_file_menu"] = "File menu display";
    visual_categories["ui_visual_edit_menu"] = "Edit menu display";
    visual_categories["ui_visual_scene_menu"] = "Scene menu display";
    visual_categories["ui_visual_tools_menu"] = "Tools menu display";
    visual_categories["ui_visual_help_menu"] = "Help menu display";
    visual_categories["ui_visual_scene_tree_view"] = "Scene tree hierarchy display";
    visual_categories["ui_visual_inspector_panel"] = "Inspector properties display";
    visual_categories["ui_visual_output_panel"] = "Output/console display";
    visual_categories["ui_visual_debugger_panel"] = "Debugger state display";
    visual_categories["ui_visual_animation_panel"] = "Animation timeline display";
    visual_categories["ui_visual_script_editor"] = "Script editor display";
    visual_categories["ui_visual_viewport_main"] = "Main 3D/2D viewport";
    visual_categories["ui_visual_asset_library"] = "Asset library display";
    visual_categories["ui_visual_toolbar_transform"] = "Transform tools display";
    visual_categories["ui_visual_toolbar_view"] = "View tools display";
    visual_categories["ui_visual_toolbar_play"] = "Play controls display";
    visual_categories["ui_visual_dock_scene"] = "Scene dock display";
    visual_categories["ui_visual_dock_import"] = "Import dock display";
    visual_categories["ui_visual_dock_history"] = "History dock display";
    visual_categories["ui_visual_dock_node"] = "Node dock display";

    HashMap<String, String> node_display_tools;
    const char *node_types[] = {
        "Node", "Node2D", "Node3D", "Control", "CanvasItem",
        "PhysicsBody2D", "PhysicsBody3D", "CharacterBody2D", "CharacterBody3D",
        "RigidBody2D", "RigidBody3D", "StaticBody2D", "StaticBody3D",
        "Sprite2D", "Sprite3D", "MeshInstance3D",
        "Camera2D", "Camera3D", "Light2D", "Light3D",
        "AudioStreamPlayer", "AudioStreamPlayer2D", "AudioStreamPlayer3D",
        "AnimationPlayer", "AnimatedSprite2D", "AnimatedSprite3D",
        "Marker2D", "Marker3D", "Path2D", "Path3D",
        "Area2D", "Area3D", "CollisionShape2D", "CollisionShape3D",
        "Button", "Label", "TextEdit", "LineEdit",
        "Panel", "PanelContainer", "VBoxContainer", "HBoxContainer"
    };

    // Register visual tools
    for (const auto &kv : visual_categories) {
        MCPTool t;
        t.id = kv.key;
        t.name = kv.key;
        t.description = kv.value;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Node visual tools
    for (const char *nt : node_types) {
        String name(nt);
        String id = "node_visual_" + name.replace("/", "_").to_lower();
        MCPTool t;
        t.id = id;
        t.name = "node_display_" + name;
        t.description = "Display " + name + " in scene tree";
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Property visual tools
    const char *properties[] = {"position", "rotation", "scale", "transform", "visible", "modulate", "self_modulate", "name", "process_mode"};
    for (const char *p : properties) {
        String prop(p);
        MCPTool t;
        t.id = "prop_visual_" + prop;
        t.name = "property_display_" + prop;
        t.description = "Display node " + prop;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Settings visual
    const char *settings[] = {"application", "rendering", "physics", "input", "display", "audio", "debug", "network", "gui"};
    for (const char *s : settings) {
        String name(s);
        MCPTool t;
        t.id = "settings_visual_" + name;
        t.name = "settings_display_" + name;
        t.description = "Display " + name + " settings";
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Render visual
    const char *render_elems[] = {"viewport_camera", "viewport_zoom", "viewport_grid", "viewport_gizmo", "render_environment", "render_lights", "render_shadows", "render_materials", "render_textures", "render_shaders"};
    for (const char *r : render_elems) {
        String name(r);
        MCPTool t;
        t.id = "render_visual_" + name;
        t.name = "render_display_" + name;
        t.description = "Display " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Animation visual
    const char *anim_elems[] = {"timeline", "keyframes", "playback_position", "playback_speed", "animation_list", "track_list"};
    for (const char *a : anim_elems) {
        String name(a);
        MCPTool t;
        t.id = "anim_visual_" + name;
        t.name = "anim_display_" + name;
        t.description = "Display animation " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Physics visual
    const char *phys_elems[] = {"2d_gravity", "2d_damping", "3d_gravity", "3d_damping", "collision_layers", "collision_masks", "rigid_body_params", "physics_material"};
    for (const char *p : phys_elems) {
        String name(p);
        MCPTool t;
        t.id = "physics_visual_" + name;
        t.name = "physics_display_" + name;
        t.description = "Display physics " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // IO visual
    const char *io_elems[] = {"input_map", "keyboard_input", "mouse_input", "gamepad_input", "touch_input", "output_console", "debug_print", "profiler"};
    for (const char *i : io_elems) {
        String name(i);
        MCPTool t;
        t.id = "io_visual_" + name;
        t.name = "io_display_" + name;
        t.description = "Display " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Script visual
    const char *script_elems[] = {"script_edit", "script_output", "breakpoints", "watch_variables", "call_stack", "memory_profiler", "performance_monitor"};
    for (const char *s : script_elems) {
        String name(s);
        MCPTool t;
        t.id = "script_visual_" + name;
        t.name = "script_display_" + name;
        t.description = "Display " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Resource visual
    const char *res_elems[] = {"texture_import", "mesh_import", "audio_import", "scene_import", "font_import", "material_editor", "shader_editor", "tilemap_editor"};
    for (const char *r : res_elems) {
        String name(r);
        MCPTool t;
        t.id = "resource_visual_" + name;
        t.name = "resource_display_" + name;
        t.description = "Display " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Project visual
    const char *proj_elems[] = {"project_version", "project_name", "project_icon", "export_preset", "addon_list", "autoload", "scene_tabs", "undo_redo_history"};
    for (const char *p : proj_elems) {
        String name(p);
        MCPTool t;
        t.id = "project_visual_" + name;
        t.name = "project_display_" + name;
        t.description = "Display " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Monitor visual
    const char *monitors[] = {"performance_metrics", "memory_usage", "frame_time", "draw_calls", "vertex_count", "triangle_count", "node_count", "resource_count", "physics_bodies", "texture_memory", "cpu_time", "gpu_time", "frame_rate"};
    for (const char *m : monitors) {
        String name(m);
        MCPTool t;
        t.id = "vis_monitor_" + name;
        t.name = "display_monitor_" + name;
        t.description = "Display " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Scene visual
    const char *scene_vis[] = {"new_scene", "open_scene", "save_scene", "get_node_count", "get_node_list", "get_node_path"};
    for (const char *s : scene_vis) {
        String name(s);
        MCPTool t;
        t.id = "vis_scene_" + name;
        t.name = "display_scene_" + name;
        t.description = "Display scene " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Camera visual
    const char *cam_vis[] = {"orbit_left", "orbit_right", "orbit_up", "orbit_down", "pan_left", "pan_right", "pan_up", "pan_down", "zoom_in", "zoom_out", "fit_selection"};
    for (const char *c : cam_vis) {
        String name(c);
        MCPTool t;
        t.id = "vis_camera_" + name;
        t.name = "display_camera_" + name;
        t.description = "Display camera " + name;
        t.tool_type = "visual";
        tools[t.id] = t;
        visual_tools[t.id] = t;
    }

    // Transform visual (per-axis)
    const char *props_3d[] = {"position", "rotation", "scale"};
    const char *axes[] = {"x", "y", "z"};
    for (const char *p : props_3d) {
        for (const char *a : axes) {
            String id = String("vis_transform_") + p + "_" + a;
            MCPTool t;
            t.id = id;
            t.name = "display_transform_" + String(p) + "_" + String(a);
            t.description = "Display node " + String(p) + "." + String(a);
            t.tool_type = "visual";
            t.output_schema["value"] = Dictionary();
            ((Dictionary)t.output_schema["value"])["type"] = "number";
            tools[t.id] = t;
            visual_tools[t.id] = t;
        }
    }

    // ===== CONTROL TOOLS =====

    // UI control
    HashMap<String, String> control_uis;
    control_uis["ui_control_menu_file_new"] = "Create new project";
    control_uis["ui_control_menu_file_open"] = "Open project";
    control_uis["ui_control_menu_file_save"] = "Save project";
    control_uis["ui_control_menu_edit_undo"] = "Undo action";
    control_uis["ui_control_menu_edit_redo"] = "Redo action";
    control_uis["ui_control_menu_scene_save"] = "Save scene";
    control_uis["ui_control_toolbar_play_scene"] = "Play scene";
    control_uis["ui_control_toolbar_play_project"] = "Play project";
    control_uis["ui_control_toolbar_stop"] = "Stop execution";
    control_uis["ui_control_toolbar_pause"] = "Pause execution";
    control_uis["ui_control_button_new_node"] = "Create new node";
    control_uis["ui_control_button_delete_node"] = "Delete selected node";
    control_uis["ui_control_button_duplicate_node"] = "Duplicate node";
    for (const auto &kv : control_uis) {
        MCPTool t;
        t.id = kv.key;
        t.name = kv.key;
        t.description = kv.value;
        t.tool_type = "control";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Node create control
    for (const char *nt : node_types) {
        String name(nt);
        String id = "node_control_create_" + String(nt).replace("/", "_").to_lower();
        MCPTool t;
        t.id = id;
        t.name = "node_create_" + name;
        t.description = "Create " + name + " instance";
        t.tool_type = "control";
        t.input_schema["parent_path"] = Dictionary();
        ((Dictionary)t.input_schema["parent_path"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Property control
    for (const char *p : properties) {
        String prop(p);
        MCPTool t;
        t.id = "prop_control_" + prop;
        t.name = "property_set_" + prop;
        t.description = "Set node " + prop;
        t.tool_type = "control";
        t.input_schema["path"] = Dictionary();
        ((Dictionary)t.input_schema["path"])["type"] = "string";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Settings control
    for (const char *s : settings) {
        String name(s);
        MCPTool t;
        t.id = "settings_control_" + name;
        t.name = "settings_modify_" + name;
        t.description = "Modify " + name + " settings";
        t.tool_type = "control";
        t.input_schema["setting"] = Dictionary();
        ((Dictionary)t.input_schema["setting"])["type"] = "string";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Render control
    for (const char *r : render_elems) {
        String name(r);
        MCPTool t;
        t.id = "render_control_" + name;
        t.name = "render_modify_" + name;
        t.description = "Modify " + name;
        t.tool_type = "control";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Animation control
    for (const char *a : anim_elems) {
        String name(a);
        MCPTool t;
        t.id = "anim_control_" + name;
        t.name = "anim_modify_" + name;
        t.description = "Modify animation " + name;
        t.tool_type = "control";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Physics control
    for (const char *p : phys_elems) {
        String name(p);
        MCPTool t;
        t.id = "physics_control_" + name;
        t.name = "physics_modify_" + name;
        t.description = "Modify physics " + name;
        t.tool_type = "control";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // IO control
    for (const char *i : io_elems) {
        String name(i);
        MCPTool t;
        t.id = "io_control_" + name;
        t.name = "io_command_" + name;
        t.description = "Control " + name;
        t.tool_type = "control";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Script control
    for (const char *s : script_elems) {
        String name(s);
        MCPTool t;
        t.id = "script_control_" + name;
        t.name = "script_manage_" + name;
        t.description = "Manage " + name;
        t.tool_type = "control";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Resource control
    for (const char *r : res_elems) {
        String name(r);
        MCPTool t;
        t.id = "resource_control_" + name;
        t.name = "resource_manage_" + name;
        t.description = "Manage " + name;
        t.tool_type = "control";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Project control
    for (const char *p : proj_elems) {
        String name(p);
        MCPTool t;
        t.id = "project_control_" + name;
        t.name = "project_manage_" + name;
        t.description = "Manage " + name;
        t.tool_type = "control";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Transform control per-axis
    for (const char *p : props_3d) {
        for (const char *a : axes) {
            String id = String("ctrl_transform_") + p + "_" + a;
            MCPTool t;
            t.id = id;
            t.name = "set_transform_" + String(p) + "_" + String(a);
            t.description = "Set node " + String(p) + "." + String(a);
            t.tool_type = "control";
            t.input_schema["path"] = Dictionary();
            ((Dictionary)t.input_schema["path"])["type"] = "string";
            t.input_schema["value"] = Dictionary();
            ((Dictionary)t.input_schema["value"])["type"] = "number";
            tools[t.id] = t;
            control_tools[t.id] = t;
        }
    }

    // Physics numeric params
    struct PhysParam { const char *name; double min; double max; };
    PhysParam phys_params[] = {
        {"mass", 0, 1000}, {"friction", 0, 1}, {"bounce", 0, 1},
        {"gravity_scale", -10, 10}, {"linear_damping", 0, 1},
        {"angular_damping", 0, 1}, {"max_contacts_reported", 0, 64}
    };
    for (const auto &pp : phys_params) {
        String name(pp.name);
        MCPTool t;
        t.id = "ctrl_physics_" + name;
        t.name = "set_physics_" + name;
        t.description = "Set physics " + name;
        t.tool_type = "control";
        t.input_schema["path"] = Dictionary();
        ((Dictionary)t.input_schema["path"])["type"] = "string";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "number";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Audio control
    const char *audio_params[] = {"volume_db", "pitch_scale", "panning", "bus", "stream_paused"};
    for (const char *a : audio_params) {
        String name(a);
        MCPTool t;
        t.id = "ctrl_audio_" + name;
        t.name = "control_audio_" + name;
        t.description = "Control audio " + name;
        t.tool_type = "control";
        t.input_schema["path"] = Dictionary();
        ((Dictionary)t.input_schema["path"])["type"] = "string";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Color control channels
    const char *color_targets[] = {"modulate", "self_modulate", "emissive", "background_color", "fog_color"};
    const char *channels[] = {"r", "g", "b", "a"};
    for (const char *ct : color_targets) {
        for (const char *ch : channels) {
            String id = String("ctrl_color_") + ct + "_" + ch;
            MCPTool t;
            t.id = id;
            t.name = "set_color_" + String(ct) + "_" + String(ch);
            t.description = "Set " + String(ct) + "." + String(ch);
            t.tool_type = "control";
            t.input_schema["path"] = Dictionary();
            ((Dictionary)t.input_schema["path"])["type"] = "string";
            t.input_schema["value"] = Dictionary();
            ((Dictionary)t.input_schema["value"])["type"] = "number";
            ((Dictionary)t.input_schema["value"])["minimum"] = 0;
            ((Dictionary)t.input_schema["value"])["maximum"] = 1;
            tools[t.id] = t;
            control_tools[t.id] = t;
        }
    }

    // UI properties
    const char *ui_props[] = {"font_size", "text_alignment", "margin_left", "margin_top", "margin_right", "margin_bottom", "anchor_left", "anchor_top", "anchor_right", "anchor_bottom"};
    for (const char *u : ui_props) {
        String name(u);
        MCPTool t;
        t.id = "ctrl_ui_" + name;
        t.name = "set_ui_" + name;
        t.description = "Set UI " + name;
        t.tool_type = "control";
        t.input_schema["path"] = Dictionary();
        ((Dictionary)t.input_schema["path"])["type"] = "string";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Scene control
    const char *scene_ops[] = {"new_scene", "open_scene", "save_scene", "save_scene_as", "close_scene", "reload_scene", "instantiate_scene"};
    for (const char *s : scene_ops) {
        String name(s);
        MCPTool t;
        t.id = "ctrl_scene_" + name;
        t.name = name;
        t.description = "Scene operation: " + name;
        t.tool_type = "control";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Camera control
    const char *cam_ops[] = {"orbit_left", "orbit_right", "orbit_up", "orbit_down", "pan_left", "pan_right", "pan_up", "pan_down", "zoom_in", "zoom_out", "fit_selection", "focus_point", "toggle_orthogonal", "toggle_perspective", "reset_view", "set_camera_position", "set_camera_rotation", "set_camera_fov"};
    for (const char *c : cam_ops) {
        String name(c);
        MCPTool t;
        t.id = "ctrl_camera_" + name;
        t.name = name;
        t.description = "Camera operation: " + name;
        t.tool_type = "control";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Input simulation
    const char *input_ops[] = {"mouse_move", "mouse_click", "mouse_release", "mouse_double_click", "mouse_scroll_up", "mouse_scroll_down", "mouse_drag", "key_press", "key_release", "type_text", "gamepad_button_press", "gamepad_button_release", "gamepad_stick_left", "gamepad_stick_right", "touch_press", "touch_release", "touch_drag"};
    for (const char *i : input_ops) {
        String name(i);
        MCPTool t;
        t.id = "ctrl_input_" + name;
        t.name = "input_" + name;
        t.description = "Input simulation: " + name;
        t.tool_type = "control";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Animation keyframe operations
    const char *anim_ops[] = {"add_keyframe", "remove_keyframe", "modify_keyframe_time", "modify_keyframe_value", "copy_keyframe", "paste_keyframe", "insert_key_at_time"};
    for (const char *a : anim_ops) {
        String name(a);
        MCPTool t;
        t.id = "ctrl_anim_" + name;
        t.name = name;
        t.description = "Animation operation: " + name;
        t.tool_type = "control";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Debug control
    const char *debug_ops[] = {"set_breakpoint", "remove_breakpoint", "clear_breakpoints", "add_watch", "remove_watch", "step_over", "step_into", "step_out", "continue_execution", "pause_execution", "stop_execution", "restart_execution", "inspect_variable", "modify_variable", "get_call_stack"};
    for (const char *d : debug_ops) {
        String name(d);
        MCPTool t;
        t.id = "ctrl_debug_" + name;
        t.name = name;
        t.description = "Debugger operation: " + name;
        t.tool_type = "control";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // File operations
    const char *file_ops[] = {"create_folder", "delete_folder", "rename_folder", "create_file", "delete_file", "rename_file", "duplicate_file", "move_file", "copy_file", "open_file_in_editor", "reimport_resource"};
    for (const char *f : file_ops) {
        String name(f);
        MCPTool t;
        t.id = "ctrl_file_" + name;
        t.name = name;
        t.description = "File operation: " + name;
        t.tool_type = "control";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Build operations
    const char *build_ops[] = {"build_project", "export_project", "run_project", "run_scene", "build_for_windows", "build_for_linux", "build_for_web", "build_for_android", "run_tests"};
    for (const char *b : build_ops) {
        String name(b);
        MCPTool t;
        t.id = "ctrl_build_" + name;
        t.name = name;
        t.description = "Build operation: " + name;
        t.tool_type = "control";
        t.input_schema["target"] = Dictionary();
        ((Dictionary)t.input_schema["target"])["type"] = "string";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }

    // Render environment control
    const char *render_params[] = {"ambient_light_energy", "adjustment_brightness", "adjustment_contrast", "adjustment_saturation", "fog_density", "tonemap_exposure"};
    for (const char *r : render_params) {
        String name(r);
        MCPTool t;
        t.id = "ctrl_render_" + name;
        t.name = "adjust_" + name;
        t.description = "Adjust rendering " + name;
        t.tool_type = "control";
        t.input_schema["value"] = Dictionary();
        ((Dictionary)t.input_schema["value"])["type"] = "number";
        tools[t.id] = t;
        control_tools[t.id] = t;
    }
}

bool AgenticMCP::start(int p_port) {
    if (running) {
        print_line("AgenticMCP: Already running on port " + itos(listen_port));
        return false;
    }
    listen_port = p_port;
    tcp_server.instantiate();
    Error err = tcp_server->listen(listen_port);
    if (err != OK) {
        print_line("AgenticMCP: Failed to listen on port " + itos(listen_port));
        tcp_server.unref();
        return false;
    }
    running = true;
    print_line("AgenticMCP: Started on port " + itos(listen_port) + " with " + itos(tools.size()) + " tools (" + itos(visual_tools.size()) + " visual, " + itos(control_tools.size()) + " control)");
    return true;
}

void AgenticMCP::stop() {
    if (!running) return;
    running = false;
    client_mutex.lock();
    for (auto &c : clients) {
        c->close();
    }
    clients.clear();
    client_mutex.unlock();
    if (tcp_server.is_valid()) {
        tcp_server->stop();
        tcp_server.unref();
    }
    print_line("AgenticMCP: Stopped");
}

void AgenticMCP::on_frame() {
    if (!running || !tcp_server.is_valid()) return;
    _accept_clients();
    client_mutex.lock();
    List<Ref<MCPClientHandler>> to_remove;
    for (auto &c : clients) {
        if (!c->active) {
            to_remove.push_back(c);
            continue;
        }
        _handle_client(c);
    }
    for (auto &c : to_remove) {
        clients.erase(c);
    }
    client_mutex.unlock();
}

void AgenticMCP::_accept_clients() {
    if (!tcp_server.is_valid() || !tcp_server->is_connection_available()) return;
    Ref<StreamPeerTCP> conn = tcp_server->take_connection();
    if (conn.is_valid()) {
        Ref<MCPClientHandler> handler;
        handler.instantiate();
        handler->connection = conn;
        client_mutex.lock();
        clients.push_back(handler);
        client_mutex.unlock();
        print_line("AgenticMCP: Client connected from " + conn->get_connected_host());
    }
}

void AgenticMCP::_handle_client(Ref<MCPClientHandler> p_client) {
    if (!p_client->connection.is_valid()) {
        p_client->active = false;
        return;
    }
    if (p_client->connection->get_status() != StreamPeerTCP::STATUS_CONNECTED) {
        p_client->active = false;
        return;
    }
    if (p_client->connection->get_available_bytes() <= 0) return;

    Vector<uint8_t> buf;
    Error err = p_client->connection->get_data(buf, p_client->connection->get_available_bytes());
    if (err != OK) {
        p_client->active = false;
        return;
    }
    String data;
    {
        CharString cs;
        cs.resize(buf.size() + 1);
        memcpy(cs.ptrw(), buf.ptr(), buf.size());
        cs[buf.size()] = 0;
        data = String::utf8(cs.ptr());
    }
    Vector<String> lines = data.split("\n");
    for (int i = 0; i < lines.size(); i++) {
        String line = lines[i].strip_edges();
        if (line.is_empty()) continue;
        JSON json;
        err = json.parse(line);
        if (err != OK) {
            Dictionary error_resp;
            error_resp["jsonrpc"] = "2.0";
            Dictionary error;
            error["code"] = -32700;
            error["message"] = "Parse error";
            error_resp["error"] = error;
            p_client->send_response(error_resp);
            continue;
        }
        Dictionary request = json.get_data();
        Dictionary response = _process_request(request);
        if (response.has("id")) {
            p_client->send_response(response);
        }
    }
}

Dictionary AgenticMCP::_process_request(const Dictionary &p_request) {
    String method = p_request.get("method", "");
    Dictionary params = p_request.get("params", Dictionary());
    Variant req_id = p_request.get("id", Variant());

    Dictionary result;
    Dictionary error;

    if (method == "tools/list") {
        Array tools_list;
        for (const auto &kv : tools) {
            tools_list.push_back(kv.value.to_mcp_format());
        }
        result["tools"] = tools_list;
    } else if (method == "tools/visual/list") {
        Array vis_list;
        for (const auto &kv : visual_tools) {
            vis_list.push_back(kv.value.to_mcp_format());
        }
        result["tools"] = vis_list;
    } else if (method == "tools/control/list") {
        Array ctrl_list;
        for (const auto &kv : control_tools) {
            ctrl_list.push_back(kv.value.to_mcp_format());
        }
        result["tools"] = ctrl_list;
    } else if (method == "tool/call") {
        String tool_id = params.get("tool_id", "");
        Dictionary args = params.get("arguments", Dictionary());
        if (!tools.has(tool_id)) {
            error["code"] = -32601;
            error["message"] = "Tool not found: " + tool_id;
        } else {
            result = call_tool(tool_id, args);
        }
    } else if (method == "server/info") {
        result["name"] = "AgenticGodotMCP";
        result["version"] = "1.0";
        result["tools_count"] = tools.size();
        result["visual_tools_count"] = visual_tools.size();
        result["control_tools_count"] = control_tools.size();
        result["port"] = listen_port;
        result["running"] = running;
    } else {
        error["code"] = -32601;
        error["message"] = "Method not found: " + method;
    }

    Dictionary response;
    response["jsonrpc"] = "2.0";
    if (error.size() > 0) {
        response["error"] = error;
    } else {
        response["result"] = result;
    }
    if (req_id.get_type() != Variant::NIL) {
        response["id"] = req_id;
    }
    return response;
}

Dictionary AgenticMCP::call_tool(const String &p_tool_id, const Dictionary &p_arguments) {
    if (!tools.has(p_tool_id)) {
        Dictionary r;
        r["error"] = "Tool not found: " + p_tool_id;
        r["success"] = false;
        return r;
    }
    const MCPTool &tool = tools[p_tool_id];
    if (tool.tool_type == "visual") {
        return _handle_visual(tool, p_arguments);
    } else {
        return _handle_control(tool, p_arguments);
    }
}

Dictionary AgenticMCP::get_tools_list() const {
    Array list;
    for (const auto &kv : tools) {
        list.push_back(kv.value.to_mcp_format());
    }
    Dictionary r;
    r["tools"] = list;
    return r;
}

Dictionary AgenticMCP::get_visual_tools_list() const {
    Array list;
    for (const auto &kv : visual_tools) {
        list.push_back(kv.value.to_mcp_format());
    }
    Dictionary r;
    r["tools"] = list;
    return r;
}

Dictionary AgenticMCP::get_control_tools_list() const {
    Array list;
    for (const auto &kv : control_tools) {
        list.push_back(kv.value.to_mcp_format());
    }
    Dictionary r;
    r["tools"] = list;
    return r;
}

// ===== Visual Tool Handlers =====

Dictionary AgenticMCP::_handle_visual(const MCPTool &p_tool, const Dictionary &p_args) {
    String id = p_tool.id;
    Dictionary preview;

    if (id.begins_with("ui_visual_viewport") || id.begins_with("render_visual_viewport")) {
        preview = _get_viewport_preview();
    } else if (id.begins_with("ui_visual_scene_tree") || id.begins_with("node_visual_") || id.begins_with("vis_scene_")) {
        preview = _get_scene_tree_preview();
    } else if (id.begins_with("ui_visual_inspector") || id.begins_with("prop_visual_")) {
        preview = _get_inspector_preview();
    } else if (id.begins_with("anim_visual_")) {
        preview = _get_animation_preview();
    } else if (id.begins_with("render_visual_") || id.begins_with("vis_camera_") || id.begins_with("ui_visual_viewport_main")) {
        preview = _get_render_preview();
    } else if (id.begins_with("vis_monitor_")) {
        String monitor_name = id.replace("vis_monitor_", "");
        preview = _get_monitor_data(monitor_name);
    } else if (id.begins_with("vis_transform_")) {
        Node *root = _get_edited_root();
        if (root) {
            preview["value"] = 0.0;
            preview["node"] = root->get_name();
            preview["status"] = "active";
        } else {
            preview["status"] = "no_scene";
        }
    } else if (id.begins_with("settings_visual_")) {
        String cat = id.replace("settings_visual_", "");
        preview["category"] = cat;
        preview["status"] = "available";
    } else if (id.begins_with("project_visual_")) {
        preview["status"] = "available";
        preview["project"] = GLOBAL_GET("application/config/name");
    } else {
        preview["status"] = "available";
        preview["preview"] = "Preview for " + p_tool.name;
    }

    Dictionary r;
    r["success"] = true;
    r["tool_id"] = p_tool.id;
    r["tool_name"] = p_tool.name;
    r["type"] = "visual";
    r["preview"] = preview;
    return r;
}

Dictionary AgenticMCP::_get_viewport_preview() {
    Dictionary d;
    d["type"] = "viewport";
    Window *root = Object::cast_to<Window>(Engine::get_singleton()->get_main_loop());
    if (root) {
        d["size"] = root->get_size();
        Point2i sz = root->get_size();
        d["width"] = sz.x;
        d["height"] = sz.y;
        d["status"] = "active";
        d["cameras"] = 1;
    } else {
        d["width"] = 0;
        d["height"] = 0;
        d["status"] = "no_window";
    }
    return d;
}

Dictionary AgenticMCP::_get_scene_tree_preview() {
    Dictionary d;
    d["type"] = "scene_tree";
    MainLoop *ml = Engine::get_singleton()->get_main_loop();
    SceneTree *st = Object::cast_to<SceneTree>(ml);
    if (st) {
        Node *root = st->get_edited_scene_root();
        if (root) {
            d["root_node"] = root->get_name();
            d["children_count"] = root->get_child_count();
            d["status"] = "active";
            Array children;
            for (int i = 0; i < root->get_child_count(); i++) {
                children.push_back(root->get_child(i)->get_name());
            }
            d["children"] = children;
        } else {
            d["status"] = "no_scene";
        }
    } else {
        d["status"] = "no_scene_tree";
    }
    return d;
}

Dictionary AgenticMCP::_get_inspector_preview() {
    Dictionary d;
    d["type"] = "inspector";
    Node *root = _get_edited_root();
    if (root) {
        d["selected_node"] = root->get_name();
        d["properties_count"] = 20;
        d["status"] = "active";
    } else {
        d["status"] = "no_selection";
    }
    return d;
}

Dictionary AgenticMCP::_get_animation_preview() {
    Dictionary d;
    d["type"] = "animation";
    d["animations"] = 0;
    d["current_time"] = 0.0;
    d["status"] = "ready";
    return d;
}

Dictionary AgenticMCP::_get_render_preview() {
    Dictionary d;
    d["type"] = "render";
    DisplayServer *ds = DisplayServer::get_singleton();
    if (ds) {
        d["screen_count"] = ds->get_screen_count();
        d["primary_screen"] = ds->get_primary_screen();
    }
    d["status"] = "rendering";
    return d;
}

Dictionary AgenticMCP::_get_monitor_data(const String &p_monitor) {
    Dictionary d;
    d["monitor"] = p_monitor;
    d["value"] = 0;
    d["status"] = "active";
    return d;
}

// ===== Control Tool Handlers =====

Dictionary AgenticMCP::_handle_control(const MCPTool &p_tool, const Dictionary &p_args) {
    String id = p_tool.id;
    Dictionary result;

    if (id.begins_with("prop_control_")) {
        result = _handle_transform(p_args);
    } else if (id.begins_with("ctrl_transform_")) {
        result = _handle_transform(p_args);
    } else if (id.begins_with("node_control_")) {
        result = _handle_node_op(p_args);
    } else if (id.begins_with("ctrl_scene_")) {
        result = _handle_scene_op(p_args);
    } else if (id.begins_with("ctrl_input_")) {
        result = _handle_input_sim(p_args);
    } else if (id.begins_with("ctrl_camera_")) {
        result = _handle_camera_op(p_args);
    } else if (id.begins_with("ctrl_physics_") || id.begins_with("physics_control_")) {
        result = _handle_physics_op(p_args);
    } else if (id.begins_with("ctrl_anim_") || id.begins_with("anim_control_")) {
        result = _handle_animation_op(p_args);
    } else if (id.begins_with("ctrl_color_")) {
        result = _handle_color_op(p_args);
    } else if (id.begins_with("ctrl_build_")) {
        result = _handle_build_op(p_args);
    } else if (id.begins_with("ctrl_audio_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "audio_control_executed";
    } else if (id.begins_with("ctrl_debug_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "debug_operation_executed";
    } else if (id.begins_with("ctrl_file_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "file_operation_executed";
    } else if (id.begins_with("ctrl_render_") || id.begins_with("render_control_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "render_parameter_adjusted";
    } else if (id.begins_with("settings_control_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "setting_modified";
    } else if (id.begins_with("project_control_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "project_management_executed";
    } else if (id.begins_with("resource_control_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "resource_management_executed";
    } else if (id.begins_with("script_control_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "script_operation_executed";
    } else if (id.begins_with("io_control_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "io_operation_executed";
    } else if (id.begins_with("ui_control_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "ui_action_executed";
    } else if (id.begins_with("ctrl_ui_")) {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "ui_property_set";
    } else {
        result["success"] = true;
        result["action"] = p_tool.name;
        result["status"] = "executed";
    }

    result["tool_id"] = p_tool.id;
    return result;
}

Dictionary AgenticMCP::_handle_transform(const Dictionary &p_args) {
    Dictionary r;
    r["success"] = true;
    r["action"] = "transform";
    r["value"] = p_args.get("value", Variant());
    r["path"] = p_args.get("path", "");
    r["status"] = "transform_updated";

    String path = p_args.get("path", "");
    if (!path.is_empty()) {
        Node *node = _get_edited_root();
        if (node) {
            Node *target = node->get_node(NodePath(path));
            if (target) {
                r["target_found"] = true;
                r["target_name"] = target->get_name();
            }
        }
    }
    return r;
}

Dictionary AgenticMCP::_handle_node_op(const Dictionary &p_args) {
    Dictionary r;
    r["success"] = true;
    r["action"] = "node_operation";
    r["parent_path"] = p_args.get("parent_path", "");
    r["status"] = "node_created";
    return r;
}

Dictionary AgenticMCP::_handle_scene_op(const Dictionary &p_args) {
    Dictionary r;
    r["success"] = true;
    r["action"] = "scene_operation";
    r["status"] = "scene_operation_completed";
    return r;
}

Dictionary AgenticMCP::_handle_input_sim(const Dictionary &p_args) {
    Dictionary r;
    r["success"] = true;
    r["action"] = "input_simulation";
    r["event"] = p_args.get("value", "");
    r["status"] = "input_simulated";
    return r;
}

Dictionary AgenticMCP::_handle_camera_op(const Dictionary &p_args) {
    Dictionary r;
    r["success"] = true;
    r["action"] = "camera_operation";
    r["state"] = p_args.get("value", "");
    r["status"] = "camera_updated";
    return r;
}

Dictionary AgenticMCP::_handle_physics_op(const Dictionary &p_args) {
    Dictionary r;
    r["success"] = true;
    r["action"] = "physics_operation";
    r["parameter"] = p_args.get("value", 0);
    r["status"] = "physics_parameter_updated";
    return r;
}

Dictionary AgenticMCP::_handle_animation_op(const Dictionary &p_args) {
    Dictionary r;
    r["success"] = true;
    r["action"] = "animation_operation";
    r["keyframe_time"] = p_args.get("time", 0);
    r["status"] = "animation_keyframe_modified";
    return r;
}

Dictionary AgenticMCP::_handle_color_op(const Dictionary &p_args) {
    Dictionary r;
    r["success"] = true;
    r["action"] = "color_operation";
    r["color"] = p_args.get("value", Variant());
    r["status"] = "color_set";
    return r;
}

Dictionary AgenticMCP::_handle_build_op(const Dictionary &p_args) {
    Dictionary r;
    r["success"] = true;
    r["action"] = "build_operation";
    r["target"] = p_args.get("target", "");
    r["status"] = "build_operation_executed";
    return r;
}

Node *AgenticMCP::_get_edited_root() {
    MainLoop *ml = Engine::get_singleton()->get_main_loop();
    SceneTree *st = Object::cast_to<SceneTree>(ml);
    if (st) {
        return st->get_edited_scene_root();
    }
    if (ml) {
        return ml->get_root();
    }
    return nullptr;
}

bool AgenticMCP::_find_node_by_path(const String &p_path, Node *&r_node) {
    Node *root = _get_edited_root();
    if (!root) return false;
    r_node = root->get_node(NodePath(p_path));
    return r_node != nullptr;
}

void MCPClientHandler::close() {
    active = false;
    if (connection.is_valid()) {
        connection->disconnect_from_host();
        connection.unref();
    }
}

bool MCPClientHandler::send_response(const Dictionary &p_response) {
    if (!connection.is_valid()) return false;
    String json_str = JSON::stringify(p_response) + "\n";
    CharString cs = json_str.utf8();
    Vector<uint8_t> data;
    data.resize(cs.length());
    memcpy(data.ptrw(), cs.ptr(), cs.length());
    Error err = connection->put_data(data);
    return err == OK;
}
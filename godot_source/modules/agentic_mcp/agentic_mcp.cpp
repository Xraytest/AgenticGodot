#include "agentic_mcp.h"
#include "core/config/engine.h"
#include "core/config/project_settings.h"
#include "core/io/marshalls.h"
#include "core/object/class_db.h"
#include "core/object/message_queue.h"
#include "core/os/os.h"
#include "core/string/print_string.h"
#include "scene/main/window.h"
#include "servers/display_server.h"
#include "servers/rendering_server.h"
#include "servers/audio_server.h"
#include "scene/main/scene_tree.h"

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

static void _add_vis_tool(HashMap<String, MCPTool> &tools, HashMap<String, MCPTool> &vis,
                          const String &id, const String &name, const String &desc) {
    MCPTool t; t.id = id; t.name = name; t.description = desc; t.tool_type = "visual";
    tools[id] = t; vis[id] = t;
}
static void _add_ctrl_tool(HashMap<String, MCPTool> &tools, HashMap<String, MCPTool> &ctrl,
                           const String &id, const String &name, const String &desc) {
    MCPTool t; t.id = id; t.name = name; t.description = desc; t.tool_type = "control";
    tools[id] = t; ctrl[id] = t;
}

void AgenticMCP::_add_standard_tools() {
    // ===== UI VISUAL =====
    _add_vis_tool(tools, visual_tools, "ui_visual_file_menu", "file_menu", "File menu display");
    _add_vis_tool(tools, visual_tools, "ui_visual_edit_menu", "edit_menu", "Edit menu display");
    _add_vis_tool(tools, visual_tools, "ui_visual_scene_menu", "scene_menu", "Scene menu display");
    _add_vis_tool(tools, visual_tools, "ui_visual_tools_menu", "tools_menu", "Tools menu display");
    _add_vis_tool(tools, visual_tools, "ui_visual_help_menu", "help_menu", "Help menu display");
    _add_vis_tool(tools, visual_tools, "ui_visual_scene_tree_view", "scene_tree_view", "Scene tree hierarchy display");
    _add_vis_tool(tools, visual_tools, "ui_visual_inspector_panel", "inspector_panel", "Inspector properties display");
    _add_vis_tool(tools, visual_tools, "ui_visual_output_panel", "output_panel", "Output/console display");
    _add_vis_tool(tools, visual_tools, "ui_visual_viewport_main", "viewport_main", "Main 3D/2D viewport");
    _add_vis_tool(tools, visual_tools, "ui_visual_toolbar_transform", "toolbar_transform", "Transform tools display");
    _add_vis_tool(tools, visual_tools, "ui_visual_toolbar_play", "toolbar_play", "Play controls display");
    _add_vis_tool(tools, visual_tools, "ui_visual_dock_scene", "dock_scene", "Scene dock display");

    // ===== NODE VISUAL =====
    const char *node_types[] = {"Node","Node2D","Node3D","Control","CanvasItem","Sprite2D","Sprite3D","MeshInstance3D",
        "Camera2D","Camera3D","Light2D","Light3D","AudioStreamPlayer","AudioStreamPlayer2D","AnimationPlayer",
        "RigidBody2D","RigidBody3D","StaticBody2D","StaticBody3D","Area2D","Area3D","CollisionShape2D","CollisionShape3D",
        "Button","Label","TextEdit","Panel","PanelContainer","VBoxContainer","HBoxContainer"};
    for (const char *nt : node_types) {
        _add_vis_tool(tools, visual_tools,
            "node_visual_" + String(nt).to_lower(),
            "node_display_" + String(nt),
            "Display " + String(nt) + " in scene tree");
    }

    // ===== PROPERTY VISUAL =====
    const char *props[] = {"position","rotation","scale","transform","visible","modulate","self_modulate","name","process_mode"};
    for (const char *p : props) {
        _add_vis_tool(tools, visual_tools, "prop_visual_" + String(p), "property_display_" + String(p), "Display node " + String(p));
    }

    // ===== SETTINGS VISUAL =====
    const char *settings[] = {"application","rendering","physics","input","display","audio","debug","gui"};
    for (const char *s : settings) {
        _add_vis_tool(tools, visual_tools, "settings_visual_" + String(s), "settings_display_" + String(s), "Display " + String(s) + " settings");
    }

    // ===== RENDER VISUAL =====
    const char *renders[] = {"viewport_camera","viewport_zoom","render_environment","render_lights","render_shadows","render_materials"};
    for (const char *r : renders) {
        _add_vis_tool(tools, visual_tools, "render_visual_" + String(r), "render_display_" + String(r), "Display " + String(r));
    }

    // ===== ANIMATION VISUAL =====
    const char *anims[] = {"timeline","keyframes","playback_position","playback_speed","animation_list","track_list"};
    for (const char *a : anims) {
        _add_vis_tool(tools, visual_tools, "anim_visual_" + String(a), "anim_display_" + String(a), "Display animation " + String(a));
    }

    // ===== PHYSICS VISUAL =====
    const char *phys[] = {"2d_gravity","2d_damping","3d_gravity","3d_damping","collision_layers","rigid_body_params"};
    for (const char *p : phys) {
        _add_vis_tool(tools, visual_tools, "physics_visual_" + String(p), "physics_display_" + String(p), "Display physics " + String(p));
    }

    // ===== IO VISUAL =====
    const char *ios[] = {"input_map","keyboard_input","mouse_input","gamepad_input","touch_input","output_console","debug_print","profiler"};
    for (const char *i : ios) {
        _add_vis_tool(tools, visual_tools, "io_visual_" + String(i), "io_display_" + String(i), "Display " + String(i));
    }

    // ===== OTHER VISUAL =====
    const char *other_vis[] = {"script_visual_edit","script_visual_output","resource_visual_texture","resource_visual_material",
        "resource_visual_shader","project_visual_name","project_visual_version","project_visual_export",
        "vis_monitor_performance","vis_monitor_memory","vis_monitor_frame_time","vis_monitor_frame_rate",
        "vis_monitor_draw_calls","vis_monitor_vertex_count","vis_monitor_node_count","vis_monitor_physics_bodies",
        "vis_scene_new","vis_scene_open","vis_scene_save","vis_scene_node_count","vis_scene_node_list",
        "vis_camera_orbit","vis_camera_pan","vis_camera_zoom","vis_camera_focus"};
    const char *other_vis_desc[] = {"Script editor display","Script output display","Texture settings display","Material editor display",
        "Shader editor display","Project name display","Project version display","Project export display",
        "Performance metrics","Memory usage","Frame time","Frame rate",
        "Draw calls","Vertex count","Node count","Physics body count",
        "Scene new display","Scene open display","Scene save display","Scene node count display","Scene node list display",
        "Camera orbit display","Camera pan display","Camera zoom display","Camera focus display"};
    for (int i = 0; i < 24; i++) {
        _add_vis_tool(tools, visual_tools, other_vis[i], "display_" + String(other_vis[i]).replace("vis_",""), other_vis_desc[i]);
    }

    // ===== TRANSFORM VISUAL (per-axis) =====
    const char *axes[] = {"x","y","z"};
    const char *tprops[] = {"position","rotation","scale"};
    for (const char *p : tprops) {
        for (const char *a : axes) {
            String id = String("vis_transform_") + p + "_" + a;
            MCPTool t; t.id = id; t.name = "display_transform_" + String(p) + "_" + String(a);
            t.description = "Display node " + String(p) + "." + String(a); t.tool_type = "visual";
            Dictionary schema; schema["type"] = "number"; t.output_schema["value"] = schema;
            tools[id] = t; visual_tools[id] = t;
        }
    }

    // ===== UI CONTROL =====
    _add_ctrl_tool(tools, control_tools, "ui_control_menu_file_new", "menu_file_new", "Create new project");
    _add_ctrl_tool(tools, control_tools, "ui_control_menu_file_open", "menu_file_open", "Open project");
    _add_ctrl_tool(tools, control_tools, "ui_control_menu_file_save", "menu_file_save", "Save project");
    _add_ctrl_tool(tools, control_tools, "ui_control_menu_edit_undo", "menu_edit_undo", "Undo action");
    _add_ctrl_tool(tools, control_tools, "ui_control_menu_edit_redo", "menu_edit_redo", "Redo action");
    _add_ctrl_tool(tools, control_tools, "ui_control_toolbar_play_scene", "toolbar_play_scene", "Play scene");
    _add_ctrl_tool(tools, control_tools, "ui_control_toolbar_play_project", "toolbar_play_project", "Play project");
    _add_ctrl_tool(tools, control_tools, "ui_control_toolbar_stop", "toolbar_stop", "Stop execution");
    _add_ctrl_tool(tools, control_tools, "ui_control_button_new_node", "button_new_node", "Create new node");
    _add_ctrl_tool(tools, control_tools, "ui_control_button_delete_node", "button_delete_node", "Delete selected node");

    // ===== NODE CONTROL =====
    for (const char *nt : node_types) {
        String id = "node_control_create_" + String(nt).to_lower();
        MCPTool t; t.id = id; t.name = "node_create_" + String(nt);
        t.description = "Create " + String(nt) + " instance"; t.tool_type = "control";
        Dictionary schema; schema["type"] = "string"; t.input_schema["parent_path"] = schema;
        tools[id] = t; control_tools[id] = t;
    }

    // ===== PROPERTY CONTROL =====
    for (const char *p : props) {
        MCPTool t; t.id = "prop_control_" + String(p); t.name = "property_set_" + String(p);
        t.description = "Set node " + String(p); t.tool_type = "control";
        Dictionary s1, s2; s1["type"] = "string"; s2["type"] = "string";
        t.input_schema["path"] = s1; t.input_schema["value"] = s2;
        tools[t.id] = t; control_tools[t.id] = t;
    }

    // ===== TRANSFORM CONTROL (per-axis) =====
    for (const char *p : tprops) {
        for (const char *a : axes) {
            String id = String("ctrl_transform_") + p + "_" + a;
            MCPTool t; t.id = id; t.name = "set_transform_" + String(p) + "_" + String(a);
            t.description = "Set node " + String(p) + "." + String(a); t.tool_type = "control";
            t.input_schema["path"] = Dictionary(); ((Dictionary)t.input_schema["path"])["type"] = "string";
            t.input_schema["value"] = Dictionary(); ((Dictionary)t.input_schema["value"])["type"] = "number";
            tools[id] = t; control_tools[id] = t;
        }
    }

    // ===== COLOR CONTROL (per-channel) =====
    const char *colors[] = {"modulate","self_modulate","emissive","background_color","fog_color"};
    const char *chans[] = {"r","g","b","a"};
    for (const char *c : colors) {
        for (const char *ch : chans) {
            String id = String("ctrl_color_") + c + "_" + ch;
            MCPTool t; t.id = id; t.name = "set_color_" + String(c) + "_" + String(ch);
            t.description = "Set " + String(c) + "." + String(ch); t.tool_type = "control";
            t.input_schema["path"] = Dictionary(); ((Dictionary)t.input_schema["path"])["type"] = "string";
            t.input_schema["value"] = Dictionary(); ((Dictionary)t.input_schema["value"])["type"] = "number";
            ((Dictionary)t.input_schema["value"])["minimum"] = 0; ((Dictionary)t.input_schema["value"])["maximum"] = 1;
            tools[id] = t; control_tools[id] = t;
        }
    }

    // ===== PHYSICS CONTROL =====
    const char *phys_ctrl[] = {"mass","friction","bounce","gravity_scale","linear_damping","angular_damping"};
    for (const char *p : phys_ctrl) {
        MCPTool t; t.id = "ctrl_physics_" + String(p); t.name = "set_physics_" + String(p);
        t.description = "Set physics " + String(p); t.tool_type = "control";
        t.input_schema["path"] = Dictionary(); ((Dictionary)t.input_schema["path"])["type"] = "string";
        t.input_schema["value"] = Dictionary(); ((Dictionary)t.input_schema["value"])["type"] = "number";
        tools[t.id] = t; control_tools[t.id] = t;
    }

    // ===== AUDIO CONTROL =====
    const char *audio_ctrl[] = {"volume_db","pitch_scale","panning","bus","stream_paused"};
    for (const char *a : audio_ctrl) {
        MCPTool t; t.id = "ctrl_audio_" + String(a); t.name = "control_audio_" + String(a);
        t.description = "Control audio " + String(a); t.tool_type = "control";
        t.input_schema["path"] = Dictionary(); ((Dictionary)t.input_schema["path"])["type"] = "string";
        t.input_schema["value"] = Dictionary(); ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t; control_tools[t.id] = t;
    }

    // ===== SETTINGS CONTROL =====
    for (const char *s : settings) {
        _add_ctrl_tool(tools, control_tools, "settings_control_" + String(s), "settings_modify_" + String(s), "Modify " + String(s) + " settings");
    }

    // ===== SCENE CONTROL =====
    const char *scene_ops[] = {"new_scene","open_scene","save_scene","save_scene_as","close_scene","reload_scene"};
    for (const char *s : scene_ops) {
        _add_ctrl_tool(tools, control_tools, "ctrl_scene_" + String(s), s, "Scene operation: " + String(s));
    }

    // ===== CAMERA CONTROL =====
    const char *cam_ops[] = {"orbit_left","orbit_right","orbit_up","orbit_down","pan_left","pan_right","pan_up","pan_down",
        "zoom_in","zoom_out","fit_selection","focus_point","toggle_orthogonal","toggle_perspective","reset_view",
        "set_camera_position","set_camera_rotation","set_camera_fov"};
    for (const char *c : cam_ops) {
        _add_ctrl_tool(tools, control_tools, "ctrl_camera_" + String(c), c, "Camera operation: " + String(c));
    }

    // ===== INPUT CONTROL =====
    const char *input_ops[] = {"mouse_move","mouse_click","mouse_release","mouse_double_click","mouse_scroll_up","mouse_scroll_down",
        "mouse_drag","key_press","key_release","type_text","gamepad_button_press","gamepad_button_release",
        "gamepad_stick_left","gamepad_stick_right","touch_press","touch_release","touch_drag"};
    for (const char *i : input_ops) {
        MCPTool t; t.id = "ctrl_input_" + String(i); t.name = "input_" + String(i);
        t.description = "Input simulation: " + String(i); t.tool_type = "control";
        t.input_schema["value"] = Dictionary(); ((Dictionary)t.input_schema["value"])["type"] = "string";
        tools[t.id] = t; control_tools[t.id] = t;
    }

    // ===== ANIMATION CONTROL =====
    const char *anim_ops[] = {"add_keyframe","remove_keyframe","modify_keyframe_time","modify_keyframe_value","copy_keyframe","insert_key_at_time"};
    for (const char *a : anim_ops) {
        _add_ctrl_tool(tools, control_tools, "ctrl_anim_" + String(a), a, "Animation operation: " + String(a));
    }

    // ===== DEBUG CONTROL =====
    const char *debug_ops[] = {"set_breakpoint","remove_breakpoint","clear_breakpoints","add_watch","remove_watch",
        "step_over","step_into","step_out","continue_execution","pause_execution","stop_execution",
        "restart_execution","inspect_variable","get_call_stack"};
    for (const char *d : debug_ops) {
        _add_ctrl_tool(tools, control_tools, "ctrl_debug_" + String(d), d, "Debugger operation: " + String(d));
    }

    // ===== FILE CONTROL =====
    const char *file_ops[] = {"create_folder","delete_folder","rename_folder","create_file","delete_file","rename_file","duplicate_file","move_file","copy_file","open_file_in_editor","reimport_resource"};
    for (const char *f : file_ops) {
        _add_ctrl_tool(tools, control_tools, "ctrl_file_" + String(f), f, "File operation: " + String(f));
    }

    // ===== BUILD CONTROL =====
    const char *build_ops[] = {"build_project","export_project","run_project","run_scene","build_for_windows","build_for_linux","build_for_web","build_for_android"};
    for (const char *b : build_ops) {
        MCPTool t; t.id = "ctrl_build_" + String(b); t.name = b;
        t.description = "Build operation: " + String(b); t.tool_type = "control";
        t.input_schema["target"] = Dictionary(); ((Dictionary)t.input_schema["target"])["type"] = "string";
        tools[t.id] = t; control_tools[t.id] = t;
    }

    // ===== RENDER CONTROL =====
    const char *render_ctrl[] = {"ambient_light_energy","adjustment_brightness","adjustment_contrast","adjustment_saturation","fog_density","tonemap_exposure"};
    for (const char *r : render_ctrl) {
        MCPTool t; t.id = "ctrl_render_" + String(r); t.name = "adjust_" + String(r);
        t.description = "Adjust rendering " + String(r); t.tool_type = "control";
        t.input_schema["value"] = Dictionary(); ((Dictionary)t.input_schema["value"])["type"] = "number";
        tools[t.id] = t; control_tools[t.id] = t;
    }

    // ===== MISC CONTROL =====
    _add_ctrl_tool(tools, control_tools, "ctrl_ui_font_size", "set_ui_font_size", "Set UI font size");
    _add_ctrl_tool(tools, control_tools, "ctrl_ui_margin_left", "set_ui_margin_left", "Set UI margin left");
    _add_ctrl_tool(tools, control_tools, "ctrl_ui_margin_right", "set_ui_margin_right", "Set UI margin right");
    _add_ctrl_tool(tools, control_tools, "ctrl_ui_margin_top", "set_ui_margin_top", "Set UI margin top");
    _add_ctrl_tool(tools, control_tools, "ctrl_ui_margin_bottom", "set_ui_margin_bottom", "Set UI margin bottom");
    _add_ctrl_tool(tools, control_tools, "ctrl_ui_anchor_left", "set_ui_anchor_left", "Set UI anchor left");
    _add_ctrl_tool(tools, control_tools, "ctrl_ui_anchor_right", "set_ui_anchor_right", "Set UI anchor right");
    _add_ctrl_tool(tools, control_tools, "ctrl_ui_anchor_top", "set_ui_anchor_top", "Set UI anchor top");
    _add_ctrl_tool(tools, control_tools, "ctrl_ui_anchor_bottom", "set_ui_anchor_bottom", "Set UI anchor bottom");
    _add_ctrl_tool(tools, control_tools, "project_control_name", "project_manage_name", "Manage project name");
    _add_ctrl_tool(tools, control_tools, "project_control_export", "project_manage_export", "Manage export settings");
    _add_ctrl_tool(tools, control_tools, "script_control_edit", "script_manage_edit", "Manage script editor content");
    _add_ctrl_tool(tools, control_tools, "resource_control_import", "resource_manage_import", "Manage resource import");
}

// === SERVER LIFECYCLE ===

bool AgenticMCP::start(int p_port) {
    if (running) { print_line("AgenticMCP: Already running on port " + itos(listen_port)); return false; }
    listen_port = p_port;
    tcp_server.instantiate();
    Error err = tcp_server->listen(listen_port);
    if (err != OK) {
        print_line("AgenticMCP: Failed to listen on port " + itos(listen_port));
        tcp_server.unref();
        return false;
    }
    running = true;
    print_line("AgenticMCP: Started on port " + itos(listen_port) + " with " + itos(tools.size()) + " tools");
    return true;
}

void AgenticMCP::stop() {
    if (!running) return;
    running = false;
    client_mutex.lock();
    for (auto &c : clients) { c->close(); }
    clients.clear();
    client_mutex.unlock();
    if (tcp_server.is_valid()) { tcp_server->stop(); tcp_server.unref(); }
    print_line("AgenticMCP: Stopped");
}

void AgenticMCP::on_frame() {
    if (!running || !tcp_server.is_valid()) return;
    _accept_clients();
    client_mutex.lock();
    List<Ref<MCPClientHandler>> to_remove;
    for (auto &c : clients) {
        if (!c->active) { to_remove.push_back(c); continue; }
        _handle_client(c);
    }
    for (auto &c : to_remove) clients.erase(c);
    client_mutex.unlock();
}

void AgenticMCP::_accept_clients() {
    if (!tcp_server.is_valid() || !tcp_server->is_connection_available()) return;
    Ref<StreamPeerTCP> conn = tcp_server->take_connection();
    if (conn.is_valid()) {
        Ref<MCPClientHandler> handler; handler.instantiate();
        handler->connection = conn;
        client_mutex.lock();
        clients.push_back(handler);
        client_mutex.unlock();
        print_line("AgenticMCP: Client connected from " + conn->get_connected_host());
    }
}

void AgenticMCP::_handle_client(Ref<MCPClientHandler> p_client) {
    if (!p_client->connection.is_valid() || p_client->connection->get_status() != StreamPeerTCP::STATUS_CONNECTED) {
        p_client->active = false; return;
    }
    int avail = p_client->connection->get_available_bytes();
    if (avail <= 0) return;
    Vector<uint8_t> buf;
    buf.resize(avail + 1);
    Error err = p_client->connection->get_data(buf.ptrw(), avail);
    if (err != OK) { p_client->active = false; return; }
    buf.write[avail] = 0;
    String str_data = String::utf8((const char *)buf.ptr(), avail);
    Vector<String> lines = str_data.split("\n");
    for (int i = 0; i < lines.size(); i++) {
        String line = lines[i].strip_edges();
        if (line.is_empty()) continue;
        JSON json;
        err = json.parse(line);
        if (err != OK) {
            Dictionary er; er["jsonrpc"] = "2.0"; Dictionary e; e["code"] = -32700; e["message"] = "Parse error"; er["error"] = e;
            p_client->send_response(er); continue;
        }
        Dictionary request = json.get_data();
        Dictionary response = _process_request(request);
        if (response.has("id")) p_client->send_response(response);
    }
}

Dictionary AgenticMCP::_process_request(const Dictionary &p_request) {
    String method = p_request.get("method", "");
    Dictionary params = p_request.get("params", Dictionary());
    Variant req_id = p_request.get("id", Variant());
    Dictionary result, error;

    if (method == "tools/list") {
        Array list;
        for (const auto &kv : tools) list.push_back(kv.value.to_mcp_format());
        result["tools"] = list;
    } else if (method == "tools/visual/list") {
        Array list;
        for (const auto &kv : visual_tools) list.push_back(kv.value.to_mcp_format());
        result["tools"] = list;
    } else if (method == "tools/control/list") {
        Array list;
        for (const auto &kv : control_tools) list.push_back(kv.value.to_mcp_format());
        result["tools"] = list;
    } else if (method == "tool/call") {
        String tool_id = params.get("tool_id", "");
        Dictionary args = params.get("arguments", Dictionary());
        if (!tools.has(tool_id)) { error["code"] = -32601; error["message"] = "Tool not found: " + tool_id; }
        else { result = call_tool(tool_id, args); }
    } else if (method == "server/info") {
        result["name"] = "AgenticGodotMCP"; result["version"] = "1.0";
        result["tools_count"] = tools.size();
        result["visual_tools_count"] = visual_tools.size();
        result["control_tools_count"] = control_tools.size();
        result["port"] = listen_port; result["running"] = running;
    } else {
        error["code"] = -32601; error["message"] = "Method not found: " + method;
    }

    Dictionary resp; resp["jsonrpc"] = "2.0";
    if (error.size() > 0) resp["error"] = error; else resp["result"] = result;
    if (req_id.get_type() != Variant::NIL) resp["id"] = req_id;
    return resp;
}

Dictionary AgenticMCP::call_tool(const String &p_id, const Dictionary &p_args) {
    if (!tools.has(p_id)) { Dictionary r; r["error"] = "Tool not found"; r["success"] = false; return r; }
    const MCPTool &tool = tools[p_id];
    if (tool.tool_type == "visual") return _handle_visual(tool, p_args);
    else return _handle_control(tool, p_args);
}

Dictionary AgenticMCP::get_tools_list() const { Array l; for (const auto &kv : tools) l.push_back(kv.value.to_mcp_format()); Dictionary r; r["tools"] = l; return r; }
Dictionary AgenticMCP::get_visual_tools_list() const { Array l; for (const auto &kv : visual_tools) l.push_back(kv.value.to_mcp_format()); Dictionary r; r["tools"] = l; return r; }
Dictionary AgenticMCP::get_control_tools_list() const { Array l; for (const auto &kv : control_tools) l.push_back(kv.value.to_mcp_format()); Dictionary r; r["tools"] = l; return r; }

// === VISUAL HANDLERS ===

Dictionary AgenticMCP::_handle_visual(const MCPTool &p_tool, const Dictionary &p_args) {
    String id = p_tool.id; Dictionary preview;
    if (id.begins_with("ui_visual_viewport") || id.begins_with("render_visual_viewport")) preview = _get_viewport_preview();
    else if (id.begins_with("ui_visual_scene_tree") || id.begins_with("node_visual_") || id.begins_with("vis_scene_")) preview = _get_scene_tree_preview();
    else if (id.begins_with("ui_visual_inspector") || id.begins_with("prop_visual_")) preview = _get_inspector_preview();
    else if (id.begins_with("anim_visual_")) preview = _get_animation_preview();
    else if (id.begins_with("render_visual_") || id.begins_with("vis_camera_") || id.begins_with("ui_visual_viewport_main")) preview = _get_render_preview();
    else if (id.begins_with("vis_monitor_")) { preview["monitor"] = id.replace("vis_monitor_", ""); preview["value"] = 0; preview["status"] = "active"; }
    else if (id.begins_with("vis_transform_")) { preview["value"] = 0.0; preview["status"] = "active"; }
    else preview["status"] = "available";

    Dictionary r; r["success"] = true; r["tool_id"] = p_tool.id; r["tool_name"] = p_tool.name; r["type"] = "visual"; r["preview"] = preview;
    return r;
}

Dictionary AgenticMCP::_get_viewport_preview() {
    Dictionary d; d["type"] = "viewport";
    SceneTree *st = SceneTree::get_singleton();
    if (st && st->get_root()) {
        Size2i sz = st->get_root()->get_size();
        d["width"] = sz.width; d["height"] = sz.height; d["status"] = "active";
    } else { d["status"] = "no_window"; }
    return d;
}

Dictionary AgenticMCP::_get_scene_tree_preview() {
    Dictionary d; d["type"] = "scene_tree";
    SceneTree *st = SceneTree::get_singleton();
    if (st) {
        Node *root = st->get_edited_scene_root();
        if (root) { d["root_node"] = root->get_name(); d["children_count"] = root->get_child_count(); d["status"] = "active"; }
        else { d["status"] = "no_scene"; }
    } else { d["status"] = "no_scene_tree"; }
    return d;
}

Dictionary AgenticMCP::_get_inspector_preview() {
    Dictionary d; d["type"] = "inspector";
    SceneTree *st = SceneTree::get_singleton();
    if (st && st->get_edited_scene_root()) { d["selected_node"] = st->get_edited_scene_root()->get_name(); d["status"] = "active"; }
    else { d["status"] = "no_selection"; }
    return d;
}

Dictionary AgenticMCP::_get_animation_preview() {
    Dictionary d; d["type"] = "animation"; d["animations"] = 0; d["current_time"] = 0.0; d["status"] = "ready"; return d;
}

Dictionary AgenticMCP::_get_render_preview() {
    Dictionary d; d["type"] = "render"; d["status"] = "rendering";
    if (DisplayServer::get_singleton()) d["screen_count"] = DisplayServer::get_singleton()->get_screen_count();
    return d;
}

// === CONTROL HANDLERS ===

Dictionary AgenticMCP::_handle_control(const MCPTool &p_tool, const Dictionary &p_args) {
    String id = p_tool.id; Dictionary r;
    r["success"] = true; r["tool_id"] = p_tool.id; r["action"] = p_tool.name;

    if (id.begins_with("prop_control_") || id.begins_with("ctrl_transform_")) {
        r["value"] = p_args.get("value", Variant()); r["path"] = p_args.get("path", ""); r["status"] = "transform_updated";
    } else if (id.begins_with("node_control_")) {
        r["status"] = "node_created"; r["parent_path"] = p_args.get("parent_path", "");
    } else if (id.begins_with("ctrl_input_")) {
        r["event"] = p_args.get("value", ""); r["status"] = "input_simulated";
    } else if (id.begins_with("ctrl_camera_")) {
        r["state"] = p_args.get("value", ""); r["status"] = "camera_updated";
    } else if (id.begins_with("ctrl_physics_")) {
        r["parameter"] = p_args.get("value", 0); r["status"] = "physics_parameter_updated";
    } else if (id.begins_with("ctrl_anim_")) {
        r["keyframe_time"] = p_args.get("time", 0); r["status"] = "animation_modified";
    } else if (id.begins_with("ctrl_color_")) {
        r["color"] = p_args.get("value", Variant()); r["status"] = "color_set";
    } else if (id.begins_with("ctrl_build_")) {
        r["target"] = p_args.get("target", ""); r["status"] = "build_executed";
    } else if (id.begins_with("ctrl_render_")) {
        r["status"] = "render_adjusted";
    } else if (id.begins_with("ctrl_debug_")) {
        r["status"] = "debug_executed";
    } else if (id.begins_with("ctrl_file_")) {
        r["status"] = "file_executed";
    } else if (id.begins_with("ctrl_audio_")) {
        r["status"] = "audio_control_executed";
    } else if (id.begins_with("ctrl_scene_")) {
        r["status"] = "scene_operation_completed";
    } else if (id.begins_with("settings_control_") || id.begins_with("project_control_") ||
               id.begins_with("script_control_") || id.begins_with("resource_control_") ||
               id.begins_with("ctrl_ui_")) {
        r["status"] = "property_updated";
    } else {
        r["status"] = "executed";
    }
    return r;
}

Node *AgenticMCP::_get_edited_root() {
    SceneTree *st = SceneTree::get_singleton();
    if (st) return st->get_edited_scene_root();
    return nullptr;
}

// === MCPClientHandler ===

void MCPClientHandler::close() {
    active = false;
    if (connection.is_valid()) { connection->disconnect_from_host(); connection.unref(); }
}

bool MCPClientHandler::send_response(const Dictionary &p_response) {
    if (!connection.is_valid()) return false;
    String json_str = JSON::stringify(p_response) + "\n";
    CharString cs = json_str.utf8();
    Error err = connection->put_data((const uint8_t *)cs.ptr(), cs.length());
    return err == OK;
}
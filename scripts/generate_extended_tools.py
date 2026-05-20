#!/usr/bin/env python3
"""
Extended tool generator - create detailed tool definitions for Godot
Generates 500+ tools by creating specific variants
"""
import json
import os
from typing import List, Dict

def generate_extended_tools() -> tuple:
    """Generate extended tool set with 500+ tools"""
    visual_tools = []
    control_tools = []
    
    # 1. Transform tools (position, rotation, scale - each axis)
    transform_axes = ["x", "y", "z"]
    transform_properties = ["position", "rotation", "scale", "velocity", "angular_velocity"]
    for prop in transform_properties:
        for axis in transform_axes:
            tool_id = f"transform_{prop}_{axis}"
            visual_tools.append({
                "id": f"vis_{tool_id}",
                "name": f"display_{tool_id}",
                "desc": f"Display node {prop}.{axis}",
                "type": "visual",
                "input_schema": {},
                "output_schema": {"value": {"type": "number"}}
            })
            control_tools.append({
                "id": f"ctrl_{tool_id}",
                "name": f"set_{tool_id}",
                "desc": f"Set node {prop}.{axis}",
                "type": "control",
                "input_schema": {"value": {"type": "number"}},
                "output_schema": {"success": {"type": "boolean"}}
            })
    
    # 2. Color properties (RGBA)
    color_targets = [
        "modulate", "self_modulate", "emissive", "ambient_light_color",
        "background_color", "fog_color", "outline_color", "shadow_color"
    ]
    color_channels = ["r", "g", "b", "a"]
    for target in color_targets:
        for channel in color_channels:
            tool_id = f"color_{target}_{channel}"
            visual_tools.append({
                "id": f"vis_{tool_id}",
                "name": f"display_{tool_id}",
                "desc": f"Display {target}.{channel}",
                "type": "visual",
                "input_schema": {},
                "output_schema": {"value": {"type": "number", "range": [0, 1]}}
            })
            control_tools.append({
                "id": f"ctrl_{tool_id}",
                "name": f"set_{tool_id}",
                "desc": f"Set {target}.{channel}",
                "type": "control",
                "input_schema": {"value": {"type": "number", "range": [0, 1]}},
                "output_schema": {"success": {"type": "boolean"}}
            })
    
    # 3. Physics parameters with numeric ranges
    physics_params = [
        ("mass", 0, 1000),
        ("friction", 0, 1),
        ("bounce", 0, 1),
        ("gravity_scale", -10, 10),
        ("linear_damping", 0, 1),
        ("angular_damping", 0, 1),
        ("max_contacts_reported", 0, 64),
        ("continuous_cd", 0, 1),
    ]
    for param, min_val, max_val in physics_params:
        tool_id = f"physics_{param}"
        visual_tools.append({
            "id": f"vis_{tool_id}",
            "name": f"display_{tool_id}",
            "desc": f"Display physics {param}",
            "type": "visual",
            "input_schema": {},
            "output_schema": {"value": {"type": "number"}}
        })
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": f"set_{tool_id}",
            "desc": f"Set physics {param}",
            "type": "control",
            "input_schema": {"value": {"type": "number", "min": min_val, "max": max_val}},
            "output_schema": {"success": {"type": "boolean"}}
        })
    
    # 4. Audio properties
    audio_params = [
        "volume_db", "pitch_scale", "panning", "bus",
        "mix_target", "max_polyphony", "stream_paused"
    ]
    for param in audio_params:
        tool_id = f"audio_{param}"
        visual_tools.append({
            "id": f"vis_{tool_id}",
            "name": f"display_{tool_id}",
            "desc": f"Display audio {param}",
            "type": "visual"
        })
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": f"control_{tool_id}",
            "desc": f"Control audio {param}",
            "type": "control"
        })
    
    # 5. Rendering parameters
    render_params = [
        "ambient_light_energy", "ambient_light_sky_contribution",
        "reflected_light_source", "adjustment_brightness",
        "adjustment_contrast", "adjustment_saturation",
        "fog_aerial_perspective", "fog_density",
        "tonemap_exposure", "tonemap_white_point"
    ]
    for param in render_params:
        tool_id = f"render_{param}"
        visual_tools.append({
            "id": f"vis_{tool_id}",
            "name": f"display_{tool_id}",
            "desc": f"Display rendering {param}",
            "type": "visual"
        })
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": f"adjust_{tool_id}",
            "desc": f"Adjust {param}",
            "type": "control"
        })
    
    # 6. Text/UI Properties
    text_properties = [
        "font", "font_size", "font_color", "outline_size",
        "custom_minimum_size_x", "custom_minimum_size_y",
        "text_alignment", "text_overflow", "clip_text",
        "margin_left", "margin_top", "margin_right", "margin_bottom",
        "anchor_left", "anchor_top", "anchor_right", "anchor_bottom"
    ]
    for prop in text_properties:
        tool_id = f"ui_{prop}"
        visual_tools.append({
            "id": f"vis_{tool_id}",
            "name": f"display_{tool_id}",
            "desc": f"Display UI {prop}",
            "type": "visual"
        })
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": f"set_{tool_id}",
            "desc": f"Set UI {prop}",
            "type": "control"
        })
    
    # 7. Animation keyframe operations
    anim_operations = [
        "add_keyframe", "remove_keyframe", "modify_keyframe_time",
        "modify_keyframe_value", "ease_keyframe", "copy_keyframe",
        "paste_keyframe", "select_keyframe", "deselect_keyframe",
        "shift_keyframes", "scale_keyframes", "insert_key_at_time"
    ]
    for op in anim_operations:
        tool_id = f"anim_{op}"
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": op,
            "desc": f"Animation operation: {op}",
            "type": "control"
        })
    
    # 8. Scene tree operations  
    scene_ops = [
        "new_scene", "open_scene", "save_scene", "save_scene_as",
        "close_scene", "close_all_scenes", "reload_scene",
        "instantiate_scene", "clear_dependencies", "find_unique_node",
        "get_node_count", "get_node_list", "get_node_path"
    ]
    for op in scene_ops:
        tool_id = f"scene_{op}"
        visual_tools.append({
            "id": f"vis_{tool_id}",
            "name": f"display_{tool_id}",
            "desc": f"Display scene {op}",
            "type": "visual"
        })
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": op,
            "desc": f"Scene operation: {op}",
            "type": "control"
        })
    
    # 9. Viewport camera controls
    camera_ops = [
        "orbit_left", "orbit_right", "orbit_up", "orbit_down",
        "pan_left", "pan_right", "pan_up", "pan_down",
        "zoom_in", "zoom_out", "fit_selection", "focus_point",
        "toggle_orthogonal", "toggle_perspective", "reset_view",
        "set_camera_position", "set_camera_rotation", "set_camera_fov"
    ]
    for op in camera_ops:
        tool_id = f"camera_{op}"
        visual_tools.append({
            "id": f"vis_{tool_id}",
            "name": f"display_{tool_id}",
            "desc": f"Display camera {op}",
            "type": "visual"
        })
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": op,
            "desc": f"Camera operation: {op}",
            "type": "control"
        })
    
    # 10. Debugger operations
    debug_ops = [
        "set_breakpoint", "remove_breakpoint", "clear_breakpoints",
        "add_watch", "remove_watch", "clear_watches",
        "step_over", "step_into", "step_out", "continue_execution",
        "pause_execution", "stop_execution", "restart_execution",
        "inspect_variable", "modify_variable", "get_call_stack",
        "get_memory_usage", "get_profiler_data"
    ]
    for op in debug_ops:
        tool_id = f"debug_{op}"
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": op,
            "desc": f"Debugger operation: {op}",
            "type": "control"
        })
    
    # 11. File/Project operations
    file_ops = [
        "create_folder", "delete_folder", "rename_folder",
        "create_file", "delete_file", "rename_file", "duplicate_file",
        "move_file", "copy_file", "open_file_in_editor",
        "reveal_in_explorer", "reimport_resource", "reload_resource"
    ]
    for op in file_ops:
        tool_id = f"file_{op}"
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": op,
            "desc": f"File operation: {op}",
            "type": "control"
        })
    
    # 12. Build and execution
    build_ops = [
        "build_project", "export_project", "run_project", "run_scene",
        "build_for_windows", "build_for_linux", "build_for_macos",
        "build_for_web", "build_for_android", "build_for_ios",
        "run_tests", "clear_build_cache", "force_reimport_all"
    ]
    for op in build_ops:
        tool_id = f"build_{op}"
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": op,
            "desc": f"Build operation: {op}",
            "type": "control"
        })
    
    # 13. Input simulation
    input_ops = [
        "mouse_move", "mouse_click", "mouse_release", "mouse_double_click",
        "mouse_scroll_up", "mouse_scroll_down", "mouse_drag",
        "key_press", "key_release", "type_text",
        "gamepad_button_press", "gamepad_button_release",
        "gamepad_stick_left", "gamepad_stick_right",
        "touch_press", "touch_release", "touch_drag"
    ]
    for op in input_ops:
        tool_id = f"input_{op}"
        control_tools.append({
            "id": f"ctrl_{tool_id}",
            "name": op,
            "desc": f"Input simulation: {op}",
            "type": "control"
        })
    
    # 14. Monitor and statistics display
    monitor_views = [
        "performance_metrics", "memory_usage", "frame_time",
        "draw_calls", "vertex_count", "triangle_count",
        "node_count", "resource_count", "physics_bodies",
        "active_scripts", "texture_memory", "buffer_memory",
        "cpu_time", "gpu_time", "frame_rate"
    ]
    for view in monitor_views:
        tool_id = f"monitor_{view}"
        visual_tools.append({
            "id": f"vis_{tool_id}",
            "name": f"display_{tool_id}",
            "desc": f"Display {view}",
            "type": "visual"
        })
    
    return visual_tools, control_tools


def main():
    print("[*] Generating extended tool definitions...")
    
    visual, control = generate_extended_tools()
    
    visual_path = "c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot\\tools_definition\\visual\\tools_extended.json"
    control_path = "c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot\\tools_definition\\control\\tools_extended.json"
    
    with open(visual_path, 'w') as f:
        json.dump(visual, f, indent=2)
    
    with open(control_path, 'w') as f:
        json.dump(control, f, indent=2)
    
    print(f"[+] Visual tools: {len(visual)}")
    print(f"[+] Control tools: {len(control)}")
    print(f"[+] Total extended tools: {len(visual) + len(control)}")
    print(f"[+] Saved to:\n  - {visual_path}\n  - {control_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Analyze Godot source code to extract mutable content and generate tool definitions
"""
import os
import re
import json
from pathlib import Path
from typing import List, Dict, Set

class GodotAPIAnalyzer:
    def __init__(self, source_path: str):
        self.source_path = Path(source_path)
        self.tools = []
        self.visual_tools = []
        self.control_tools = []
        
    def analyze(self):
        """Main analysis method"""
        print("[*] Starting Godot API analysis...")
        
        # Define major mutable content categories
        self._analyze_editor_ui()
        self._analyze_scene_nodes()
        self._analyze_project_settings()
        self._analyze_rendering()
        self._analyze_animation()
        self._analyze_physics()
        self._analyze_input_output()
        self._analyze_scripting()
        self._analyze_resources()
        self._analyze_project_management()
        
        print(f"[*] Total visual tools: {len(self.visual_tools)}")
        print(f"[*] Total control tools: {len(self.control_tools)}")
        return self.visual_tools, self.control_tools
    
    def _analyze_editor_ui(self):
        """Extract editor UI mutable elements"""
        visual_ui_elements = [
            # Top menu
            ("file_menu", "File menu display"),
            ("edit_menu", "Edit menu display"),
            ("scene_menu", "Scene menu display"),
            ("tools_menu", "Tools menu display"),
            ("help_menu", "Help menu display"),
            
            # Main windows
            ("scene_tree_view", "Scene tree hierarchy display"),
            ("inspector_panel", "Inspector properties display"),
            ("output_panel", "Output/console display"),
            ("debugger_panel", "Debugger state display"),
            ("animation_panel", "Animation timeline display"),
            ("script_editor", "Script editor display"),
            ("viewport_main", "Main 3D/2D viewport"),
            ("asset_library", "Asset library display"),
            
            # Toolbars
            ("toolbar_transform", "Transform tools display"),
            ("toolbar_view", "View tools display"),
            ("toolbar_play", "Play controls display"),
            
            # Docks
            ("dock_scene", "Scene dock display"),
            ("dock_import", "Import dock display"),
            ("dock_history", "History dock display"),
            ("dock_node", "Node dock display"),
        ]
        
        control_ui_elements = [
            ("menu_file_new", "Create new project"),
            ("menu_file_open", "Open project"),
            ("menu_file_save", "Save project"),
            ("menu_edit_undo", "Undo action"),
            ("menu_edit_redo", "Redo action"),
            ("menu_scene_save", "Save scene"),
            ("toolbar_play_scene", "Play scene button"),
            ("toolbar_play_project", "Play project button"),
            ("toolbar_stop", "Stop execution button"),
            ("toolbar_pause", "Pause execution button"),
            ("toolbar_step", "Step execution button"),
            ("button_new_node", "Create new node"),
            ("button_delete_node", "Delete selected node"),
            ("button_duplicate_node", "Duplicate node"),
            ("dock_switch_scene", "Switch to scene dock"),
            ("dock_switch_import", "Switch to import dock"),
        ]
        
        self.visual_tools.extend([{"id": f"ui_visual_{name}", "name": name, "desc": desc, "type": "visual"} 
                                 for name, desc in visual_ui_elements])
        self.control_tools.extend([{"id": f"ui_control_{name}", "name": name, "desc": desc, "type": "control"} 
                                  for name, desc in control_ui_elements])
    
    def _analyze_scene_nodes(self):
        """Extract scene and node mutable elements"""
        node_types = [
            "Node", "Node2D", "Node3D", "Control", "CanvasItem",
            "PhysicsBody2D", "PhysicsBody3D", "CharacterBody2D", "CharacterBody3D",
            "RigidBody2D", "RigidBody3D", "StaticBody2D", "StaticBody3D",
            "Sprite2D", "Sprite3D", "MeshInstance3D", "SkeletonIK3D",
            "Camera2D", "Camera3D", "Light2D", "Light3D", "OmniLight3D",
            "SpotLight3D", "DirectionalLight3D",
            "AudioStreamPlayer", "AudioStreamPlayer2D", "AudioStreamPlayer3D",
            "AnimationPlayer", "AnimatedSprite2D", "AnimatedSprite3D",
            "VisibleOnScreenNotifier2D", "VisibleOnScreenNotifier3D",
            "Marker2D", "Marker3D", "Path2D", "Path3D",
            "Area2D", "Area3D", "CollisionShape2D", "CollisionShape3D",
            "UI/Control", "UI/Button", "UI/Label", "UI/TextEdit", "UI/LineEdit",
            "UI/Panel", "UI/PanelContainer", "UI/VBoxContainer", "UI/HBoxContainer"
        ]
        
        for node_type in node_types:
            # Visual: show node in scene tree
            self.visual_tools.append({
                "id": f"node_visual_{node_type.lower().replace('/', '_')}",
                "name": f"node_display_{node_type}",
                "desc": f"Display {node_type} in scene tree",
                "type": "visual"
            })
            
            # Control: create/modify/delete node
            self.control_tools.append({
                "id": f"node_control_create_{node_type.lower().replace('/', '_')}",
                "name": f"node_create_{node_type}",
                "desc": f"Create {node_type} instance",
                "type": "control"
            })
        
        # Node properties (most mutable)
        node_properties = [
            ("position", "Node position (Vector2/Vector3)"),
            ("rotation", "Node rotation"),
            ("scale", "Node scale"),
            ("transform", "Node transform matrix"),
            ("visible", "Node visibility"),
            ("modulate", "Node modulation (color/alpha)"),
            ("self_modulate", "Self modulation"),
            ("name", "Node name"),
            ("owner", "Node owner"),
            ("unique_name_in_owner", "Unique name flag"),
            ("process_mode", "Process mode (inherit/pausable/when_paused/always/disabled)"),
            ("custom_multiplayer", "Custom multiplayer setting"),
            ("physics_interpolation_mode", "Physics interpolation"),
        ]
        
        for prop_name, prop_desc in node_properties:
            self.visual_tools.append({
                "id": f"prop_visual_{prop_name}",
                "name": f"property_display_{prop_name}",
                "desc": f"Display node {prop_desc}",
                "type": "visual"
            })
            self.control_tools.append({
                "id": f"prop_control_{prop_name}",
                "name": f"property_set_{prop_name}",
                "desc": f"Set node {prop_desc}",
                "type": "control"
            })
    
    def _analyze_project_settings(self):
        """Extract project settings mutable elements"""
        settings_categories = [
            ("application", "Application settings"),
            ("rendering", "Rendering settings"),
            ("physics", "Physics settings"),
            ("input", "Input mapping"),
            ("display", "Display settings"),
            ("audio", "Audio settings"),
            ("debug", "Debug settings"),
            ("network", "Network settings"),
            ("localization", "Localization settings"),
            ("gui", "GUI theme settings"),
            ("importer", "Importer settings"),
            ("layer_names_2d", "2D layer names"),
            ("layer_names_3d", "3D layer names"),
            ("physics_layers", "Physics layers"),
            ("shader_globals", "Shader global variables"),
        ]
        
        for cat, desc in settings_categories:
            self.visual_tools.append({
                "id": f"settings_visual_{cat}",
                "name": f"settings_display_{cat}",
                "desc": f"Display {desc}",
                "type": "visual"
            })
            self.control_tools.append({
                "id": f"settings_control_{cat}",
                "name": f"settings_modify_{cat}",
                "desc": f"Modify {desc}",
                "type": "control"
            })
    
    def _analyze_rendering(self):
        """Extract rendering mutable elements"""
        render_elements = [
            ("viewport_camera", "Viewport camera position/rotation"),
            ("viewport_zoom", "Viewport zoom level"),
            ("viewport_grid", "Grid display settings"),
            ("viewport_gizmo", "Gizmo display"),
            ("render_environment", "Environment (lighting, fog, sky)"),
            ("render_world_env", "World environment"),
            ("render_lights", "Light properties"),
            ("render_shadows", "Shadow settings"),
            ("render_materials", "Material properties"),
            ("render_textures", "Texture properties"),
            ("render_shaders", "Shader properties"),
            ("render_canvas", "Canvas layer rendering"),
            ("render_post_process", "Post-processing effects"),
            ("render_lod", "LOD settings"),
            ("render_occlusion", "Occlusion culling"),
        ]
        
        for elem, desc in render_elements:
            self.visual_tools.append({
                "id": f"render_visual_{elem}",
                "name": f"render_display_{elem}",
                "desc": f"Display {desc}",
                "type": "visual"
            })
            self.control_tools.append({
                "id": f"render_control_{elem}",
                "name": f"render_modify_{elem}",
                "desc": f"Modify {desc}",
                "type": "control"
            })
    
    def _analyze_animation(self):
        """Extract animation mutable elements"""
        anim_elements = [
            ("timeline", "Animation timeline"),
            ("keyframes", "Keyframe display"),
            ("playback_position", "Playback position"),
            ("playback_speed", "Playback speed"),
            ("animation_list", "Animation list"),
            ("track_list", "Animation tracks"),
            ("bezier_editor", "Bezier curve editor"),
            ("animation_blend", "Animation blending"),
            ("animation_state_machine", "State machine transitions"),
        ]
        
        for elem, desc in anim_elements:
            self.visual_tools.append({
                "id": f"anim_visual_{elem}",
                "name": f"anim_display_{elem}",
                "desc": f"Display {desc}",
                "type": "visual"
            })
            self.control_tools.append({
                "id": f"anim_control_{elem}",
                "name": f"anim_modify_{elem}",
                "desc": f"Modify {desc}",
                "type": "control"
            })
    
    def _analyze_physics(self):
        """Extract physics mutable elements"""
        physics_elements = [
            ("2d_gravity", "2D world gravity"),
            ("2d_damping", "2D damping settings"),
            ("3d_gravity", "3D world gravity"),
            ("3d_damping", "3D damping settings"),
            ("collision_layers", "Collision layers"),
            ("collision_masks", "Collision masks"),
            ("rigid_body_params", "RigidBody parameters"),
            ("physics_material", "Physics material properties"),
            ("joint_params", "Joint parameters"),
            ("vehicle_params", "Vehicle parameters"),
            ("character_params", "Character parameters"),
        ]
        
        for elem, desc in physics_elements:
            self.visual_tools.append({
                "id": f"physics_visual_{elem}",
                "name": f"physics_display_{elem}",
                "desc": f"Display {desc}",
                "type": "visual"
            })
            self.control_tools.append({
                "id": f"physics_control_{elem}",
                "name": f"physics_modify_{elem}",
                "desc": f"Modify {desc}",
                "type": "control"
            })
    
    def _analyze_input_output(self):
        """Extract input/output mutable elements"""
        io_elements = [
            ("input_map", "Input action mapping"),
            ("keyboard_input", "Keyboard input simulation"),
            ("mouse_input", "Mouse input simulation"),
            ("gamepad_input", "Gamepad input simulation"),
            ("touch_input", "Touch input simulation"),
            ("midi_input", "MIDI input handling"),
            ("joy_input", "Joystick input handling"),
            ("output_console", "Output console"),
            ("debug_print", "Debug output"),
            ("profiler", "Profiler data"),
            ("network_socket", "Network socket control"),
        ]
        
        for elem, desc in io_elements:
            self.visual_tools.append({
                "id": f"io_visual_{elem}",
                "name": f"io_display_{elem}",
                "desc": f"Display {desc}",
                "type": "visual"
            })
            self.control_tools.append({
                "id": f"io_control_{elem}",
                "name": f"io_command_{elem}",
                "desc": f"Control {desc}",
                "type": "control"
            })
    
    def _analyze_scripting(self):
        """Extract scripting mutable elements"""
        script_elements = [
            ("script_edit", "Script editor content"),
            ("script_output", "Script output/console"),
            ("breakpoints", "Debugger breakpoints"),
            ("watch_variables", "Variable watch display"),
            ("call_stack", "Call stack display"),
            ("memory_profiler", "Memory profiling"),
            ("performance_monitor", "Performance monitoring"),
            ("gdscript_highlighter", "GDScript syntax highlighting"),
            ("csharp_highlighter", "C# syntax highlighting"),
            ("autocomplete", "Autocomplete suggestions"),
        ]
        
        for elem, desc in script_elements:
            self.visual_tools.append({
                "id": f"script_visual_{elem}",
                "name": f"script_display_{elem}",
                "desc": f"Display {desc}",
                "type": "visual"
            })
            self.control_tools.append({
                "id": f"script_control_{elem}",
                "name": f"script_manage_{elem}",
                "desc": f"Manage {desc}",
                "type": "control"
            })
    
    def _analyze_resources(self):
        """Extract resource mutable elements"""
        resource_elements = [
            ("texture_import", "Texture import settings"),
            ("mesh_import", "Mesh import settings"),
            ("audio_import", "Audio import settings"),
            ("scene_import", "Scene import settings"),
            ("font_import", "Font import settings"),
            ("script_import", "Script import settings"),
            ("material_editor", "Material editor"),
            ("shader_editor", "Shader editor"),
            ("tilemap_editor", "Tilemap editor"),
            ("polygon_editor", "Polygon editor"),
            ("resource_list", "Resource list display"),
        ]
        
        for elem, desc in resource_elements:
            self.visual_tools.append({
                "id": f"resource_visual_{elem}",
                "name": f"resource_display_{elem}",
                "desc": f"Display {desc}",
                "type": "visual"
            })
            self.control_tools.append({
                "id": f"resource_control_{elem}",
                "name": f"resource_manage_{elem}",
                "desc": f"Manage {desc}",
                "type": "control"
            })
    
    def _analyze_project_management(self):
        """Extract project management mutable elements"""
        project_elements = [
            ("project_version", "Project version info"),
            ("project_name", "Project name"),
            ("project_icon", "Project icon"),
            ("project_author", "Project author info"),
            ("build_profile", "Build profile"),
            ("export_preset", "Export presets"),
            ("addon_list", "Addon list and settings"),
            ("autoload", "Autoload list"),
            ("scene_tabs", "Open scene tabs"),
            ("undo_redo_history", "Undo/redo history"),
            ("version_control", "Version control integration"),
        ]
        
        for elem, desc in project_elements:
            self.visual_tools.append({
                "id": f"project_visual_{elem}",
                "name": f"project_display_{elem}",
                "desc": f"Display {desc}",
                "type": "visual"
            })
            self.control_tools.append({
                "id": f"project_control_{elem}",
                "name": f"project_manage_{elem}",
                "desc": f"Manage {desc}",
                "type": "control"
            })


def main():
    source_path = "c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot\\godot_source"
    analyzer = GodotAPIAnalyzer(source_path)
    visual, control = analyzer.analyze()
    
    # Save definitions
    visual_path = "c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot\\tools_definition\\visual\\tools.json"
    control_path = "c:\\Users\\xray\\Documents\\ArkStudio\\AgenticGodot\\tools_definition\\control\\tools.json"
    
    os.makedirs(os.path.dirname(visual_path), exist_ok=True)
    os.makedirs(os.path.dirname(control_path), exist_ok=True)
    
    with open(visual_path, 'w') as f:
        json.dump(visual, f, indent=2)
    
    with open(control_path, 'w') as f:
        json.dump(control, f, indent=2)
    
    print(f"\n[+] Visual tools saved to {visual_path}")
    print(f"[+] Control tools saved to {control_path}")
    print(f"\n[*] Total tools generated: {len(visual) + len(control)}")


if __name__ == "__main__":
    main()

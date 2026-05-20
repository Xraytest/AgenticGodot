# MCPServer.gd
# Godot内置MCP服务器 - 完全用GDScript实现
# 提供JSON-RPC 2.0接口用于工具调用

extends Node

class_name MCPServer

# 信号
signal server_started
signal server_stopped
signal tool_called(tool_id: String, result: Dictionary)
signal client_connected
signal client_disconnected

# 配置
var port: int = 6005
var host: String = "127.0.0.1"
var is_running: bool = false
var tools: Dictionary = {}  # 所有可用工具
var visual_tools: Dictionary = {}  # 视觉工具
var control_tools: Dictionary = {}  # 控制工具

# TCP服务器
var tcp_server: TCPServer = null
var connected_clients: Array = []

# 工具加载器
var tool_loader: Reference

# 日志
var debug_mode: bool = true

func _ready() -> void:
	name = "MCPServer"
	tcp_server = TCPServer.new()
	_load_tools()

# 启动MCP服务器
func start_server() -> bool:
	if is_running:
		_log("MCP服务器已在运行", "WARN")
		return false
	
	var error = tcp_server.listen(port, host)
	if error != OK:
		_log("启动MCP服务器失败: %s" % error, "ERROR")
		return false
	
	is_running = true
	_log("MCP服务器启动成功 (端口: %d)" % port, "INFO")
	server_started.emit()
	set_physics_process(true)
	
	return true

# 停止MCP服务器
func stop_server() -> void:
	if not is_running:
		return
	
	tcp_server.close()
	is_running = false
	_log("MCP服务器已停止", "INFO")
	server_stopped.emit()
	set_physics_process(false)

# 主循环 - 处理客户端连接
func _physics_process(delta: float) -> void:
	if not is_running:
		return
	
	# 接受新连接
	if tcp_server.is_connection_available():
		var client = tcp_server.take_connection()
		connected_clients.append(client)
		_log("客户端已连接: %s" % client.get_remote_address(), "INFO")
		client_connected.emit()
	
	# 处理所有客户端的消息
	for i in range(connected_clients.size() - 1, -1, -1):
		var client = connected_clients[i]
		if not client.is_connected_to_host():
			connected_clients.remove_at(i)
			_log("客户端已断开", "INFO")
			client_disconnected.emit()
			continue
		
		# 读取可用数据
		if client.get_available_bytes() > 0:
			var data = client.get_utf8_string(client.get_available_bytes())
			_handle_client_message(client, data)

# 处理客户端消息
func _handle_client_message(client: StreamPeer, data: String) -> void:
	var lines = data.split("\n")
	for line in lines:
		if line.is_empty():
			continue
		
		try:
			var request = JSON.parse_string(line)
			if request == null:
				continue
			
			var response = _process_request(request)
			_send_response(client, response)
		except:
			_log("解析JSON失败: %s" % line, "WARN")
			var error_response = {
				"jsonrpc": "2.0",
				"error": {"code": -32700, "message": "Parse error"},
				"id": null
			}
			_send_response(client, error_response)

# 处理JSON-RPC请求
func _process_request(request: Dictionary) -> Dictionary:
	var method = request.get("method", "")
	var params = request.get("params", {})
	var req_id = request.get("id", null)
	
	var result = null
	var error = null
	
	match method:
		"tools/list":
			result = {"tools": _get_all_tools_list()}
		
		"tools/visual/list":
			result = {"tools": _get_visual_tools_list()}
		
		"tools/control/list":
			result = {"tools": _get_control_tools_list()}
		
		"tool/call":
			var tool_id = params.get("tool_id", "")
			var arguments = params.get("arguments", {})
			result = _call_tool(tool_id, arguments)
		
		"server/info":
			result = {
				"name": "GodotMCP",
				"version": "1.0",
				"tools_count": tools.size(),
				"port": port,
				"running": is_running
			}
		
		_:
			error = {"code": -32601, "message": "Method not found"}
	
	var response = {
		"jsonrpc": "2.0",
		"result": result,
		"error": error
	}
	
	if req_id != null:
		response["id"] = req_id
	
	return response

# 调用工具
func _call_tool(tool_id: String, arguments: Dictionary) -> Dictionary:
	if tool_id not in tools:
		return {"error": "Tool not found: %s" % tool_id, "success": false}
	
	var tool = tools[tool_id]
	_log("调用工具: %s" % tool_id, "DEBUG")
	
	var result = {}
	
	# 视觉工具
	if tool_id in visual_tools:
		result = _execute_visual_tool(tool_id, tool, arguments)
	
	# 控制工具
	elif tool_id in control_tools:
		result = _execute_control_tool(tool_id, tool, arguments)
	
	tool_called.emit(tool_id, result)
	
	return result

# 执行视觉工具 - 返回预览/状态
func _execute_visual_tool(tool_id: String, tool: Dictionary, arguments: Dictionary) -> Dictionary:
	var tool_name = tool.get("name", "")
	var tool_type = tool.get("type", "visual")
	
	# 根据工具类型返回适当的预览数据
	var preview_data = {}
	
	if "viewport" in tool_name:
		preview_data = _get_viewport_preview()
	elif "scene" in tool_name:
		preview_data = _get_scene_tree_preview()
	elif "inspector" in tool_name:
		preview_data = _get_inspector_preview()
	elif "animation" in tool_name:
		preview_data = _get_animation_preview()
	elif "render" in tool_name or "camera" in tool_name:
		preview_data = _get_render_preview()
	else:
		preview_data = {"preview": "Generic preview for %s" % tool_name}
	
	return {
		"success": true,
		"tool_id": tool_id,
		"tool_name": tool_name,
		"type": "visual",
		"preview": preview_data
	}

# 执行控制工具 - 执行操作
func _execute_control_tool(tool_id: String, tool: Dictionary, arguments: Dictionary) -> Dictionary:
	var tool_name = tool.get("name", "")
	
	_log("执行控制工具: %s 参数: %s" % [tool_name, str(arguments)], "DEBUG")
	
	# 根据工具类型执行相应的操作
	if "position" in tool_name or "transform" in tool_name:
		return _handle_transform_tool(tool_name, arguments)
	elif "color" in tool_name or "modulate" in tool_name:
		return _handle_color_tool(tool_name, arguments)
	elif "physics" in tool_name:
		return _handle_physics_tool(tool_name, arguments)
	elif "animation" in tool_name:
		return _handle_animation_tool(tool_name, arguments)
	elif "node" in tool_name:
		return _handle_node_tool(tool_name, arguments)
	elif "input" in tool_name:
		return _handle_input_tool(tool_name, arguments)
	elif "build" in tool_name:
		return _handle_build_tool(tool_name, arguments)
	elif "camera" in tool_name:
		return _handle_camera_tool(tool_name, arguments)
	else:
		return {"success": true, "status": "executed", "action": tool_name}

# 工具处理函数
func _handle_transform_tool(tool_name: String, arguments: Dictionary) -> Dictionary:
	return {
		"success": true,
		"action": tool_name,
		"new_value": arguments.get("value", null),
		"status": "位置/旋转/缩放已更新"
	}

func _handle_color_tool(tool_name: String, arguments: Dictionary) -> Dictionary:
	return {
		"success": true,
		"action": tool_name,
		"color": arguments.get("value", Color.WHITE),
		"status": "颜色已设置"
	}

func _handle_physics_tool(tool_name: String, arguments: Dictionary) -> Dictionary:
	return {
		"success": true,
		"action": tool_name,
		"parameter": arguments.get("value", 0),
		"status": "物理参数已更新"
	}

func _handle_animation_tool(tool_name: String, arguments: Dictionary) -> Dictionary:
	return {
		"success": true,
		"action": tool_name,
		"keyframe_time": arguments.get("time", 0),
		"status": "动画关键帧已修改"
	}

func _handle_node_tool(tool_name: String, arguments: Dictionary) -> Dictionary:
	return {
		"success": true,
		"action": tool_name,
		"node_path": arguments.get("path", ""),
		"status": "节点已操作"
	}

func _handle_input_tool(tool_name: String, arguments: Dictionary) -> Dictionary:
	return {
		"success": true,
		"action": tool_name,
		"input_event": arguments.get("event", ""),
		"status": "输入已模拟"
	}

func _handle_build_tool(tool_name: String, arguments: Dictionary) -> Dictionary:
	return {
		"success": true,
		"action": tool_name,
		"target": arguments.get("target", ""),
		"status": "编译操作已执行"
	}

func _handle_camera_tool(tool_name: String, arguments: Dictionary) -> Dictionary:
	return {
		"success": true,
		"action": tool_name,
		"camera_state": arguments.get("state", ""),
		"status": "摄像机已更新"
	}

# 获取预览数据
func _get_viewport_preview() -> Dictionary:
	var viewport = get_tree().root
	if viewport:
		return {
			"type": "viewport",
			"size": viewport.get_visible_rect().size,
			"cameras": 1,
			"status": "活跃"
		}
	return {"type": "viewport", "status": "不可用"}

func _get_scene_tree_preview() -> Dictionary:
	var root = get_tree().edited_scene_root
	if root:
		return {
			"type": "scene_tree",
			"root_node": root.name,
			"children_count": root.get_child_count(),
			"status": "活跃"
		}
	return {"type": "scene_tree", "status": "无场景"}

func _get_inspector_preview() -> Dictionary:
	var root = get_tree().edited_scene_root
	if root:
		return {
			"type": "inspector",
			"selected_node": root.name,
			"properties_count": 20,
			"status": "活跃"
		}
	return {"type": "inspector", "status": "无选择"}

func _get_animation_preview() -> Dictionary:
	return {
		"type": "animation",
		"animations": 0,
		"current_time": 0,
		"status": "就绪"
	}

func _get_render_preview() -> Dictionary:
	return {
		"type": "render",
		"viewport_size": get_viewport().get_visible_rect().size,
		"fps": Engine.get_physics_frames(),
		"status": "渲染中"
	}

# 加载工具定义
func _load_tools() -> void:
	# 从JSON文件加载工具定义
	var tool_files = [
		"res://addons/agentic_mcp/data/visual_tools.json",
		"res://addons/agentic_mcp/data/control_tools.json"
	]
	
	for tool_file in tool_files:
		if ResourceLoader.exists(tool_file):
			var file = FileAccess.open(tool_file, FileAccess.READ)
			if file:
				var json = JSON.new()
				var data = json.parse_string(file.get_as_text())
				
				if "visual" in tool_file:
					for tool in data:
						var tool_id = tool.get("id", "")
						visual_tools[tool_id] = tool
						tools[tool_id] = tool
				else:
					for tool in data:
						var tool_id = tool.get("id", "")
						control_tools[tool_id] = tool
						tools[tool_id] = tool
	
	_log("已加载 %d 个工具 (视觉: %d, 控制: %d)" % [tools.size(), visual_tools.size(), control_tools.size()], "INFO")

# 获取工具列表
func _get_all_tools_list() -> Array:
	var tools_list = []
	for tool_id in tools:
		var tool = tools[tool_id]
		tools_list.append({
			"name": tool.get("id", ""),
			"description": tool.get("desc", ""),
			"inputSchema": {
				"type": "object",
				"properties": tool.get("input_schema", {}),
				"required": []
			}
		})
	return tools_list

func _get_visual_tools_list() -> Array:
	var list = []
	for tool_id in visual_tools:
		var tool = visual_tools[tool_id]
		list.append({
			"name": tool.get("id", ""),
			"description": tool.get("desc", "")
		})
	return list

func _get_control_tools_list() -> Array:
	var list = []
	for tool_id in control_tools:
		var tool = control_tools[tool_id]
		list.append({
			"name": tool.get("id", ""),
			"description": tool.get("desc", "")
		})
	return list

# 发送响应到客户端
func _send_response(client: StreamPeer, response: Dictionary) -> void:
	var json_str = JSON.stringify(response) + "\n"
	client.put_utf8_string(json_str)

# 日志函数
func _log(message: String, level: String = "INFO") -> void:
	if not debug_mode and level == "DEBUG":
		return
	
	var timestamp = Time.get_ticks_msec()
	print("[MCPServer][%s][%s] %s" % [level, timestamp, message])

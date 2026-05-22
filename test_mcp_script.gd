extends Node

func _ready():
    print("=== AgenticMCP Test ===")
    
    if Engine.has_singleton("AgenticMCP"):
        var mcp = Engine.get_singleton("AgenticMCP")
        print("[+] AgenticMCP singleton found")
        print_tool_info(mcp)
        
        mcp.stop()
        print("[+] Stopped default server on port 6005")
        
        if mcp.start(16005):
            print("[+] Started MCP server on port 16005")
            print("[+] is_running: ", mcp.is_running())
            
            var tools = mcp.get_tools_list()
            print("[+] Total tools: ", tools.size())
            
            var vis_tools = mcp.get_visual_tools_list()
            print("[+] Visual tools: ", vis_tools.size())
            
            var ctrl_tools = mcp.get_control_tools_list()
            print("[+] Control tools: ", ctrl_tools.size())
            
            print("[*] Waiting for connections... Press F1 to exit")
        else:
            print("[-] Failed to start MCP server")
    else:
        print("[-] AgenticMCP singleton NOT found!")

func _input(event):
    if event.is_action_pressed("ui_cancel"):
        get_tree().quit()

func print_tool_info(mcp):
    print("  - get_tool_count(): ", mcp.get_tool_count())
    print("  - get_visual_tool_count(): ", mcp.get_visual_tool_count())
    print("  - get_control_tool_count(): ", mcp.get_control_tool_count())
    print("  - get_port(): ", mcp.get_port())
    print("  - is_running(): ", mcp.is_running())

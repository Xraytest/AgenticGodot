#!/usr/bin/env python3
"""
MCP Server for Godot Control and Visualization
Exposes 500+ tools for controlling every mutable element of Godot
Separates CONTROL tools from VISUAL tools
"""

import os
import json
import asyncio
import logging
import sys
from typing import Any, Optional
from pathlib import Path

# MCP Protocol Server implementation
from dataclasses import dataclass, field
from enum import Enum
import socket
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('GodotMCP')


class ToolType(Enum):
    VISUAL = "visual"
    CONTROL = "control"


@dataclass
class Tool:
    id: str
    name: str
    description: str
    tool_type: ToolType
    input_schema: dict = field(default_factory=dict)
    output_schema: dict = field(default_factory=dict)
    
    def to_mcp_format(self) -> dict:
        """Convert tool to MCP protocol format"""
        return {
            "name": self.id,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": self.input_schema,
                "required": list(self.input_schema.keys()) if self.input_schema else []
            }
        }


class GodotMCPServer:
    """MCP Server for Godot Engine Control"""
    
    def __init__(self, port: int = 6005, tools_dir: str = None):
        self.port = port
        self.tools_dir = tools_dir or str(Path(__file__).parent.parent / "tools_definition")
        self.tools: dict[str, Tool] = {}
        self.visual_tools: dict[str, Tool] = {}
        self.control_tools: dict[str, Tool] = {}
        self.godot_process = None
        self.mcp_server = None
        self.running = False
        
    def load_tools(self):
        """Load tool definitions from JSON files"""
        logger.info(f"[*] Loading tools from {self.tools_dir}")
        
        # Load visual tools
        visual_path = os.path.join(self.tools_dir, "visual", "tools.json")
        control_path = os.path.join(self.tools_dir, "control", "tools.json")
        visual_ext_path = os.path.join(self.tools_dir, "visual", "tools_extended.json")
        control_ext_path = os.path.join(self.tools_dir, "control", "tools_extended.json")
        
        tool_count = 0
        
        # Load all JSON files
        for path, tool_type in [
            (visual_path, ToolType.VISUAL),
            (control_path, ToolType.CONTROL),
            (visual_ext_path, ToolType.VISUAL),
            (control_ext_path, ToolType.CONTROL),
        ]:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    tools_data = json.load(f)
                    for tool_data in tools_data:
                        tool = Tool(
                            id=tool_data.get('id', ''),
                            name=tool_data.get('name', ''),
                            description=tool_data.get('desc', ''),
                            tool_type=tool_type,
                            input_schema=tool_data.get('input_schema', {}),
                            output_schema=tool_data.get('output_schema', {})
                        )
                        self.tools[tool.id] = tool
                        if tool_type == ToolType.VISUAL:
                            self.visual_tools[tool.id] = tool
                        else:
                            self.control_tools[tool.id] = tool
                        tool_count += 1
        
        logger.info(f"[+] Loaded {tool_count} tools total")
        logger.info(f"    - Visual tools: {len(self.visual_tools)}")
        logger.info(f"    - Control tools: {len(self.control_tools)}")
    
    def get_tools_list(self) -> list[dict]:
        """Get list of all available tools in MCP format"""
        return [tool.to_mcp_format() for tool in self.tools.values()]
    
    async def handle_tool_call(self, tool_id: str, arguments: dict) -> dict:
        """Handle a tool call from the MCP client"""
        if tool_id not in self.tools:
            return {"error": f"Tool {tool_id} not found"}
        
        tool = self.tools[tool_id]
        logger.info(f"[>] Calling tool: {tool_id} ({tool.tool_type.value})")
        
        try:
            if tool.tool_type == ToolType.VISUAL:
                return await self._handle_visual_tool(tool, arguments)
            else:
                return await self._handle_control_tool(tool, arguments)
        except Exception as e:
            logger.error(f"[!] Error calling tool {tool_id}: {e}")
            return {"error": str(e)}
    
    async def _handle_visual_tool(self, tool: Tool, arguments: dict) -> dict:
        """Handle visual tool - returns preview/state"""
        # In actual implementation, this would query Godot's state
        logger.info(f"    [V] Visual tool: {tool.name}")
        
        # Return simulated preview data
        return {
            "success": True,
            "tool": tool.id,
            "type": "visual",
            "preview": f"Preview of {tool.name}",
            "data": arguments
        }
    
    async def _handle_control_tool(self, tool: Tool, arguments: dict) -> dict:
        """Handle control tool - performs action"""
        # In actual implementation, this would send command to Godot
        logger.info(f"    [C] Control tool: {tool.name}")
        
        # Return action result
        return {
            "success": True,
            "tool": tool.id,
            "type": "control",
            "action": tool.name,
            "arguments": arguments,
            "status": "executed"
        }
    
    async def start_mcp_server(self):
        """Start the MCP server listening on the specified port"""
        logger.info(f"[*] Starting MCP server on port {self.port}")
        
        self.running = True
        server_thread = threading.Thread(target=self._run_mcp_server, daemon=True)
        server_thread.start()
        
        logger.info(f"[+] MCP server started successfully on port {self.port}")
    
    def _run_mcp_server(self):
        """Run the MCP server (simplified implementation)"""
        # This is a simplified version - real implementation would use
        # proper MCP protocol handling and async I/O
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('localhost', self.port))
            server_socket.listen(1)
            
            logger.info(f"[*] MCP server listening on port {self.port}...")
            
            while self.running:
                try:
                    client_socket, addr = server_socket.accept()
                    logger.info(f"[+] Client connected from {addr}")
                    
                    # Handle client in a separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket,),
                        daemon=True
                    )
                    client_thread.start()
                except Exception as e:
                    if self.running:
                        logger.error(f"[!] Error accepting client: {e}")
        except Exception as e:
            logger.error(f"[!] Error in MCP server: {e}")
        finally:
            try:
                server_socket.close()
            except:
                pass
    
    def _handle_client(self, client_socket):
        """Handle a connected MCP client"""
        try:
            while self.running:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                # Parse and handle the request (simplified JSON-RPC)
                try:
                    request = json.loads(data)
                    response = self._process_request(request)
                    client_socket.send(json.dumps(response).encode('utf-8'))
                except json.JSONDecodeError:
                    response = {"error": "Invalid JSON"}
                    client_socket.send(json.dumps(response).encode('utf-8'))
        except Exception as e:
            logger.error(f"[!] Error handling client: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
    
    def _process_request(self, request: dict) -> dict:
        """Process a client request (simplified JSON-RPC 2.0)"""
        method = request.get('method', '')
        params = request.get('params', {})
        req_id = request.get('id', None)
        
        try:
            if method == 'tools/list':
                result = {"tools": self.get_tools_list()}
            elif method == 'tool/call':
                tool_id = params.get('tool_id', '')
                arguments = params.get('arguments', {})
                # Run async function synchronously (simplified)
                result = asyncio.run(self.handle_tool_call(tool_id, arguments))
            elif method == 'tools/visual/list':
                result = {"tools": [t.to_mcp_format() for t in self.visual_tools.values()]}
            elif method == 'tools/control/list':
                result = {"tools": [t.to_mcp_format() for t in self.control_tools.values()]}
            elif method == 'server/info':
                result = {
                    "version": "1.0",
                    "name": "GodotMCP",
                    "tools_count": len(self.tools),
                    "port": self.port,
                    "running": self.running
                }
            else:
                result = {"error": f"Unknown method: {method}"}
        except Exception as e:
            result = {"error": str(e)}
        
        response = {
            "jsonrpc": "2.0",
            "result": result if 'error' not in result else None,
            "error": result.get("error"),
        }
        if req_id is not None:
            response["id"] = req_id
        
        return response
    
    async def shutdown(self):
        """Shutdown the MCP server"""
        logger.info("[*] Shutting down MCP server...")
        self.running = False


async def main():
    """Main entry point for the MCP server"""
    
    # Create server instance
    tools_dir = os.environ.get('GODOT_TOOLS_DIR', 
                              str(Path(__file__).parent.parent / "tools_definition"))
    port = int(os.environ.get('GODOT_MCP_PORT', 6005))
    
    server = GodotMCPServer(port=port, tools_dir=tools_dir)
    
    # Load tools
    server.load_tools()
    
    # Start MCP server
    await server.start_mcp_server()
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("[*] Received shutdown signal")
        await server.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())

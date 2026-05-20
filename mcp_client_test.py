#!/usr/bin/env python3
"""
MCP Client Test Suite
Tests connection and basic tool calls to the Godot MCP server
"""

import socket
import json
import sys
import argparse
import time
from typing import Optional, Dict, Any
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('MCPClient')


class MCPClient:
    def __init__(self, host: str = 'localhost', port: int = 6005):
        self.host = host
        self.port = port
        self.socket = None
        self.request_id = 0
    
    def connect(self, timeout: int = 5) -> bool:
        """Connect to MCP server"""
        logger.info(f"[*] Connecting to {self.host}:{self.port}...")
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)
            self.socket.connect((self.host, self.port))
            logger.info("[+] Connected to MCP server")
            return True
        except Exception as e:
            logger.error(f"[!] Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
    
    def send_request(self, method: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Send JSON-RPC request to server"""
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self.request_id
        }
        
        if params:
            request["params"] = params
        
        try:
            # Send request
            self.socket.send(json.dumps(request).encode('utf-8'))
            
            # Receive response
            response_data = self.socket.recv(65536).decode('utf-8')
            response = json.loads(response_data)
            
            return response
        except Exception as e:
            logger.error(f"[!] Request failed: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Test basic server connection"""
        logger.info("[*] Testing server connection...")
        
        response = self.send_request('server/info')
        if response and 'result' in response:
            result = response['result']
            logger.info(f"[+] Server Info:")
            logger.info(f"    Name: {result.get('name')}")
            logger.info(f"    Version: {result.get('version')}")
            logger.info(f"    Tools: {result.get('tools_count')}")
            logger.info(f"    Port: {result.get('port')}")
            return True
        else:
            logger.error("[!] Server info request failed")
            return False
    
    def get_tools_list(self) -> Optional[list]:
        """Get list of all available tools"""
        logger.info("[*] Fetching tools list...")
        
        response = self.send_request('tools/list')
        if response and 'result' in response:
            tools = response['result'].get('tools', [])
            logger.info(f"[+] Found {len(tools)} tools")
            return tools
        else:
            logger.error("[!] Failed to fetch tools")
            return None
    
    def get_visual_tools(self) -> Optional[list]:
        """Get list of visual tools"""
        logger.info("[*] Fetching visual tools...")
        
        response = self.send_request('tools/visual/list')
        if response and 'result' in response:
            tools = response['result'].get('tools', [])
            logger.info(f"[+] Found {len(tools)} visual tools")
            return tools
        else:
            logger.error("[!] Failed to fetch visual tools")
            return None
    
    def get_control_tools(self) -> Optional[list]:
        """Get list of control tools"""
        logger.info("[*] Fetching control tools...")
        
        response = self.send_request('tools/control/list')
        if response and 'result' in response:
            tools = response['result'].get('tools', [])
            logger.info(f"[+] Found {len(tools)} control tools")
            return tools
        else:
            logger.error("[!] Failed to fetch control tools")
            return None
    
    def call_tool(self, tool_id: str, arguments: Optional[Dict] = None) -> Optional[Dict]:
        """Call a specific tool"""
        logger.info(f"[*] Calling tool: {tool_id}")
        
        params = {
            "tool_id": tool_id,
            "arguments": arguments or {}
        }
        
        response = self.send_request('tool/call', params=params)
        if response and 'result' in response:
            logger.info(f"[+] Tool result: {response['result']}")
            return response['result']
        else:
            logger.error(f"[!] Tool call failed")
            return None
    
    def test_visual_tool(self, tool_id: str) -> bool:
        """Test a visual tool"""
        logger.info(f"[*] Testing visual tool: {tool_id}")
        
        result = self.call_tool(tool_id, {})
        return result is not None
    
    def test_control_tool(self, tool_id: str, args: Dict) -> bool:
        """Test a control tool"""
        logger.info(f"[*] Testing control tool: {tool_id}")
        
        result = self.call_tool(tool_id, args)
        return result is not None
    
    def run_diagnostic(self) -> bool:
        """Run full diagnostic tests"""
        logger.info("=" * 70)
        logger.info("MCP Client Diagnostic Suite")
        logger.info("=" * 70)
        
        if not self.connect():
            return False
        
        # Test server connection
        if not self.test_connection():
            self.disconnect()
            return False
        
        # Get tool counts
        all_tools = self.get_tools_list()
        visual_tools = self.get_visual_tools()
        control_tools = self.get_control_tools()
        
        logger.info("")
        logger.info("[*] Tool Statistics:")
        logger.info(f"    Total: {len(all_tools) if all_tools else 0}")
        logger.info(f"    Visual: {len(visual_tools) if visual_tools else 0}")
        logger.info(f"    Control: {len(control_tools) if control_tools else 0}")
        
        # Test sample tools
        logger.info("")
        logger.info("[*] Testing sample tools...")
        
        if visual_tools and len(visual_tools) > 0:
            sample_visual = visual_tools[0]['name']
            logger.info(f"    Testing visual tool: {sample_visual}")
            self.test_visual_tool(sample_visual)
        
        if control_tools and len(control_tools) > 0:
            sample_control = control_tools[0]['name']
            logger.info(f"    Testing control tool: {sample_control}")
            self.test_control_tool(sample_control, {})
        
        logger.info("")
        logger.info("[+] Diagnostic complete!")
        
        self.disconnect()
        return True


def main():
    parser = argparse.ArgumentParser(description='MCP Client for Godot')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=6005, help='Server port')
    parser.add_argument('--test', action='store_true', help='Run diagnostic tests')
    parser.add_argument('--tool', help='Call specific tool')
    parser.add_argument('--args', help='Tool arguments (JSON)')
    
    args = parser.parse_args()
    
    client = MCPClient(host=args.host, port=args.port)
    
    if args.test:
        # Run diagnostic
        success = client.run_diagnostic()
        sys.exit(0 if success else 1)
    
    elif args.tool:
        # Call specific tool
        if not client.connect():
            sys.exit(1)
        
        tool_args = {}
        if args.args:
            try:
                tool_args = json.loads(args.args)
            except json.JSONDecodeError:
                logger.error("[!] Invalid JSON arguments")
                sys.exit(1)
        
        result = client.call_tool(args.tool, tool_args)
        client.disconnect()
        
        if result:
            print(json.dumps(result, indent=2))
            sys.exit(0)
        else:
            sys.exit(1)
    
    else:
        # Interactive mode
        if not client.connect():
            sys.exit(1)
        
        logger.info("")
        logger.info("Interactive MCP Client - Type 'help' for commands")
        logger.info("")
        
        while True:
            try:
                cmd = input("> ").strip()
                
                if not cmd:
                    continue
                elif cmd == 'help':
                    print("""
Commands:
  help                     - Show this help
  info                     - Get server info
  tools                    - List all tools
  visual                   - List visual tools
  control                  - List control tools
  call TOOL_ID [ARGS]     - Call a tool
  quit                     - Exit
""")
                elif cmd == 'info':
                    client.send_request('server/info')
                elif cmd == 'tools':
                    client.get_tools_list()
                elif cmd == 'visual':
                    client.get_visual_tools()
                elif cmd == 'control':
                    client.get_control_tools()
                elif cmd.startswith('call'):
                    parts = cmd.split(maxsplit=2)
                    if len(parts) >= 2:
                        tool_id = parts[1]
                        args_json = parts[2] if len(parts) > 2 else '{}'
                        try:
                            args = json.loads(args_json)
                            client.call_tool(tool_id, args)
                        except json.JSONDecodeError:
                            logger.error("Invalid JSON")
                elif cmd == 'quit':
                    break
                else:
                    logger.error(f"Unknown command: {cmd}")
            
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error: {e}")
        
        client.disconnect()
        logger.info("Bye!")


if __name__ == "__main__":
    main()

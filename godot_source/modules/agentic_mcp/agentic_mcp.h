#ifndef AGENTIC_MCP_H
#define AGENTIC_MCP_H

#include "core/object/class_db.h"
#include "core/io/tcp_server.h"
#include "core/io/stream_peer_tcp.h"
#include "core/io/json.h"
#include "core/variant/variant.h"
#include "core/os/thread.h"
#include "core/os/mutex.h"
#include "core/templates/hash_map.h"
#include "core/templates/vector.h"
#include "scene/main/node.h"
#include "scene/main/window.h"
#include "scene/2d/node_2d.h"
#include "scene/3d/node_3d.h"

struct MCPTool {
    String id;
    String name;
    String description;
    String tool_type; // "visual" or "control"
    Dictionary input_schema;
    Dictionary output_schema;

    Dictionary to_mcp_format() const {
        Dictionary d;
        d["name"] = id;
        d["description"] = description;
        Dictionary input_schema_mcp;
        input_schema_mcp["type"] = "object";
        input_schema_mcp["properties"] = input_schema;
        Array required;
        if (input_schema.size() > 0) {
            for (int i = 0; i < input_schema.size(); i++) {
                required.push_back(input_schema.keys()[i]);
            }
        }
        input_schema_mcp["required"] = required;
        d["inputSchema"] = input_schema_mcp;
        return d;
    }
};

class MCPClientHandler : public RefCounted {
    GDCLASS(MCPClientHandler, RefCounted)
public:
    Ref<StreamPeerTCP> connection;
    bool active = true;

    MCPClientHandler() {}
    ~MCPClientHandler() { close(); }

    void close();
    bool send_response(const Dictionary &p_response);

protected:
    static void _bind_methods() {}
};

class AgenticMCP : public Node {
    GDCLASS(AgenticMCP, Object)

    static AgenticMCP *singleton;

    Ref<TCPServer> tcp_server;
    List<Ref<MCPClientHandler>> clients;
    Mutex client_mutex;

    HashMap<String, MCPTool> tools;
    HashMap<String, MCPTool> visual_tools;
    HashMap<String, MCPTool> control_tools;

    bool running = false;
    int listen_port = 6005;

    static void _thread_callback(void *p_self);
    void _server_loop();
    void _accept_clients();
    void _handle_client(Ref<MCPClientHandler> p_client);
    Dictionary _process_request(const Dictionary &p_request);

    void _load_tools();
    void _add_standard_tools();

    Dictionary _handle_visual(const MCPTool &p_tool, const Dictionary &p_args);
    Dictionary _handle_control(const MCPTool &p_tool, const Dictionary &p_args);

    // Visual tool implementations
    Dictionary _get_viewport_preview();
    Dictionary _get_scene_tree_preview();
    Dictionary _get_inspector_preview();
    Dictionary _get_animation_preview();
    Dictionary _get_render_preview();
    Dictionary _get_monitor_data(const String &p_monitor);

    // Control tool implementations
    Dictionary _handle_transform(const Dictionary &p_args);
    Dictionary _handle_node_op(const Dictionary &p_args);
    Dictionary _handle_scene_op(const Dictionary &p_args);
    Dictionary _handle_input_sim(const Dictionary &p_args);
    Dictionary _handle_camera_op(const Dictionary &p_args);
    Dictionary _handle_physics_op(const Dictionary &p_args);
    Dictionary _handle_animation_op(const Dictionary &p_args);
    Dictionary _handle_color_op(const Dictionary &p_args);
    Dictionary _handle_build_op(const Dictionary &p_args);

    bool _find_node_by_path(const String &p_path, Node *&r_node);
    Node *_get_edited_root();

protected:
    static void _bind_methods();

public:
    static AgenticMCP *get_singleton() { return singleton; }

    AgenticMCP();
    ~AgenticMCP();

    void set_port(int p_port) { listen_port = p_port; }
    int get_port() const { return listen_port; }

    bool start(int p_port = 6005);
    void stop();
    bool is_running() const { return running; }

    void on_frame();

    Dictionary call_tool(const String &p_tool_id, const Dictionary &p_arguments);
    Dictionary get_tools_list() const;
    Dictionary get_visual_tools_list() const;
    Dictionary get_control_tools_list() const;
    int get_tool_count() const { return tools.size(); }
    int get_visual_tool_count() const { return visual_tools.size(); }
    int get_control_tool_count() const { return control_tools.size(); }
};

#endif // AGENTIC_MCP_H
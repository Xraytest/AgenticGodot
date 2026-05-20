#include "register_types.h"
#include "agentic_mcp.h"
#include "core/object/class_db.h"

static AgenticMCP *agentic_mcp_singleton = nullptr;

void initialize_agentic_mcp_module(ModuleInitializationLevel p_level) {
    if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {
        return;
    }

    GDREGISTER_CLASS(AgenticMCP);
    agentic_mcp_singleton = memnew(AgenticMCP);
    Engine::get_singleton()->add_singleton(Engine::Singleton("AgenticMCP", agentic_mcp_singleton));
}

void uninitialize_agentic_mcp_module(ModuleInitializationLevel p_level) {
    if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {
        return;
    }

    if (agentic_mcp_singleton) {
        agentic_mcp_singleton->stop();
        memdelete(agentic_mcp_singleton);
        agentic_mcp_singleton = nullptr;
    }
}
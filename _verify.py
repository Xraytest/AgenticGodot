import os

mod_dir = r'C:\Users\xray\Documents\ArkStudio\AgenticGodot\godot_source\modules\agentic_mcp'
files = ['config.py', 'SCsub', 'register_types.h', 'register_types.cpp', 'agentic_mcp.h', 'agentic_mcp.cpp']
print('=== Module Files Verification ===')
for f in files:
    path = os.path.join(mod_dir, f)
    exists = os.path.exists(path)
    size = os.path.getsize(path) if exists else 0
    status = 'OK' if exists else 'MISSING'
    print('  {}: {} ({} bytes)'.format(f, status, size))

# Check main.cpp integration
main_path = r'C:\Users\xray\Documents\ArkStudio\AgenticGodot\godot_source\main\main.cpp'
with open(main_path, 'r', encoding='utf-8') as f:
    mc = f.read()
    checks = {
        'Module include': '#include "modules/agentic_mcp/agentic_mcp.h"' in mc,
        'Port variable': 'agentic_mcp_port' in mc,
        'CLI arg parsing': '--mcp-port' in mc,
        'Startup call': 'get_singleton()->start(' in mc,
        'Frame call': 'get_singleton()->on_frame()' in mc,
        'Cleanup stop call': 'get_singleton()->stop()' in mc,
    }
    print('\n=== main.cpp Integration ===')
    all_ok = True
    for k, v in checks.items():
        status = 'OK' if v else 'MISSING'
        if not v:
            all_ok = False
        print('  {}: {}'.format(k, status))
    print('  ALL: {}'.format('PASSED' if all_ok else 'FAILED'))

print('\n=== ALL VERIFICATIONS COMPLETE ===')
import bpy
import os

# 使用用户主目录
output_dir = '/home/xray4668/blender_project'
os.makedirs(output_dir, exist_ok=True)

with open(os.path.join(output_dir, 'blender_log.txt'), 'w') as f:
    f.write('Blender started\n')
    f.write('Version: ' + str(bpy.app.version) + '\n')
    f.write('Objects: ' + str(len(bpy.data.objects)) + '\n')
    for obj in bpy.data.objects:
        f.write('  ' + obj.name + ' | ' + str(obj.type) + '\n')
        if obj.type == 'MESH':
            f.write('    Vertices: ' + str(len(obj.data.vertices)) + '\n')
        if obj.type == 'ARMATURE':
            f.write('    Bones: ' + str(len(obj.data.bones)) + '\n')
    f.write('Script completed\n')

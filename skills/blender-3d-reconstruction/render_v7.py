import bpy
import os

output_dir = '/home/xray4668/blender_project'
os.makedirs(output_dir, exist_ok=True)

# 打开场景
bpy.ops.wm.open_mainfile(filepath=os.path.join(output_dir, 'character_v7'))

# 使用 Workbench 渲染器（更稳定）
bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'

# 设置相机
cam = bpy.data.objects.get('Camera')
if not cam:
    cam = bpy.data.objects.new('Camera', bpy.data.cameras.new('Camera'))
    bpy.context.collection.objects.link(cam)
cam.location = (5, -5, 3)
cam.rotation_euler = (0.8, 0, 0.5)
bpy.context.scene.camera = cam

# 设置渲染分辨率
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 768
bpy.context.scene.render.resolution_percentage = 100

# 设置输出路径
output_path = os.path.join(output_dir, 'character_v7_render.png')
bpy.context.scene.render.filepath = output_path

# 渲染
bpy.ops.render.render(write_still=True)

print('RENDER_COMPLETE')
print('Output:', output_path)

# 输出场景信息
with open(os.path.join(output_dir, 'scene_info_v7.txt'), 'w') as f:
    f.write('=== SCENE INFO ===\n')
    f.write('Objects: ' + str(len(bpy.data.objects)) + '\n\n')
    for obj in bpy.data.objects:
        f.write('  ' + obj.name + ' | ' + str(obj.type) + '\n')
        if obj.type == 'MESH':
            f.write('    Vertices: ' + str(len(obj.data.vertices)) + '\n')
            f.write('    Faces: ' + str(len(obj.data.polygons)) + '\n')
        elif obj.type == 'ARMATURE':
            f.write('    Bones: ' + str(len(obj.data.bones)) + '\n')
    f.write('\n=== END ===\n')

print('INFO_SAVED')

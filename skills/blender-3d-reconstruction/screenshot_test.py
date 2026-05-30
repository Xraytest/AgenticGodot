import bpy
import os

output_dir = '/home/xray4668/blender_project'
os.makedirs(output_dir, exist_ok=True)

# 打开场景
bpy.ops.wm.open_mainfile(filepath=os.path.join(output_dir, 'character_v7'))

# 设置相机视角
cam = bpy.data.objects.get('Camera')
if cam:
    cam.location = (3, -3, 2)
    cam.rotation_euler = (1.0, 0, 0.7)

# 方法 1: 使用图像模块保存视图
# 创建新图像
img = bpy.data.images.new('ViewportShot', width=1024, height=1024)

# 尝试使用 gl 读取
try:
    import bpy_extras.view3d_utils
    img.save_render(os.path.join(output_dir, 'viewport_capture.png'))
    print('VIEWPORT_CAPTURE_OK')
except Exception as e:
    print('VIEWPORT_ERROR:', str(e))

# 方法 2: 输出场景信息到文件
with open(os.path.join(output_dir, 'scene_info.txt'), 'w') as f:
    f.write('=== SCENE INFO ===\n')
    f.write('Objects: ' + str(len(bpy.data.objects)) + '\n\n')
    for obj in bpy.data.objects:
        f.write('  ' + obj.name + ' | ' + str(obj.type) + '\n')
        if obj.type == 'MESH':
            f.write('    Vertices: ' + str(len(obj.data.vertices)) + '\n')
            f.write('    Faces: ' + str(len(obj.data.polygons)) + '\n')
        elif obj.type == 'ARMATURE':
            f.write('    Bones: ' + str(len(obj.data.bones)) + '\n')
            for bone in obj.data.bones:
                f.write('      - ' + bone.name + '\n')
    f.write('\n=== END ===\n')

print('INFO_SAVED')

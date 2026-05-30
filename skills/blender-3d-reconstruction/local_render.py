
import bpy
import os

# 设置输出目录
output_dir = r'C:/Users/xray/Documents/ArkStudio/AgenticGodot/skills/blender-3d-reconstruction/screenshots'
os.makedirs(output_dir, exist_ok=True)

# 设置渲染参数
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 1024
bpy.context.scene.render.filepath = os.path.join(output_dir, 'iteration_8_render')

# 设置相机
cam = bpy.data.objects.get('Camera')
if cam:
    cam.location = (3, -3, 2)
    cam.rotation_euler = (1.0, 0, 0.7)

# 渲染
bpy.ops.render.render(write_still=True)
print('RENDER_COMPLETE')

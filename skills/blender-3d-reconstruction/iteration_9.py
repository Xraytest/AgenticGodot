import bpy
import os
import math

output_dir = '/home/xray4668/blender_project'
os.makedirs(output_dir, exist_ok=True)

# 清除默认对象
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print('=== ITERATION 9: Create More Human-like Character ===')

# ============ 创建头部 (更真实的人头形状) ============
# 使用 UV 球体并缩放成椭圆形 (减少分段数以降低复杂度)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.12, segments=16, ring_count=12, location=(0, 0.85, 1.55))
head = bpy.context.active_object
head.name = 'Head'
# 缩放成更真实的人头比例（上下略长，前后略扁）
head.scale = (0.95, 0.9, 1.15)
# 应用缩放
bpy.ops.object.transform_apply(scale=True)
print(f'Head created: {len(head.data.vertices)} vertices, {len(head.data.polygons)} faces')

# ============ 创建颈部 ============
bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.15, vertices=16, location=(0, 0.75, 1.25))
neck = bpy.context.active_object
neck.name = 'Neck'
print(f'Neck created: {len(neck.data.vertices)} vertices')

# ============ 创建躯干 (有肩膀宽度和腰部收缩) ============
# 上半身（胸部）
bpy.ops.mesh.primitive_cylinder_add(radius=0.14, depth=0.25, vertices=16, location=(0, 0.55, 1.1))
chest = bpy.context.active_object
chest.name = 'Chest'
# 稍微压扁前后，加宽左右（肩膀）
chest.scale = (1.15, 0.85, 1.0)
bpy.ops.object.transform_apply(scale=True)
print(f'Chest created: {len(chest.data.vertices)} vertices')

# 下半身（腰部/臀部）
bpy.ops.mesh.primitive_cylinder_add(radius=0.11, depth=0.2, vertices=16, location=(0, 0.35, 0.75))
waist = bpy.context.active_object
waist.name = 'Waist'
# 臀部略宽
waist.scale = (1.1, 0.9, 1.05)
bpy.ops.object.transform_apply(scale=True)
print(f'Waist created: {len(waist.data.vertices)} vertices')

# ============ 创建左臂 (分上臂和前臂) ============
# 左上臂
bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.22, vertices=12, location=(-0.22, 0.65, 1.15))
left_upper_arm = bpy.context.active_object
left_upper_arm.name = 'LeftUpperArm'
left_upper_arm.rotation_euler = (math.pi/2, 0, 0)
# 应用旋转
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
print(f'LeftUpperArm created')

# 左前臂
bpy.ops.mesh.primitive_cylinder_add(radius=0.038, depth=0.2, vertices=12, location=(-0.38, 0.65, 1.15))
left_lower_arm = bpy.context.active_object
left_lower_arm.name = 'LeftLowerArm'
left_lower_arm.rotation_euler = (math.pi/2, 0, 0)
# 应用旋转
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
print(f'LeftLowerArm created')

# ============ 创建右臂 ============
# 右上臂
bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.22, vertices=12, location=(0.22, 0.65, 1.15))
right_upper_arm = bpy.context.active_object
right_upper_arm.name = 'RightUpperArm'
right_upper_arm.rotation_euler = (math.pi/2, 0, 0)
# 应用旋转
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
print(f'RightUpperArm created')

# 右前臂
bpy.ops.mesh.primitive_cylinder_add(radius=0.038, depth=0.2, vertices=12, location=(0.38, 0.65, 1.15))
right_lower_arm = bpy.context.active_object
right_lower_arm.name = 'RightLowerArm'
right_lower_arm.rotation_euler = (math.pi/2, 0, 0)
# 应用旋转
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
print(f'RightLowerArm created')

# ============ 创建左腿 (分大腿和小腿) ============
# 左大腿
bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.3, vertices=16, location=(-0.07, 0.25, 0.45))
left_thigh = bpy.context.active_object
left_thigh.name = 'LeftThigh'
print(f'LeftThigh created: {len(left_thigh.data.vertices)} vertices')

# 左小腿
bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.35, vertices=12, location=(-0.07, 0.25, 0.05))
left_shin = bpy.context.active_object
left_shin.name = 'LeftShin'
print(f'LeftShin created: {len(left_shin.data.vertices)} vertices')

# ============ 创建右腿 ============
# 右大腿
bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.3, vertices=16, location=(0.07, 0.25, 0.45))
right_thigh = bpy.context.active_object
right_thigh.name = 'RightThigh'
print(f'RightThigh created: {len(right_thigh.data.vertices)} vertices')

# 右小腿
bpy.ops.mesh.primitive_cylinder_add(radius=0.045, depth=0.35, vertices=12, location=(0.07, 0.25, 0.05))
right_shin = bpy.context.active_object
right_shin.name = 'RightShin'
print(f'RightShin created: {len(right_shin.data.vertices)} vertices')

# ============ 创建骨骼系统 ============
print('\n=== Creating Armature ===')
bpy.ops.object.armature_add(location=(0, 0.5, 0.8))
armature = bpy.context.active_object
armature.name = 'Armature'
armature_data = armature.data

# 进入编辑模式
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='EDIT')

# 创建骨骼
bones = {}

# 根骨骼
bones['Root'] = armature_data.edit_bones.new('Root')
bones['Root'].head = (0, 0.5, 0)
bones['Root'].tail = (0, 0.5, 0.15)

# 髋部
bones['Hips'] = armature_data.edit_bones.new('Hips')
bones['Hips'].head = (0, 0.5, 0.15)
bones['Hips'].tail = (0, 0.5, 0.45)
bones['Hips'].parent = bones['Root']

# 脊柱
bones['Spine'] = armature_data.edit_bones.new('Spine')
bones['Spine'].head = (0, 0.5, 0.45)
bones['Spine'].tail = (0, 0.5, 0.9)
bones['Spine'].parent = bones['Hips']

# 胸部
bones['Chest'] = armature_data.edit_bones.new('Chest')
bones['Chest'].head = (0, 0.5, 0.9)
bones['Chest'].tail = (0, 0.5, 1.15)
bones['Chest'].parent = bones['Spine']

# 颈部
bones['Neck'] = armature_data.edit_bones.new('Neck')
bones['Neck'].head = (0, 0.5, 1.15)
bones['Neck'].tail = (0, 0.5, 1.35)
bones['Neck'].parent = bones['Chest']

# 头部
bones['Head'] = armature_data.edit_bones.new('Head')
bones['Head'].head = (0, 0.5, 1.35)
bones['Head'].tail = (0, 0.5, 1.65)
bones['Head'].parent = bones['Neck']

# 左肩
bones['LeftShoulder'] = armature_data.edit_bones.new('LeftShoulder')
bones['LeftShoulder'].head = (-0.12, 0.5, 1.15)
bones['LeftShoulder'].tail = (-0.22, 0.5, 1.15)
bones['LeftShoulder'].parent = bones['Chest']

# 左上臂
bones['LeftUpperArm'] = armature_data.edit_bones.new('LeftUpperArm')
bones['LeftUpperArm'].head = (-0.22, 0.5, 1.15)
bones['LeftUpperArm'].tail = (-0.44, 0.5, 1.15)
bones['LeftUpperArm'].parent = bones['LeftShoulder']

# 左前臂
bones['LeftLowerArm'] = armature_data.edit_bones.new('LeftLowerArm')
bones['LeftLowerArm'].head = (-0.44, 0.5, 1.15)
bones['LeftLowerArm'].tail = (-0.64, 0.5, 1.15)
bones['LeftLowerArm'].parent = bones['LeftUpperArm']

# 右手臂
bones['RightShoulder'] = armature_data.edit_bones.new('RightShoulder')
bones['RightShoulder'].head = (0.12, 0.5, 1.15)
bones['RightShoulder'].tail = (0.22, 0.5, 1.15)
bones['RightShoulder'].parent = bones['Chest']

# 右上臂
bones['RightUpperArm'] = armature_data.edit_bones.new('RightUpperArm')
bones['RightUpperArm'].head = (0.22, 0.5, 1.15)
bones['RightUpperArm'].tail = (0.44, 0.5, 1.15)
bones['RightUpperArm'].parent = bones['RightShoulder']

# 右前臂
bones['RightLowerArm'] = armature_data.edit_bones.new('RightLowerArm')
bones['RightLowerArm'].head = (0.44, 0.5, 1.15)
bones['RightLowerArm'].tail = (0.64, 0.5, 1.15)
bones['RightLowerArm'].parent = bones['RightUpperArm']

# 左大腿
bones['LeftThigh'] = armature_data.edit_bones.new('LeftThigh')
bones['LeftThigh'].head = (-0.07, 0.5, 0.3)
bones['LeftThigh'].tail = (-0.07, 0.5, 0.0)
bones['LeftThigh'].parent = bones['Hips']

# 左小腿
bones['LeftShin'] = armature_data.edit_bones.new('LeftShin')
bones['LeftShin'].head = (-0.07, 0.5, 0.0)
bones['LeftShin'].tail = (-0.07, 0.5, -0.35)
bones['LeftShin'].parent = bones['LeftThigh']

# 右大腿
bones['RightThigh'] = armature_data.edit_bones.new('RightThigh')
bones['RightThigh'].head = (0.07, 0.5, 0.3)
bones['RightThigh'].tail = (0.07, 0.5, 0.0)
bones['RightThigh'].parent = bones['Hips']

# 右小腿
bones['RightShin'] = armature_data.edit_bones.new('RightShin')
bones['RightShin'].head = (0.07, 0.5, 0.0)
bones['RightShin'].tail = (0.07, 0.5, -0.35)
bones['RightShin'].parent = bones['RightThigh']

# 退出编辑模式
bpy.ops.object.mode_set(mode='OBJECT')

print(f'Armature created with {len(armature_data.bones)} bones')

# ============ 为每个网格添加 Armature Modifier ============
print('\n=== Adding Armature Modifiers ===')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        modifier = obj.modifiers.new(name='ArmatureMod', type='ARMATURE')
        modifier.object = armature
        modifier.use_vertex_groups = True
        print(f'Added Armature Modifier to: {obj.name}')

# ============ 保存场景 ============
bpy.ops.wm.save_mainfile(filepath=os.path.join(output_dir, 'character_v9'))
print('\n=== SCENE SAVED ===')

# ============ 输出统计 ============
print('\n=== SUMMARY ===')
print(f'Total objects: {len(bpy.data.objects)}')
mesh_count = sum(1 for o in bpy.data.objects if o.type == 'MESH')
print(f'Mesh objects: {mesh_count}')
print(f'Armature bones: {len(armature_data.bones)}')

# ============ 导出数据为 JSON ============
print('\n=== Exporting to JSON ===')

import json

def matrix_to_list(matrix):
    return [[m for m in row] for row in matrix]

def export_object(obj):
    location = obj.location
    rotation = obj.rotation_euler
    scale = obj.scale

    vertices = []
    for vert in obj.data.vertices:
        vertices.append(list(vert.co))

    faces = []
    for poly in obj.data.polygons:
        faces.append(list(poly.vertices))

    return {
        'name': obj.name,
        'location': list(location),
        'rotation': list(rotation),
        'scale': list(scale),
        'vertices': vertices,
        'faces': faces
    }

def export_armature(arm):
    bones = []
    for bone in arm.data.bones:
        bones.append({
            'name': bone.name,
            'head': list(bone.head),
            'tail': list(bone.tail)
        })
    return {'bones': bones}

data = {
    'version': '9',
    'objects': [],
    'armature': None
}

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        data['objects'].append(export_object(obj))
    elif obj.type == 'ARMATURE':
        data['armature'] = export_armature(obj)

json_path = os.path.join(output_dir, 'character_v9_data.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f'JSON exported: {json_path}')
print(f'Total vertices: {sum(len(o["vertices"]) for o in data["objects"])}')
print(f'Total faces: {sum(len(o["faces"]) for o in data["objects"])}')

import bpy
import os

output_dir = '/home/xray4668/blender_project'
os.makedirs(output_dir, exist_ok=True)

# 清除默认对象
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print('=== ITERATION 7: Create Base Meshes and Armature ===')

# 创建头部 (UVSphere)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.15, segments=32, ring_count=16, location=(0, 0.9, 0))
head = bpy.context.active_object
head.name = 'Head'
print('Head created:', len(head.data.vertices), 'vertices')

# 创建躯干 (Cylinder)
bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.3, vertices=16, location=(0, 0.5, 0))
torso = bpy.context.active_object
torso.name = 'Torso'
print('Torso created:', len(torso.data.vertices), 'vertices')

# 创建左臂
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.25, vertices=8, location=(-0.15, 0.65, 0))
left_arm = bpy.context.active_object
left_arm.name = 'LeftArm'
import math
left_arm.rotation_euler[0] = math.pi/2
print('LeftArm created')

# 创建右臂
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.25, vertices=8, location=(0.15, 0.65, 0))
right_arm = bpy.context.active_object
right_arm.name = 'RightArm'
right_arm.rotation_euler[0] = math.pi/2
print('RightArm created')

# 创建左腿
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.35, vertices=8, location=(-0.08, 0.15, 0))
left_leg = bpy.context.active_object
left_leg.name = 'LeftLeg'
print('LeftLeg created')

# 创建右腿
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.35, vertices=8, location=(0.08, 0.15, 0))
right_leg = bpy.context.active_object
right_leg.name = 'RightLeg'
print('RightLeg created')

# 创建骨骼系统
print('\n=== Creating Armature ===')
bpy.ops.object.armature_add(location=(0, 0.5, 0))
armature = bpy.context.active_object
armature.name = 'Armature'
armature_data = armature.data

# 进入编辑模式
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='EDIT')

# 创建骨骼
bones = {}
bones['Root'] = armature_data.edit_bones.new('Root')
bones['Root'].head = (0, 0.5, 0)
bones['Root'].tail = (0, 0.5, 0.1)

bones['Hips'] = armature_data.edit_bones.new('Hips')
bones['Hips'].head = (0, 0.5, 0.1)
bones['Hips'].tail = (0, 0.5, 0.3)
bones['Hips'].parent = bones['Root']

bones['Spine'] = armature_data.edit_bones.new('Spine')
bones['Spine'].head = (0, 0.5, 0.3)
bones['Spine'].tail = (0, 0.5, 0.6)
bones['Spine'].parent = bones['Hips']

bones['Neck'] = armature_data.edit_bones.new('Neck')
bones['Neck'].head = (0, 0.5, 0.6)
bones['Neck'].tail = (0, 0.5, 0.8)
bones['Neck'].parent = bones['Spine']

bones['Head'] = armature_data.edit_bones.new('Head')
bones['Head'].head = (0, 0.5, 0.8)
bones['Head'].tail = (0, 0.5, 1.0)
bones['Head'].parent = bones['Neck']

# 左臂骨骼
bones['LeftShoulder'] = armature_data.edit_bones.new('LeftShoulder')
bones['LeftShoulder'].head = (-0.1, 0.5, 0.6)
bones['LeftShoulder'].tail = (-0.2, 0.5, 0.6)
bones['LeftShoulder'].parent = bones['Spine']

bones['LeftUpperArm'] = armature_data.edit_bones.new('LeftUpperArm')
bones['LeftUpperArm'].head = (-0.2, 0.5, 0.6)
bones['LeftUpperArm'].tail = (-0.3, 0.5, 0.6)
bones['LeftUpperArm'].parent = bones['LeftShoulder']

bones['LeftLowerArm'] = armature_data.edit_bones.new('LeftLowerArm')
bones['LeftLowerArm'].head = (-0.3, 0.5, 0.6)
bones['LeftLowerArm'].tail = (-0.4, 0.5, 0.6)
bones['LeftLowerArm'].parent = bones['LeftUpperArm']

bones['LeftHand'] = armature_data.edit_bones.new('LeftHand')
bones['LeftHand'].head = (-0.4, 0.5, 0.6)
bones['LeftHand'].tail = (-0.45, 0.5, 0.6)
bones['LeftHand'].parent = bones['LeftLowerArm']

# 右臂骨骼
bones['RightShoulder'] = armature_data.edit_bones.new('RightShoulder')
bones['RightShoulder'].head = (0.1, 0.5, 0.6)
bones['RightShoulder'].tail = (0.2, 0.5, 0.6)
bones['RightShoulder'].parent = bones['Spine']

bones['RightUpperArm'] = armature_data.edit_bones.new('RightUpperArm')
bones['RightUpperArm'].head = (0.2, 0.5, 0.6)
bones['RightUpperArm'].tail = (0.3, 0.5, 0.6)
bones['RightUpperArm'].parent = bones['RightShoulder']

bones['RightLowerArm'] = armature_data.edit_bones.new('RightLowerArm')
bones['RightLowerArm'].head = (0.3, 0.5, 0.6)
bones['RightLowerArm'].tail = (0.4, 0.5, 0.6)
bones['RightLowerArm'].parent = bones['RightUpperArm']

bones['RightHand'] = armature_data.edit_bones.new('RightHand')
bones['RightHand'].head = (0.4, 0.5, 0.6)
bones['RightHand'].tail = (0.45, 0.5, 0.6)
bones['RightHand'].parent = bones['RightLowerArm']

# 左腿骨骼
bones['LeftThigh'] = armature_data.edit_bones.new('LeftThigh')
bones['LeftThigh'].head = (-0.05, 0.5, 0.1)
bones['LeftThigh'].tail = (-0.05, 0.5, -0.1)
bones['LeftThigh'].parent = bones['Hips']

bones['LeftShin'] = armature_data.edit_bones.new('LeftShin')
bones['LeftShin'].head = (-0.05, 0.5, -0.1)
bones['LeftShin'].tail = (-0.05, 0.5, -0.3)
bones['LeftShin'].parent = bones['LeftThigh']

bones['LeftFoot'] = armature_data.edit_bones.new('LeftFoot')
bones['LeftFoot'].head = (-0.05, 0.5, -0.3)
bones['LeftFoot'].tail = (-0.05, 0.5, -0.4)
bones['LeftFoot'].parent = bones['LeftShin']

# 右腿骨骼
bones['RightThigh'] = armature_data.edit_bones.new('RightThigh')
bones['RightThigh'].head = (0.05, 0.5, 0.1)
bones['RightThigh'].tail = (0.05, 0.5, -0.1)
bones['RightThigh'].parent = bones['Hips']

bones['RightShin'] = armature_data.edit_bones.new('RightShin')
bones['RightShin'].head = (0.05, 0.5, -0.1)
bones['RightShin'].tail = (0.05, 0.5, -0.3)
bones['RightShin'].parent = bones['RightThigh']

bones['RightFoot'] = armature_data.edit_bones.new('RightFoot')
bones['RightFoot'].head = (0.05, 0.5, -0.3)
bones['RightFoot'].tail = (0.05, 0.5, -0.4)
bones['RightFoot'].parent = bones['RightShin']

# 退出编辑模式
bpy.ops.object.mode_set(mode='OBJECT')

print('Armature created with', len(armature_data.bones), 'bones')

# 为每个网格添加 Armature Modifier
print('\n=== Adding Armature Modifiers ===')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        modifier = obj.modifiers.new(name='ArmatureMod', type='ARMATURE')
        modifier.object = armature
        modifier.use_vertex_groups = True
        print('Added Armature Modifier to:', obj.name)

# 保存场景
bpy.ops.wm.save_mainfile(filepath=os.path.join(output_dir, 'character_v7'))
print('\n=== SCENE SAVED ===')

# 输出统计
print('\n=== SUMMARY ===')
print('Total objects:', len(bpy.data.objects))
mesh_count = sum(1 for o in bpy.data.objects if o.type == 'MESH')
print('Mesh objects:', mesh_count)
print('Armature bones:', len(armature_data.bones))

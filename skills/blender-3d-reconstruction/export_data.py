import bpy
import os
import json

output_dir = '/home/xray4668/blender_project'
os.makedirs(output_dir, exist_ok=True)

# 打开场景
bpy.ops.wm.open_mainfile(filepath=os.path.join(output_dir, 'character_v7'))

# 输出模型数据到 JSON
model_data = {
    'objects': [],
    'armature': None
}

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        mesh_data = {
            'name': obj.name,
            'type': 'MESH',
            'location': list(obj.location),
            'rotation': list(obj.rotation_euler),
            'scale': list(obj.scale),
            'vertices': [],
            'faces': []
        }
        for v in obj.data.vertices:
            mesh_data['vertices'].append(list(v.co))
        for poly in obj.data.polygons:
            mesh_data['faces'].append(list(poly.vertices))
        model_data['objects'].append(mesh_data)
    elif obj.type == 'ARMATURE':
        bone_data = {
            'name': obj.name,
            'type': 'ARMATURE',
            'location': list(obj.location),
            'bones': []
        }
        for bone in obj.data.bones:
            bone_info = {
                'name': bone.name,
                'head': list(bone.head),
                'tail': list(bone.tail),
                'parent': bone.parent.name if bone.parent else None
            }
            bone_data['bones'].append(bone_info)
        model_data['armature'] = bone_data

# 保存 JSON
json_path = os.path.join(output_dir, 'character_v7_data.json')
with open(json_path, 'w') as f:
    json.dump(model_data, f, indent=2)

print('JSON_SAVED:', json_path)
print('Objects:', len(model_data['objects']))
print('Armature bones:', len(model_data['armature']['bones']) if model_data['armature'] else 0)

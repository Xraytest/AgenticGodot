import json
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 读取模型数据
with open(r'C:\Users\xray\Documents\ArkStudio\AgenticGodot\skills\blender-3d-reconstruction\character_v10_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建 3D 可视化
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')

# 颜色映射
colors = {
    'Head': 'red',
    'Neck': 'pink',
    'Chest': 'blue',
    'Waist': 'cyan',
    'LeftUpperArm': 'green',
    'LeftLowerArm': 'lightgreen',
    'RightUpperArm': 'orange',
    'RightLowerArm': 'gold',
    'LeftThigh': 'purple',
    'LeftShin': 'mediumpurple',
    'RightThigh': 'brown',
    'RightShin': 'sienna'
}

# 绘制每个网格
for obj in data['objects']:
    name = obj['name']
    verts = np.array(obj['vertices'])
    faces = obj.get('faces', [])

    # 应用变换
    location = np.array(obj['location'])
    transformed_verts = verts + location

    color = colors.get(name, 'gray')

    # 绘制三角面片（如果有的话）
    if faces:
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        triangles = []
        for face in faces:
            if len(face) == 3:
                triangles.append([transformed_verts[face[0]], transformed_verts[face[1]], transformed_verts[face[2]]])
            elif len(face) > 3:
                # 将多边形三角化
                for i in range(1, len(face) - 1):
                    triangles.append([transformed_verts[face[0]], transformed_verts[face[i]], transformed_verts[face[i+1]]])

        if triangles:
            mesh = Poly3DCollection(triangles, facecolors=color, alpha=0.8, linewidth=0.5, edgecolors='black')
            ax.add_collection3d(mesh)

    # 同时绘制顶点作为参考
    ax.scatter(
        transformed_verts[:, 0],
        transformed_verts[:, 1],
        transformed_verts[:, 2],
        c=color,
        s=2,
        alpha=0.5,
        label=f'{name} ({len(verts)} verts, {len(faces)} faces)' if name not in colors else None
    )

# 绘制骨骼
if data['armature']:
    ax.scatter([0], [0], [0], c='black', s=100, marker='*', label='Armature Origin')

    for bone in data['armature']['bones']:
        head = np.array(bone['head'])
        tail = np.array(bone['tail'])
        ax.plot(
            [head[0], tail[0]],
            [head[1], tail[1]],
            [head[2], tail[2]],
            c='black',
            linewidth=2
        )
        ax.text(head[0], head[1], head[2], bone['name'], fontsize=8)

# 设置标签和标题
ax.set_xlabel('X (Right)')
ax.set_ylabel('Y (Front)')
ax.set_zlabel('Z (Up)')
ax.set_title('Character v10 - 3D Model Visualization (Fixed Limb Positions)')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3)

# 设置相角度
ax.view_init(elev=20, azim=45)

# 保存图像
output_path = r'C:\Users\xray\Documents\ArkStudio\AgenticGodot\skills\blender-3d-reconstruction\screenshots\character_v10_visualization.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f'Visualization saved: {output_path}')

# 显示统计信息
print('\n=== Model Statistics ===')
print(f'Total mesh objects: {len(data["objects"])}')
total_verts = sum(len(obj['vertices']) for obj in data['objects'])
total_faces = sum(len(obj['faces']) for obj in data['objects'])
print(f'Total vertices: {total_verts}')
print(f'Total faces: {total_faces}')
if data['armature']:
    print(f'Total bones: {len(data["armature"]["bones"])}')

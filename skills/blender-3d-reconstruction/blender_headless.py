#!/usr/bin/env python3
"""
Blender 无头模式 3D 重建控制器
完全静默运行，通过 Python 脚本控制 Blender 建模
"""

import paramiko
import time
import os
from pathlib import Path
import json

# 连接配置
HOST = "192.168.1.3"
PORT = 22
USERNAME = "xray4668"
PASSWORD = "18248745"
LOCAL_OUTPUT_DIR = Path(r"C:\Users\xray\Documents\ArkStudio\AgenticGodot\skills\blender-3d-reconstruction")
PROJECT_DIR = "/home/xray4668/blender_project"

class BlenderHeadlessController:
    """Blender 无头模式控制器"""

    def __init__(self):
        self.ssh = None
        self.sftp = None
        self.local_output_dir = LOCAL_OUTPUT_DIR
        self.local_output_dir.mkdir(parents=True, exist_ok=True)
        self.iteration_count = 0
        self.log_file = self.local_output_dir / "reconstruction_log.json"

    def connect(self):
        """连接到远端服务器"""
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=HOST, port=PORT, username=USERNAME, password=PASSWORD)

        # 创建项目目录
        self.ssh.exec_command(f"mkdir -p {PROJECT_DIR}")
        print(f"[连接] 已连接到 {HOST}:{PORT}")
        print(f"[项目] 目录：{PROJECT_DIR}")
        return True

    def disconnect(self):
        """断开连接"""
        if self.ssh:
            self.ssh.close()
            print("[连接] 已断开连接")

    def execute_blender_script(self, script_content, script_name="script.py"):
        """在远端执行 Blender Python 脚本"""
        remote_script = f"{PROJECT_DIR}/{script_name}"

        # 创建临时文件传输脚本
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(script_content)
            local_script = f.name

        try:
            # 传输脚本
            self.sftp = self.ssh.open_sftp()
            self.sftp.put(local_script, remote_script)

            # 执行 Blender 脚本
            cmd = f"box64 /opt/blender/blender --background --python {remote_script}"
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')

            print(f"[Blender] 输出：{output[:500] if output else '无'}")
            if error and "DeprecationWarning" not in error:
                print(f"[Blender] 警告：{error[:200] if error else '无'}")

            return output, error
        finally:
            os.unlink(local_script)

    def save_screenshot(self, remote_path, local_filename=None):
        """从远端传输截图到本地"""
        if local_filename is None:
            timestamp = int(time.time() * 1000)
            local_filename = f"render_{timestamp}.png"

        local_path = self.local_output_dir / local_filename

        try:
            self.sftp = self.ssh.open_sftp()
            self.sftp.get(remote_path, str(local_path))
            print(f"[截图] 已保存：{local_path}")
            return str(local_path)
        except Exception as e:
            print(f"[截图] 传输失败：{e}")
            return None

    def log_iteration(self, iteration_data):
        """记录迭代数据"""
        self.iteration_count += 1

        # 读取现有日志
        log_data = []
        if self.log_file.exists():
            with open(self.log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

        # 添加新记录
        log_data.append({
            "iteration": self.iteration_count,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            **iteration_data
        })

        # 保存日志
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)

        print(f"[日志] 迭代 {self.iteration_count} 已记录")

    def create_new_scene(self):
        """创建新场景"""
        script = """
import bpy

# 清除所有对象
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# 创建新场景
print("新场景已创建")
print(f"当前帧：{bpy.context.scene.frame_current}")
"""
        return self.execute_blender_script(script, "create_scene.py")

    def add_base_mesh(self, mesh_type='UVSphere'):
        """添加基础网格"""
        script = f"""
import bpy

# 添加基础网格
bpy.ops.mesh.add(type='{mesh_type}', radius=1, location=(0, 0, 0))

# 获取活动对象
obj = bpy.context.active_object
print(f"已添加网格：{{obj.name}}, 顶点数：{{len(obj.data.vertices)}}")
"""
        return self.execute_blender_script(script, "add_mesh.py")

    def render_image(self, output_path=None):
        """渲染当前视图"""
        if output_path is None:
            output_path = f"{PROJECT_DIR}/render.png"

        # 确保输出目录存在
        self.ssh.exec_command(f"mkdir -p {PROJECT_DIR}")

        script = f"""
import bpy

# 设置输出路径
bpy.context.scene.render.filepath = "{output_path}"

# 设置渲染引擎
bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'

# 设置输出格式
bpy.context.scene.render.image_settings.file_format = 'PNG'

# 渲染
bpy.ops.render.render(write_still=True)

print(f"RENDER_SUCCESS:{output_path}")
"""
        output, error = self.execute_blender_script(script, "render.py")

        # 检查是否成功
        if "RENDER_SUCCESS" in output:
            # 传输渲染图到本地
            local_path = self.save_screenshot(output_path)
            return local_path
        else:
            print(f"[渲染] 失败：{output}")
            return None

    def get_scene_info(self):
        """获取场景信息"""
        script = """
import bpy

info = {
    "objects": len(bpy.data.objects),
    "meshes": len([o for o in bpy.data.objects if o.type == 'MESH']),
    "active_object": bpy.context.active_object.name if bpy.context.active_object else None,
    "frame": bpy.context.scene.frame_current,
}

for k, v in info.items():
    print(f"{k}: {v}")
"""
        output, _ = self.execute_blender_script(script, "info.py")
        return output

    def save_project(self, filename="project.blend"):
        """保存项目"""
        filepath = f"{PROJECT_DIR}/{filename}"
        script = f"""
import bpy
bpy.ops.wm.save_as_mainfile(filepath="{filepath}", overwrite=True)
print(f"项目已保存：{{filepath}}")
"""
        return self.execute_blender_script(script, "save.py")


def main():
    """测试函数"""
    controller = BlenderHeadlessController()

    try:
        # 连接
        if not controller.connect():
            print("[错误] 连接失败")
            return

        # 创建新场景
        print("\n[测试] 创建新场景...")
        controller.create_new_scene()

        # 添加基础网格
        print("\n[测试] 添加 UV 球体...")
        controller.add_base_mesh('UVSphere')

        # 获取场景信息
        print("\n[测试] 场景信息...")
        print(controller.get_scene_info())

        # 渲染
        print("\n[测试] 渲染视图...")
        render_path = controller.render_image()
        if render_path:
            print(f"[成功] 渲染图：{render_path}")

        # 记录迭代
        controller.log_iteration({
            "action": "create_base_mesh",
            "mesh_type": "UVSphere",
            "status": "success"
        })

        # 保存项目
        print("\n[测试] 保存项目...")
        controller.save_project("test_project.blend")

    finally:
        controller.disconnect()


if __name__ == "__main__":
    main()

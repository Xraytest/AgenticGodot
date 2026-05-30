#!/usr/bin/env python3
"""
VNC 静默截图工具 - Windows 侧完全静默，通过 SSH 在远端执行截图
"""

import paramiko
import time
import os
from pathlib import Path

# 连接配置
HOST = "192.168.1.3"
PORT = 22
USERNAME = "xray4668"
PASSWORD = "18248745"
LOCAL_OUTPUT_DIR = Path(r"C:\Users\xray\Documents\ArkStudio\AgenticGodot\skills\blender-3d-reconstruction\screenshots")

class SilentVNCController:
    """静默 VNC 控制器 - Windows 侧无窗口，通过 SSH 在远端截图"""

    def __init__(self):
        self.ssh = None
        self.sftp = None
        self.local_output_dir = LOCAL_OUTPUT_DIR
        self.local_output_dir.mkdir(parents=True, exist_ok=True)

    def connect(self):
        """连接到远端服务器"""
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=HOST, port=PORT, username=USERNAME, password=PASSWORD)
        print(f"[连接] 已连接到 {HOST}:{PORT}")
        return True

    def disconnect(self):
        """断开连接"""
        if self.ssh:
            self.ssh.close()
            print("[连接] 已断开连接")

    def capture_screenshot(self, output_path=None):
        """
        静默截图 - 在远端执行截图命令，通过 SFTP 传输到本地
        Windows 侧完全静默，不弹出任何窗口
        """
        if output_path is None:
            timestamp = int(time.time() * 1000)
            output_path = self.local_output_dir / f"screenshot_{timestamp}.png"

        remote_file = "/tmp/vnc_screenshot.png"

        # 尝试多种截图方式
        screenshot_methods = [
            # 方法 1: import (ImageMagick)
            f"DISPLAY=:1 import -window root {remote_file} 2>/dev/null",
            # 方法 2: scrot
            f"DISPLAY=:1 scrot -o {remote_file} 2>/dev/null",
            # 方法 3: gnome-screenshot
            f"DISPLAY=:1 gnome-screenshot -f {remote_file} 2>/dev/null",
            # 方法 4: xwd + convert
            f"DISPLAY=:1 xwd -root -display :1 | convert xwd:- {remote_file} 2>/dev/null",
        ]

        success = False
        for i, cmd in enumerate(screenshot_methods, 1):
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()

            if exit_status == 0 and self._remote_file_exists(remote_file):
                print(f"[截图] 方法{i}成功")
                success = True
                break

        if not success:
            print("[截图] 所有方法都失败，尝试安装工具...")
            if self._install_screenshot_tools():
                # 重试 import
                cmd = f"DISPLAY=:1 import -window root {remote_file}"
                stdin, stdout, stderr = self.ssh.exec_command(cmd)
                exit_status = stdout.channel.recv_exit_status()
                if exit_status == 0:
                    print("[截图] 安装后重试成功")
                    success = True

        if success:
            try:
                # 通过 SFTP 传输文件
                self.sftp = self.ssh.open_sftp()
                self.sftp.get(remote_file, str(output_path))

                # 清理远端临时文件
                self.ssh.exec_command(f"rm -f {remote_file}")

                if output_path.exists():
                    size = os.path.getsize(output_path)
                    print(f"[截图] 成功：{output_path} ({size} bytes)")
                    return str(output_path)
                else:
                    print("[截图] 文件传输失败")
                    return None
            except Exception as e:
                print(f"[截图] 传输错误：{e}")
                return None
        else:
            print("[截图] 失败")
            return None

    def _remote_file_exists(self, filepath):
        """检查远端文件是否存在"""
        stdin, stdout, stderr = self.ssh.exec_command(f"test -f {filepath} && echo 'exists'")
        return stdout.read().decode().strip() == 'exists'

    def _install_screenshot_tools(self):
        """安装截图工具"""
        print("[安装] 正在安装 ImageMagick...")
        cmd = 'echo "18248745" | sudo -S apt-get update && echo "18248745" | sudo -S apt-get install -y imagemagick'
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            print("[安装] ImageMagick 安装成功")
            return True
        else:
            print(f"[安装] 失败：{stderr.read().decode()[:200]}")
            return False

    def send_mouse_click(self, x, y, button=1):
        """发送鼠标点击到远端"""
        cmd = f"DISPLAY=:1 xdotool mousemove {x} {y} click {button}"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            print(f"[触控] 点击 ({x}, {y})")
            return True
        return False

    def send_mouse_move(self, x, y):
        """发送鼠标移动"""
        cmd = f"DISPLAY=:1 xdotool mousemove {x} {y}"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.channel.recv_exit_status() == 0

    def send_mouse_drag(self, start_x, start_y, end_x, end_y, button=1):
        """发送鼠标拖拽"""
        cmd = f"DISPLAY=:1 xdotool mousemove {start_x} {start_y} mousedown {button} mousemove {end_x} {end_y} mouseup {button}"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.channel.recv_exit_status() == 0

    def send_key(self, key):
        """发送键盘按键"""
        cmd = f"DISPLAY=:1 xdotool key {key}"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.channel.recv_exit_status() == 0

    def send_text(self, text):
        """发送文本"""
        escaped_text = text.replace("'", "'\\''")
        cmd = f"DISPLAY=:1 xdotool type '{escaped_text}'"
        stdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.channel.recv_exit_status() == 0

    def execute_blender_python(self, python_code):
        """在远端 Blender 中执行 Python 代码"""
        # 将代码写入临时文件
        remote_script = "/tmp/blender_script.py"

        # 传输脚本
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(python_code)
            local_script = f.name

        try:
            self.sftp = self.ssh.open_sftp()
            self.sftp.put(local_script, remote_script)

            # 执行脚本
            cmd = f"DISPLAY=:1 box64 /opt/blender/blender --background --python {remote_script}"
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()

            print(f"[Blender] 输出：{output}")
            if error:
                print(f"[Blender] 错误：{error}")

            return output, error
        finally:
            os.unlink(local_script)
            self.ssh.exec_command(f"rm -f {remote_script}")

    def save_blender_file(self, filepath):
        """保存 Blender 文件"""
        code = f'''
import bpy
bpy.ops.wm.save_as_mainfile(filepath="{filepath}", overwrite=True)
'''
        return self.execute_blender_python(code)

    def get_blender_info(self):
        """获取 Blender 当前场景信息"""
        code = '''
import bpy
print(f"Objects: {len(bpy.data.objects)}")
if bpy.context.active_object:
    print(f"Active: {bpy.context.active_object.name}")
'''
        return self.execute_blender_python(code)


def main():
    """测试函数"""
    controller = SilentVNCController()

    try:
        # 连接
        if not controller.connect():
            print("[错误] 连接失败")
            return

        # 测试截图
        print("\n[测试] 开始截图...")
        screenshot_path = controller.capture_screenshot()

        if screenshot_path:
            print(f"[成功] 截图已保存：{screenshot_path}")
        else:
            print("[失败] 截图失败")

    finally:
        controller.disconnect()


if __name__ == "__main__":
    main()

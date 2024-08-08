# sandbox/manager.py
import uuid
from datetime import datetime, timedelta
import threading

from pbox.sandbox.sand_box import CodeSandBox


class CodeSandBoxManager:
    def __init__(self):
        self.sandboxes = {}  # 存储kernel_id和其对应的sandbox实例
        self.api_key_to_kernel_ids = {}  # 新增：存储API_KEY与kernel_id的映射
        self.idle_kernels = set()  # 跟踪空闲的 kernel_id
        self.lock = threading.Lock()  # 确保线程安全

    def create_sandbox(self, api_key):
        try:
            with self.lock:
                # 检查是否有空闲的 kernel_id 可用
                if self.idle_kernels:
                    kernel_id = self.idle_kernels.pop()  # 从空闲列表中取出一个 kernel_id
                    sandbox = self.sandboxes.get(kernel_id)
                    if sandbox is None:
                        sandbox = CodeSandBox()  # 如果没有找到对应的 sandbox 实例，则创建一个新的
                        self.sandboxes[kernel_id] = sandbox
                else:
                    kernel_id = str(uuid.uuid4())  # 创建新的 kernel_id
                    sandbox = CodeSandBox()
                    self.sandboxes[kernel_id] = sandbox

                # 将新创建的 kernel_id 添加到对应的 API_KEY 列表中
                if api_key not in self.api_key_to_kernel_ids:
                    self.api_key_to_kernel_ids[api_key] = []

                if kernel_id not in self.api_key_to_kernel_ids[api_key]:
                    self.api_key_to_kernel_ids[api_key].append(kernel_id)

                # 设置 4 小时后自动关闭 kernel 的定时器
                timer = threading.Timer(4 * 3600, self.close_sandbox, [api_key, kernel_id])
                timer.daemon = True
                timer.start()
                return kernel_id
        except Exception as e:
            print(str(e))
            return None

    def kernels(self, api_key):
        try:
            kernel_ids = self.api_key_to_kernel_ids.get(api_key, [])
            if not kernel_ids:  # 如果列表为空
                return f"No kernels found for {api_key}. Please create a kernel first."
            return kernel_ids
        except Exception as e:
            print(str(e))
            return None

    def close_sandbox(self, api_key, kernel_id):
        try:
            with self.lock:
                if kernel_id in self.sandboxes:
                    # 空闲列表200个以内，则添加到空闲列表中，否则关闭并删除
                    if len(self.idle_kernels) < 200:
                        self.idle_kernels.add(kernel_id)  # 将 kernel_id 标记为空闲
                    else:
                        sandbox = self.sandboxes.pop(kernel_id, None)
                        if sandbox:
                            sandbox.close()
                            self.api_key_to_kernel_ids[api_key].remove(kernel_id)
                    return True
                else:
                    return f"未找到 {api_key} 对应的 kernel。请先创建一个 kernel。"
        except Exception as e:
            print(str(e))
            return False

    def execute_code(self, api_key, kernel_id, code):
        try:
            if kernel_id in self.sandboxes:
                sandbox = self.sandboxes[kernel_id]
                return sandbox.execute_code(code)
            else:
                return f"No kernels found for {api_key}. Please create a kernel first."
        except Exception as e:
            print(str(e))
            return False

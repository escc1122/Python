import threading

from .config import Config
from .service_interface import CloudServiceInterface


class Singleton(CloudServiceInterface):
    _instance = None
    _lock = threading.Lock()  # 鎖

    def __new__(cls, *args, **kwargs):
        # 第一次檢查 _instance 是否已經存在
        if not cls._instance:
            with cls._lock:  # 獲取鎖，確保只有一個執行緒可以進入此區域
                # 再次檢查 _instance 是否已經存在
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    print("__new__")
        return cls._instance

    def __init__(self, name):
        # 初始化代碼，這部分會在第一次創建時執行
        if not hasattr(Singleton._instance, "_initialized"):
            with Singleton._lock:
                if not hasattr(Singleton._instance, "_initialized"):
                    print("__init__")
                    self.name = name
                    Singleton._instance._initialized = True  # 標記為已初始化


    def show(self):
        return f"{self.name} pwd: {Config.getPwd()}"

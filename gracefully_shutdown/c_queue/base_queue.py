from abc import ABC, abstractmethod

class BaseQueue(ABC):
    """抽象基底類別，定義佇列的通用接口"""

    @abstractmethod
    def put(self, item):
        """放入一個項目到佇列"""
        pass

    @abstractmethod
    def get(self, block=True, timeout=None):
        """從佇列中取出一個項目"""
        pass

    @abstractmethod
    def task_done(self):
        """標記佇列中的任務為完成狀態"""
        pass

    @abstractmethod
    def empty(self) -> bool:
        """檢查佇列是否為空"""
        pass

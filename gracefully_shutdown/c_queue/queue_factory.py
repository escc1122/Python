from gracefully_shutdown.c_queue.base_queue import BaseQueue
from gracefully_shutdown.c_queue.memory_queue import MemoryQueue


# from gracefully_shutdown.queue.redis_queue import RedisQueue


class QueueFactory:
    _queue_classes = {
        "in_memory": MemoryQueue,
        # "redis": RedisQueue,
    }

    _queue_list = []

    @classmethod
    def create_queue(cls, queue_type: str, **kwargs) -> BaseQueue:
        """根據指定類型創建 Queue 實例

        Args:
            queue_type (str): Queue 的類型，例如 'in_memory', 'redis'
            **kwargs: 傳遞給 Queue 的初始化參數

        Returns:
            BaseQueue: 創建的 Queue 實例
        """
        if queue_type not in QueueFactory._queue_classes:
            raise ValueError(f"Unsupported queue type: {queue_type}")

        queue_class = QueueFactory._queue_classes[queue_type]
        queue = queue_class(**kwargs)
        cls._queue_list.append(queue)
        return queue_class(**kwargs)

    @classmethod
    def stop(cls):
        for queue in cls._queue_list:
            queue.put(None)

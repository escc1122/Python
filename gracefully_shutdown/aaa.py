import threading
import time

from gracefully_shutdown.queue.base_queue import BaseQueue
from gracefully_shutdown.queue.queue_factory import QueueFactory

# 註冊內存佇列和 Redis 佇列
queue1 = QueueFactory.create_queue("in_memory")  # 使用內存佇列
queue2 = QueueFactory.create_queue("redis", name="my_queue")  # 使用 Redis 佇列

class StopSignal:
    value = False

    @classmethod
    def set(cls, value: bool):
        cls.value = value

    @classmethod
    def is_set(cls) -> bool:
        return cls.value

def producer(q: BaseQueue):
    for i in range(5):
        time.sleep(1)
        q.put(f"Item {i}")
        print(f"Produced: Item {i}")
    time.sleep(2)
    StopSignal.set(True)
    print("Stop signal set!")

def consumer(q: BaseQueue):
    while True:
        try:
            item = q.get(timeout=0.5)
            print(f"Consumed: {item}")
            q.task_done()
        except Exception:
            if StopSignal.is_set():
                print("Stop signal received, exiting consumer...")
                break

# 使用 queue1 和 queue2
producer_thread = threading.Thread(target=producer, args=(queue1,))
consumer_thread = threading.Thread(target=consumer, args=(queue1,))

producer_thread.start()
consumer_thread.start()

producer_thread.join()
consumer_thread.join()

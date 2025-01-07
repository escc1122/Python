import asyncio

from gracefully_shutdown.queue.base_queue import BaseQueue
from gracefully_shutdown.queue.queue_factory import QueueFactory

# 創建內存佇列和 Redis 佇列
queue1 = QueueFactory.create_queue("in_memory")
queue2 = QueueFactory.create_queue("redis", name="async_queue")

class StopSignal:
    value = False

    @classmethod
    def set(cls, value: bool):
        cls.value = value

    @classmethod
    def is_set(cls) -> bool:
        return cls.value

async def producer(q: BaseQueue):
    for i in range(5):
        await asyncio.sleep(1)
        q.put(f"Item {i}")
        print(f"Produced: {item}")
    await asyncio.sleep(2)
    StopSignal.set(True)
    print("Stop signal set!")

async def consumer(q: BaseQueue):
    while True:
        try:
            item = q.get(timeout=0.5)
            print(f"Consumed: {item}")
            q.task_done()
        except Exception:
            if StopSignal.is_set():
                print("Stop signal received, exiting consumer...")
                break

async def main():
    producer_task = asyncio.create_task(producer(queue2))
    consumer_task = asyncio.create_task(consumer(queue2))

    await producer_task
    await consumer_task

asyncio.run(main())

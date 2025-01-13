import json
import queue
import threading
import time
from datetime import datetime

from redis_queue.redis_queue import RedisQueue

# 創建隊列
q = queue.Queue()
stop_flag = threading.Event()  # 停止旗標

redis_queue = RedisQueue("al_test","al_test_wait")

channel = queue.Queue(maxsize=1)

from pydantic import BaseModel

# 定義 Pydantic 模型
class Data(BaseModel):
    id: str
    count:int
    timestamp:int




def producer():
    i = 0
    while not stop_flag.is_set():
        time.sleep(3)
        data = Data(id=str(i), count=0,timestamp=int(datetime.now().timestamp()))
        a= redis_queue.put(data.model_dump_json())
        print(f"producer item {i}")
        i = i + 1


def redis_consumer(i):
    while not stop_flag.is_set():
        item = redis_queue.get()
        if item is not None:
            name, value = item
            retrieved_data = json.loads(value)

            # 將字典資料轉換回 Pydantic 模型
            data = Data(**retrieved_data)
            print(f"redis_consumer{i}: {data}")
            time.sleep(5)
        # channel.put(item,block=True)
        # channel.join()


# def memory_consumer():
#     while not stop_flag.is_set():
#         try:
#             item = channel.get(timeout=5)
#             time.sleep(1)
#             # channel.task_done()
#             print(f"memory_consumer: {item}")
#         except queue.Empty:
#             continue

threads = []
if __name__ == '__main__':
    # 啟動生產者和消費者
    producer_thread = threading.Thread(target=producer)
    threads.append(producer_thread)

    for thread_id in range(5):
        redis_thread = threading.Thread(target=redis_consumer,args=(thread_id,))
        # threads.append(threading.Thread(target=redis_consumer,args=(thread_id,)))
        threads.append(redis_thread)

    for thread in threads:
        # print(thread)
        thread.start()

    # time.sleep(30)
    # stop_flag.set()  # 設置停止旗標

    # for thread in threads:
    #     # pass
    #     thread.join()  # 等待所有��程完成

    time.sleep(50)

    print("Queue stopped.")

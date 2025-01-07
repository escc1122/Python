# import signal
# import asyncio
# from fastapi import FastAPI
# import uvicorn
#
# app = FastAPI()
#
# # 優雅關機的清理操作
# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Cleaning up resources...")
#     # 可在此進行其他資源清理操作，例如關閉資料庫連接
#
# # 模擬長時間運行的任務
# @app.get("/")
# async def read_root():
#     return {"message": "Hello, World!"}
#
# # 處理關機信號的協程
# def handle_signal(loop):
#     async def shutdown():
#         print("Received shutdown signal, gracefully shutting down...")
#         for task in asyncio.all_tasks(loop):
#             if task is not asyncio.current_task(loop):
#                 task.cancel()
#                 try:
#                     await task
#                 except asyncio.CancelledError:
#                     pass
#         loop.stop()
#
#     return shutdown
#
# @app.on_event("startup")
# async def startup_event():
#     loop = asyncio.get_running_loop()
#     for sig in (signal.SIGINT, signal.SIGTERM):
#         loop.add_signal_handler(sig, lambda: asyncio.create_task(handle_signal(loop)()))
#

import signal
import time
from contextlib import asynccontextmanager
from threading import Thread
from typing import Optional

import uvicorn
from fastapi import FastAPI

from gracefully_shutdown.c_queue.queue_factory import QueueFactory
from gracefully_shutdown.stop_signal import StopSignal


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start")
    # Load the ML model
    startup_event()
    yield
    # Clean up the ML models and release the resources
    shutdown_event()


app = FastAPI(lifespan=lifespan)


# 創建隊列
queue = QueueFactory.create_queue("in_memory")


# 生產者函數
def producer():
    # for i in range(100):  # 模擬持續產生數據
    i = 0
    while StopSignal.is_set():
        time.sleep(1)
        queue.put(f"Item{i}")
        i = i + 1
    # print("Producer stopped.")


# 消費者函數
def consumer():
    while StopSignal.is_set():
        item = queue.get()
        time.sleep(1)
        if item is None:  # 如果收到 None，表示結束
            break
        else:
            print(f"Consumed: {item}")


def consumer2():
    while StopSignal.is_set():
        item = queue.get()
        time.sleep(15)
        if item is None:  # 如果收到 None，表示結束
            break
        else:
            print(f"Consumed2: {item}")


# 啟動執行緒
producer_thread: Optional[Thread] = None
consumer_thread: Optional[Thread] = None
consumer_thread2: Optional[Thread] = None


def shutdown():
    print("Received shutdown signal, gracefully shutting down...")
    StopSignal.set(False)
    QueueFactory.stop()


# @app.on_event("startup")
def startup_event():
    # for sig in (signal.SIGINT, signal.SIGTERM):
    #     shutdown()

    global producer_thread, consumer_thread, consumer_thread2
    producer_thread = Thread(target=producer)
    consumer_thread = Thread(target=consumer)
    consumer_thread2 = Thread(target=consumer2)

    producer_thread.start()
    consumer_thread.start()
    consumer_thread2.start()
    print("Producer and Consumer threads started.")


# @app.on_event("shutdown")
def shutdown_event():
    shutdown()
    print("Shutting down...")
    # StopSignal.set(True)
    #
    # 等待執行緒完成
    if producer_thread and producer_thread.is_alive():
        producer_thread.join()

    if consumer_thread and consumer_thread.is_alive():
        consumer_thread.join()

    if consumer_thread2 and consumer_thread2.is_alive():
        consumer_thread2.join()

    print("All threads stopped gracefully.")


@app.get("/")
def read_root():
    return {"message": "FastAPI Queue Example Running"}


#
# @app.post("/add-item/{item}")
# def add_item(item: str):
#     queue.put(item)
#     return {"message": f"Item '{item}' added to queue."}
#
#
# @app.get("/stop")
# def stop():
#     StopSignal.set(True)
#     return {"message": "Stop signal sent."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

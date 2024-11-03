# main.py
import threading
from logging_context import get_logger
from request_handler import handle_request


# 模擬請求的函數
def simulate_request(thread_id):
    # 獲取 logger 並在未提供 request_id 時自動生成
    logger = get_logger(__name__)

    logger.info(f"Thread {thread_id} - Processing request...")
    handle_request()  # 呼叫處理請求的方法
    logger.info(f"Thread {thread_id} - Completed request")


# 模擬請求的函數,使用者自行產request_id
def simulate_request_with_id(thread_id):
    # 獲取 logger 並在未提供 request_id 時自動生成
    logger = get_logger(__name__,f"request_id {thread_id*10}")

    logger.info(f"Thread {thread_id} - Processing request...")
    handle_request()  # 呼叫處理請求的方法
    logger.info(f"Thread {thread_id} - Completed request")


# 主函數
def main():
    threads = []

    # 創建多個線程來模擬請求
    for i in range(5):  # 模擬 5 個請求
        thread = threading.Thread(target=simulate_request, args=(i,))
        threads.append(thread)
        thread.start()

    for i in range(6,11):  # 模擬 5 個請求
        thread = threading.Thread(target=simulate_request_with_id, args=(i,))
        threads.append(thread)
        thread.start()

    # 等待所有線程完成
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

import uuid
import threading
import time
import logging
from context import request_id_var  # 從 context.py 中導入 request_id_var
from request_handler import handle_request  # 引入處理請求的方法

# 設定日誌配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# 模擬請求的函數
def simulate_request(thread_id):
    # 生成唯一請求 ID
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)  # 設置請求 ID 到上下文變量

    logging.info(f"Thread {thread_id} - Request ID: {request_id} - Processing request...")
    handle_request()  # 呼叫處理請求的方法，不再傳遞 request_id
    logging.info(f"Thread {thread_id} - Completed request with ID: {request_id}")


# 主函數
def main():
    threads = []

    # 創建多個線程來模擬請求
    for i in range(5):  # 模擬 5 個請求
        thread = threading.Thread(target=simulate_request, args=(i,))
        threads.append(thread)
        thread.start()

    # 等待所有線程完成
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()

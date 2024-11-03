# request_handler.py
import logging
import time
from context import request_id_var  # 從 context.py 中導入 request_id_var

# 設定日誌配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def handle_request():
    request_id = request_id_var.get()  # 從 contextvar 獲取請求 ID
    logging.info(f"Handling request with ID: {request_id}")

    # 模擬請求處理
    time.sleep(1)  # 模擬處理時間
    logging.info(f"Request {request_id} handled successfully.")

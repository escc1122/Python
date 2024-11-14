# request_handler.py
import time
from logging_context import get_logger

# 獲取帶有 request_id 格式化的 logger
logger = get_logger(__name__)


def handle_request():
    logger.info("Handling request")

    # 模擬請求處理
    time.sleep(1)  # 模擬處理時間
    logger.info("Request handled successfully.")

    logger.error("Request handled error")

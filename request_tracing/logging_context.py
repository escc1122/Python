# logging_context.py
import logging
import contextvars
import uuid

# 定義 __all__ 來控制匯出
__all__ = ["get_logger"]

# 定義私有的 contextvar 來儲存請求 ID
_request_id_var = contextvars.ContextVar("request_id", default=None)


class RequestIdFilter(logging.Filter):
    """
    日誌過濾器，用於將 request_id 添加到日誌記錄中。
    """

    def filter(self, record):
        # 從上下文變量獲取當前的 request_id，如果沒有則設為 'N/A'
        record.request_id = _request_id_var.get() or "N/A"
        return True


def get_logger(name: str = __name__, request_id: str = None):
    """
    獲取 logger，並將 request_id 添加到日誌格式。
    """
    # 如果 request_id 未提供，嘗試從上下文變量中獲取
    if request_id is None:
        request_id = _request_id_var.get()

    # 如果上下文中也沒有 request_id，則自動生成一個新的
    if request_id is None:
        request_id = str(uuid.uuid4())

    # 設置 request_id 到 context variable
    _request_id_var.set(request_id)

    logger = logging.getLogger(name)
    if not logger.handlers:  # 避免重複添加處理器
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [Request ID: %(request_id)s] - %(message)s')

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.propagate = True

        # 添加 request_id 過濾器
        logger.addFilter(RequestIdFilter())

    return logger

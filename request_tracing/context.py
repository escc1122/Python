# context.py
import contextvars

# 定義一個 contextvar 來儲存請求 ID
request_id_var = contextvars.ContextVar("request_id")

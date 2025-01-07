import redis

from gracefully_shutdown.c_queue.base_queue import BaseQueue


class RedisQueue(BaseQueue):
    def __init__(self, name, redis_host='localhost', redis_port=6379, redis_db=0):
        self._name = name
        self._redis = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

    def put(self, item):
        self._redis.rpush(self._name, item)

    def get(self, block=True, timeout=None):
        if block:
            item = self._redis.blpop(self._name, timeout=timeout)
            return item[1] if item else None
        else:
            return self._redis.lpop(self._name)

    def task_done(self):
        # Redis 無需顯式標記任務完成，這裡可以留空或記錄日志
        pass

    def empty(self) -> bool:
        return self._redis.llen(self._name) == 0

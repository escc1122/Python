# https://python-rq.org/docs/workers/
from rq import Worker
from redis import Redis


# get job and run
def run_worker():
    redis_conn = Redis()
    with redis_conn:
        w = Worker("al_test", connection=redis_conn)
        w.work()


if __name__ == '__main__':
    run_worker()

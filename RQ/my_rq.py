# https://python-rq.org/docs/
from redis import Redis
from rq import Queue
import requests


# get domain ip
def get_ip(url):
    response = requests.get(url).json()
    print(response)
    return response


# send job to queue
def main():
    redis_conn = Redis()
    with redis_conn:
        q = Queue("al_test", connection=redis_conn)
        result = q.enqueue(get_ip, "https://api.ipify.org?format=json")


def test():
    redis_conn = Redis()
    with redis_conn:
        q = Queue("al_test", connection=redis_conn, is_async=False)
        job = q.enqueue(get_ip, "https://api.ipify.org?format=json")
        print(job.result)


if __name__ == '__main__':
    main()

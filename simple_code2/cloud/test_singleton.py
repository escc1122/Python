import unittest
from unittest.mock import patch
import threading

from simple_code2.cloud.singleton import Singleton


class TestSingleton(unittest.TestCase):

    @patch('simple_code2.cloud.config.Config.getPwd', return_value='mocked_password')
    def test_singleton_instance(self, mock_getPwd):
        # 创建第一个 Singleton 实例
        singleton1 = Singleton("First Instance")
        # 创建第二个 Singleton 实例
        singleton2 = Singleton("Second Instance")

        # 验证两个实例是否相同
        self.assertIs(singleton1, singleton2, "Singleton instances are not the same")

        # 验证 show 方法是否返回正确的值
        self.assertEqual(singleton1.show(), f"First Instance pwd: {mock_getPwd()}")
        self.assertEqual(singleton2.show(), f"First Instance pwd: {mock_getPwd()}")

    def test_threading_singleton(self):
        """ 測試多線程情況下單例模式是否線程安全 """
        singleton_ids = []

        def create_singleton():
            singleton_instance = Singleton("test")
            singleton_ids.append(id(singleton_instance))

        threads = []
        for _ in range(1000):
            thread = threading.Thread(target=create_singleton)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # 確保所有線程都獲得了相同的實例
        self.assertEqual(len(set(singleton_ids)), 1, "應該只有一個唯一的實例")


if __name__ == '__main__':
    unittest.main()

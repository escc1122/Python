import configparser

__all__ = ["mysql_config"]

import os

# 讀取設定檔
config = configparser.ConfigParser()
_original_directory = os.getcwd()
os.chdir(os.path.dirname(__file__))
files_read = config.read('config.ini')
os.chdir(_original_directory)
if not files_read:  # 如果檔案清單為空
    print("config.ini 檔案不存在或無法讀取")

# 從設定檔中取得 MySQL 的登入資訊
mysql_config = {
    'host': config['mysql']['host'],
    'user': config['mysql']['user'],
    'password': config['mysql']['password'],
    'database': config['mysql']['database'],
    'port': config['mysql'].getint('port', 3306)
}
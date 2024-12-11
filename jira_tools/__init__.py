import configparser

# 初始化 ConfigParser
config = configparser.ConfigParser()

# 讀取 config.ini 文件
config.read('config.ini')

# 取得 [jira] 部分的參數並使用大寫變數名稱
JIRA_URL = config.get('jira', 'jira_url')
EMAIL = config.get('jira', 'email')
API_TOKEN = config.get('jira', 'api_token')


config.read('account.ini')
account_id_demo = config.get('account_id', 'demo')
account_al = config.get('account_id', 'al')
account_gary = config.get('account_id', 'gary')


from flask import Flask
from route.hello_world import bp as views_bp

# 创建 Flask 应用实例
app = Flask(__name__)

# 注册蓝图
app.register_blueprint(views_bp)

# 启动 Flask 应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5555)

from flask import Blueprint, jsonify

# 创建一个蓝图对象
bp = Blueprint('hello_world', __name__)


@bp.route("/")
def home():
    return "<h1>hello world</h1>"


@bp.route("/hello_world", methods=['GET'])
def get_hello_world():
    return jsonify('{"data":"hello_world"}')

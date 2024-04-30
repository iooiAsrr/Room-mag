from flask import Blueprint, request, Response, jsonify, render_template, redirect
from models import User, House
from settings import db
import json

user_page = Blueprint('user_page', __name__)

@user_page.route('/register', methods=["POST"])
def register():
    # 获取用户的注册信息，包括用户名、密码、邮箱
    name = request.form['username']
    password = request.form['password']
    email = request.form['email']
    # 查询数据库中
    result = User.query.filter(User.name == name).all()
    # 判断用户是否已经注册，如果没有注册在返回的结果中设置Cookie
    if len(result) == 0:
        user = User(name=name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        json_str = json.dumps({'valid': '1', 'msg': user.name})
        res = Response(json_str)  # 实例化的过程中需要给他传入响应内容
        res.set_cookie('name', user.name, 3600 * 2)
        return res
    # 用户名已经被注册过
    # 2021011125-杨高磊
    else:
        return jsonify({'valid': '0', 'msg': '用户已注册！'})


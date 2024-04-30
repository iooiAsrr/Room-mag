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

@user_page.route('/user/<name>')
def user(name):
    # 查询数据库中用户名为name的User类对象
    user = User.query.filter(User.name == name).first()
    # 判断用户是否存在
    if user:   # 该用户存在
        collect_id_str = user.collect_id    # 获取当前用户收藏的房源ID
        if collect_id_str:                  # 若不为空
            collect_id_list = collect_id_str.split(',')
            collect_house_list = []
            # 根据房源ID获取对应的房源对象
            for hid in collect_id_list:
                house = House.query.get(int(hid))
                # 将房源对象添加到列表中
                collect_house_list.append(house)
        else:                     # 若为空
            collect_house_list = []

        seen_id_str = user.seen_id       # 获取当前用户的浏览记录
        if seen_id_str:
            seen_id_list = seen_id_str.split(',')
            seen_house_list = []
            # 根据房源ID获取对应的房源对象
            for hid in seen_id_list:
                house = House.query.get(int(hid))
                seen_house_list.append(house)
        else:
            seen_house_list = []
        return render_template('user_page.html', user=user,
                               collect_house_list=collect_house_list,
                               seen_house_list=seen_house_list)
    else:
        # 重定向到首页
        return redirect('/')
    # 2021011125-杨高磊

@user_page.route('/login', methods=['POST'])
def login():
    # 首先需要获取用户提交的信息用户的名字和密码
    name = request.form['username']
    password = request.form['password']
    # 根据用户名进行校验
    user = User.query.filter(User.name == name).first()
    # 用户名存在的时候
    if user:
        # 判断用户输入的密码是否正确
        if user.password == password:
            # 将响应信息变化成JSON字符串
            result = {'valid': '1', 'msg': user.name}
            result_json = json.dumps(result)
            # 构建返回数据
            res = Response(result_json)
            # 设置Cookie的过期时间
            res.set_cookie('name', user.name, 3600 * 2)
            return res
        else:
            return jsonify({'valid': '0', 'msg': '密码不正确！'})
    # 用户不存在的时候
    else:
        return jsonify({'valid': '0', 'msg': '用户名不正确！'})
# 2021011125-杨高磊
from flask import Blueprint, jsonify
from flask import Blueprint, render_template
from sqlalchemy import func

from models import House

detail_page = Blueprint('detail_page', __name__)
#2021011125-杨高磊
@detail_page.route('/house/<int:hid>')
def detail(hid):
    # 从数据库查询房源ID为hid的房源对象
    house = House.query.get(hid)
    return render_template('detail_page.html', house=house)
# 自定义过滤器，用于处理交通条件有无数据的情况
def deal_traffic_txt(word):
    if len(word) == 0 or word is None:
        return '暂无信息！'
    else:
        return word
detail_page.add_app_template_filter(deal_traffic_txt, 'dealNone')

#2021011125-杨高磊
# 实现户型占比功能
@detail_page.route('/get/piedata/<block>')
def return_pie_data(block):
    result = House.query.with_entities(House.rooms, func.count()).filter(House.block == block).group_by(
        House.rooms).order_by(func.count().desc()).all()
    data = []
    for one_house in result:
        data.append({'name': one_house[0], 'value': one_house[1]})
    return jsonify({'data': data})

#2021011125-杨高磊
# 实现本地区小区数量TOP20功能
@detail_page.route('/get/columndata/<block>')
def return_bar_data(block):
    result = House.query.with_entities(House.address, func.count()).filter(House.block == block).group_by(
        House.address).order_by(func.count().desc()).all()
    name_list = []
    num_list = []
    for addr, num in result:
        residence_name = addr.rsplit('-', 1)[1]
        name_list.append(residence_name)
        num_list.append(num)
    if len(name_list) > 20:
        data = {'name_list_x': name_list[:20], 'num_list_y': num_list[:20]}
    else:
        data = {'name_list_x': name_list, 'num_list_y': num_list}
    return jsonify({'data': data})
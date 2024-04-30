from flask import Blueprint, request, render_template

from models import House

import math
# 创建蓝图对象
list_page = Blueprint('list_page', __name__)

# 2021011125-杨高磊
@list_page.route('/query')
def search_txt_info():
    # 获取addr地区字段的查询
    if request.args.get('addr'):
        addr = request.args.get('addr')
        result = House.query.filter(House.address == addr).order_by(House.publish_time.desc()).all()
        return render_template('search_list.html.bp', house_list=result)

    # 获取rooms户型字段的查询
    if request.args.get('rooms'):
        rooms_info = request.args.get('rooms')
        result = House.query.filter(House.rooms == rooms_info).order_by(House.publish_time.desc()).all()
        return render_template('search_list.html.bp', house_list=result)
        return redirect(url_for('index_page.index'))
#2021011125-杨高磊
@list_page.route('/list/pattern/<int:page>')
def return_new_list(page):
    # 获取房源总数量
    house_num = House.query.count()
    # 计算总的页码数，向上取整
    total_num = math.ceil(house_num / 10)
    result = House.query.order_by(
        House.publish_time.desc()).paginate(page = page, per_page=10)
    return render_template('list.html', house_list=result.items, page_num=result.page, total_num=total_num)
#2021011125-杨高磊
@list_page.route('/list/hot_house/<int:page>')
def return_hot_list(page):
    # 获取房源总数量
    house_num = House.query.count()
    # 计算总的页码数，向上取整
    total_num = math.ceil(house_num / 10)
    result = House.query.order_by(
        House.page_views.desc()).paginate(page = page, per_page=10)
    return render_template('list.html', house_list=result.items, page_num=result.page, total_num=total_num)













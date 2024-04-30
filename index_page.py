from flask import Blueprint, render_template
from models import House

# 创建蓝图，蓝图的名称为包的名称index_page
index_page = Blueprint('index_page', __name__)

# 2021011125杨高磊
@index_page.route('/')
def index():
    # 获取房源总数量
    house_total_num = House.query.count()
    return render_template('index.html', num=house_total_num)

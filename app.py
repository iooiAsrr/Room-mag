from flask import Flask
from settings import Config, db
from models import House
from index_page import index_page
from list_page import list_page
# 2021011125杨高磊
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# @app.route('/')
# def test():
#     # 查询第一条记录
#     first_user = House.query.first()
#     print(first_user)
#     return 'ok'
app.register_blueprint(index_page)
app.register_blueprint(list_page,url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
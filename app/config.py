class DevConfig(object):
    DEBUG = True
    SECRET_KEY = 'abcd'
    UPLOAD_FOLDER = 'warehouse'
    ''' mysql'''
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:xie7758521@localhost:3306/ai_api'
    # 如果设置成True(默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
    # 这需要额外的内存， 如果不必要的可以禁用它。如果你不显示的调用它，在最新版的运行环境下，会显示警告。
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # 是否显示底层执行的SQL语句
    SQLALCHEMY_ECHO = True


config = DevConfig()
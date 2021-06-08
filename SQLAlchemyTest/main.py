import db
import model
from model import Users
from sqlalchemy.orm import sessionmaker

if __name__ == '__main__':
    engine = db.get_engine()
    model.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    # 创建新User对象:
    new_user = Users(id='6', name='Bob')
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()





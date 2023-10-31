import time
import sys
from threading import Thread
from sqlalchemy import create_engine
from config import DB_URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime

engine = create_engine(DB_URL)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)
    height = Column(Numeric(precision=5, scale=2), nullable=False)
    weight = Column(Numeric(precision=5, scale=2), nullable=False)
    # 记录时间
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # 链接Blood_pressure表
    blood_pressures = relationship('Blood_pressure', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'


class Blood_pressure(Base):
    __tablename__ = 'blood_pressure'
    id = Column(Integer, primary_key=True, autoincrement=True)
    systolic = Column(Numeric(precision=5, scale=2), nullable=False)
    diastolic = Column(Numeric(precision=5, scale=2), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # 链接User
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='blood_pressures')


def rotating_dash():
    while not done_loading:
        for symbol in '|/-\\':
            sys.stdout.write('\r' + 'Connecting ' + symbol)
            sys.stdout.flush()
            time.sleep(0.1)


print("Connecting to the database...")

# 启动旋转横杠动画线程
done_loading = False
loading_thread = Thread(target=rotating_dash)
loading_thread.start()

# 连接数据库
Base.metadata.create_all(engine)

# 标志动画线程完成
done_loading = True

# 等待动画线程退出
loading_thread.join()

sys.stdout.write('\r' + 'Connected to the database!\n')

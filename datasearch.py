import math
import random

from sqlalchemy import create_engine
from datetime import datetime
from config import DB_URL
from models import User, Blood_pressure
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import itchat

DB_Model = {
    'users': 'User',
    'blood_pressure': 'Blood_pressure'
}
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def get_all_table():
    inspector = Inspector.from_engine(engine)
    table_names = inspector.get_table_names()
    return table_names


def user_search_username(username):  # 查
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    return user


def user_search_id(user_id):  # 查
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    return user


# def user_add(userdata):  # 增
#     session = Session()
#     new_user = User(
#         username=userdata.username,
#         age=userdata.age,
#         gender=userdata.gender,
#         height=userdata.height,
#         weight=userdata.weight,
#         systolic=userdata.systolic,
#         diastolic=userdata.diastolic
#     )
#     session.add(new_user)
#     session.commit()


def user_generate(count1, count2):  # 生成数据
    genders = ['male', 'female']
    for i in range(count1):
        session = Session()
        new_user = User(
            username=f'TestUser{random.randint(1000, 9999)}',
            age=random.randint(10, 90),
            gender=genders[math.floor(random.random() + 0.5)],
            height=random.uniform(160, 190),
            weight=random.uniform(40, 80),
        )
        blood_pressure_records = []
        for j in range(count2):
            new_blood_pressure = Blood_pressure(
                systolic=random.uniform(100, 200),
                diastolic=random.uniform(100, 200),
            )
            blood_pressure_records.append(new_blood_pressure)
        new_user.blood_pressures.extend(blood_pressure_records)
        session.add(new_user)
        session.commit()


def user_delete(user):  # 删
    session = Session()
    user = session.query(User).filter(User.username == user.username).first()
    for record in user.blood_pressures:
        session.delete(record)
    session.delete(user)
    session.commit()


def user_delete_record(user, id):  # 删除用户所有记录
    session = Session()
    user = session.query(User).filter(User.username == user.username).first()
    for record in user.blood_pressures:
        if record.id == id:
            session.delete(record)
    session.commit()


def search_user_records(user):  # 搜索用户的血压记录
    blood_pressures = user.blood_pressures
    if blood_pressures:
        return blood_pressures
    else:
        return None


def user_edit(user, username, age, gender, height, weight):  # 查找到目标用户并更改信息
    session = Session()
    user = session.query(User).filter(User.username == user.username).first()
    user.username = username
    user.age = age
    user.gender = gender
    user.height = height
    user.weight = weight
    session.commit()


def blood_pressure_record_edit(user, flag, systolic, diastolic):  # 更改单个血压记录
    session = Session()
    user = session.query(User).filter(User.username == user.username).first()
    for record in user.blood_pressures:
        if record.id == flag:
            record.systolic = systolic
            record.diastolic = diastolic
    session.commit()


def list_all(tabel_name):
    session = Session()
    users = None
    users = session.query(eval(DB_Model[tabel_name])).all()
    return users

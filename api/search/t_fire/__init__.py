from fastapi import APIRouter, Header, Depends

from pydantic.main import BaseModel
from api.search.station import User as StationUser
from api import ok, mysql
from const import tbl__t_fire
from geopy.distance import geodesic
router = APIRouter()



@router.get('/info', summary='首页')
def index():
    userList = [user for user in User.select().order_by(User.start_date.desc())]
    print(userList[1])
    return ok(data={'result': userList})

# 计算事故地点到消防站的直线距离
def getDistance(id):
    station_users = StationUser.select()
    fires = User.select().where(User.id == id)
    f2s_position = []  # 火灾位置离消防站的距离结果列表

    def StrToPoint (a):  # 求坐标值
        if a:
            x, y = a.split(",")
            point = [float(x), float(y)]
            return point


    for fire in fires:
        if not fire.position is None:
            for station in station_users:
                s_x = StrToPoint(station.position)[0]
                s_y = StrToPoint(station.position)[1]
                f_x = StrToPoint(fire.position)[0]
                f_y = StrToPoint(fire.position)[1]
                aa = round(geodesic((s_y,s_x),(f_y,f_x)).km,2)
                f2s_position.append({"id":fire.id,"station": station.name,"address": fire.address,"distance": aa})
    return f2s_position

@router.get('/getDistance/{id}', summary='获取直线距离')
def returnDistance(id:int):
    print('参数form：', id)
    userList = getDistance(id)
    return ok(data={'result': userList})
###################################################################################################################

from peewee import Model, PrimaryKeyField, CharField, IntegerField

class User(Model):
    id = PrimaryKeyField()
    start_date = CharField()
    start_time = CharField()
    main_thing = CharField()
    type = CharField()
    level = CharField()
    position = CharField()
    province = CharField()
    city = CharField()
    address = CharField()

    class Meta:
        database = mysql
        db_table = tbl__t_fire



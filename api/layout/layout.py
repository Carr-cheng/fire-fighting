from peewee import *
from fastapi import APIRouter
from api import mysql, ok
from const import tbl_fire_decisioninfo, tbl_fire_levelinfo, tbl_fire_placeinfo

router = APIRouter()


# 定义表结构
class FireLevelInfo(Model):
    id = AutoField()
    火灾等级 = CharField()

    class Meta:
        database = mysql
        table_name = tbl_fire_levelinfo


class FirePlaceInfo(Model):
    Pcat_id = IntegerField()
    address = CharField()

    class Meta:
        database = mysql
        table_name = tbl_fire_placeinfo


class FireDecisionInfo(Model):
    id = AutoField()
    programme = CharField()
    Alev_id = IntegerField()
    Pcat_id = IntegerField()

    class Meta:
        database = mysql
        table_name = tbl_fire_decisioninfo


# 执行查询
@router.get('/layout', summary='首页')
def get_fire_decision_info():
    query = (FireDecisionInfo
             .select(FireDecisionInfo.programme, FireLevelInfo.火灾等级, FirePlaceInfo.address)
             .join(FireLevelInfo, on=(FireDecisionInfo.Alev_id == FireLevelInfo.id))
             .switch(FireDecisionInfo)
             .join(FirePlaceInfo, on=(FireDecisionInfo.Pcat_id == FirePlaceInfo.Pcat_id))
             )

    # 打印查询生成的SQL语句（可选）
    print(query.sql())
    result = []
    # 输出查询结果
    for record in query:
        result.append({"programme": record.programme, "firelevelinfo": record.firelevelinfo.火灾等级,
                       "fireplaceinfo": record.fireplaceinfo.address})
    print(result)
    return ok(data={'result': result})

@router.get('/layout/firelevelinfo', summary='获取火灾等级')
def get_fire_decision_info():
    query = FireLevelInfo.select(FireLevelInfo.火灾等级).distinct()
    result = []
    for record in query:
        result.append({"firelevelinfo": record.火灾等级})
    return ok(data={'result': result})

@router.get('/layout/fireplaceinfo', summary='获取火灾地点')
def get_fire_decision_info():
    query = FirePlaceInfo.select(FirePlaceInfo.address).distinct()
    result = []
    for record in query:
        result.append({"fireplaceinfo": record.address})
    return ok(data={'result': result})
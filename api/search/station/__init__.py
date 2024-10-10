from fastapi import APIRouter, Header, Depends

from pydantic.main import BaseModel

from api import ok, mysql
from const import tbl__t_stationInfo

router = APIRouter()

class SaveForm(BaseModel):
    id = ''
    district = ''
    address = ''
    position = ''
    name = ''
    tel = ''

class UpdateForm(BaseModel):
    id = ''
    district = ''
    address = ''
    position = ''
    name = ''
    tel = ''


@router.get('/info', summary='首页')
def index():
    userList = [user for user in User.select()]
    #print(userList[1])
    return ok(data={'result': userList})

@router.post('/save', summary='保存')
def save(form:SaveForm):
    print('参数form', form)
    user = User.create(name = form.name, district = form.district,address=form.address,position=form.position,tel=form.tel)
    return ok(data={'op': 'save', 'user':user})

# @router.get('/search/{id}', summary='搜索')
# def search(id: int):
#     print('参数id', id)
#     user = User.get_or_none(User.id == id)
#     print('结果', user.id, user.name, user.age)
#     return ok(data={'op': 'search', 'result':user})

@router.put('/update/{id}', summary='修改')
def update(id:int, form:UpdateForm):
    print('参数id', id, '参数form', form)
    user = User.get_by_id(id)
    user.name = form.name
    user.district = form.district
    user.address = form.address
    user.position = form.position
    user.tel = form.tel
    user.save()
    return ok(data={'op': 'update'})

@router.delete('/delete/{id}', summary='删除')
async def delete(id:int):
    print(id)
    User.delete_by_id(id)
    return ok(data={'op': 'delete'})

###################################################################################################################

from peewee import Model, PrimaryKeyField, CharField, IntegerField

class User(Model):
    id = PrimaryKeyField()
    district = CharField()
    address = CharField()
    position = CharField()
    name = CharField()
    tel = CharField()


    class Meta:
        database = mysql
        db_table = tbl__t_stationInfo



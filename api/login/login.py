from fastapi import APIRouter, Header, Depends, HTTPException
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from peewee import Model, PrimaryKeyField, CharField, IntegerField
from api import ok, mysql
from const import tbl_t_user
import jwt
router = APIRouter()

from pydantic.main import BaseModel

SECRET_KEY = "mySecretkey"
# 数据库配置
class User(Model):
    id = PrimaryKeyField()
    password_hash = CharField()
    username = CharField()



    class Meta:
        database = mysql
        db_table = tbl_t_user

class LoginForm(BaseModel):
    id=''
    password = ''
    username = ''


@router.post('/login',summary='登录')
def login(form:LoginForm):
    username = form.username
    password = form.password

    user= User.select().where(User.username == username)
    print(bool(user))
    if(user):
        for user1 in user:
            if user1 and check_password_hash(user1.password_hash, password):
                token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
                return {"success": True, "message": "登录成功！","token": token}
            else:
                return {"success": False, "message": "登录失败，用户名或密码错误！"}
    else:
        return {"success": False, "message": "登录失败，用户名或密码错误！"}

@router.post('/register', summary="注册")
def register(form:LoginForm):
    username = form.username
    password = form.password
    password_hash = generate_password_hash(password)
    user = User.select().where(User.username == username)
    if (user):
        return {"success": False, "message": "用户名已存在！"}
    else:
        user = User.create(username=username, password_hash=password_hash)
        return {"success": True, "message": "注册成功！",'user':user}




from util.logger import logger


def ok(data={}):
    return {'status':200, 'msg':'', 'data':data,'code':200}

def fail(msg='', data={}):
    return {'status': 400, 'msg': msg, 'data': data,'code':400}

from peewee import *
from const import *
mysql = MySQLDatabase(mysql_db, host=mysql_host, port=3306, user=mysql_user, password=mysql_pwd)
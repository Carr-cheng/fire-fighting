_api_baseurl = 'http://localhost:33333'

# 这里的参数不能修改
mysql_host = 'bvideo'    # 这里的host可以通过修改hosts映射到自己的ip
mysql_port = 3306           # 数据库端口
mysql_db = 'b_video_stat'   # 统一的数据名称 CREATE DATABASE `b-video-stat` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */
mysql_user = 'root'         # 统一的用户名
mysql_pwd = '123456'         # 统一的密码

# 以下是表名称前缀，每个模块一个表前缀


tbl__t_fire = 't_fire'
tbl__t_stationInfo = 'fire_station_info'


tbl__tag_video = 'tag_video_'

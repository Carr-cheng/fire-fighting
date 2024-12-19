# 获取消防站的经纬度信息，并返回给前端。高德api接口请求过慢，
# 或许可以考虑把所有消防站的经纬度信息存入数据库，然后直接从数据库中获取。该部分后续再完善
import requests
from peewee import Model, CharField, fn

from api import mysql


def get_fire_stations(city_code, api_key):
    fire_stations = []
    page = 1
    while True:
        url = f"http://restapi.amap.com/v3/place/text?key={api_key}&keywords=花溪&types=130504&city={city_code}&offset=20&page={page}&output=json"
        response = requests.get(url)
        data = response.json()
        if data.get('status') != '1':
            print("请求失败:", data.get('info'))
            break
        pois = data.get('pois', [])
        if not pois:
            break
        for poi in pois:
            name = poi.get('name')
            location = poi.get('location')
            if name and location:
                lng, lat = location.split(',')
                fire_stations.append({
                    'name': name,
                    'longitude': lng,
                    'latitude': lat
                })
        page += 1
    return fire_stations


def get_cityCode(city,area):
    class AmapAdcodeCitycode(Model):
        cityName = CharField()
        adcode = CharField(primary_key=True)

        class Meta:
            database = mysql
            table_name = 'amap_adcode_citycode'

    # 执行子查询，获取上海的adcode前缀
    shanghai_adcode = (AmapAdcodeCitycode
                      .select(AmapAdcodeCitycode.adcode)
                      .where(AmapAdcodeCitycode.cityName.contains('上海'))
                      .limit(1)
                      .scalar())

    # 处理前缀
    if shanghai_adcode:
        prefix = str(shanghai_adcode)[:3]
    else:
        prefix = ''

    # 主查询，获取cityName包含“宝山”且adcode以prefix开头的记录
    query = (AmapAdcodeCitycode
             .select()
             .where(AmapAdcodeCitycode.cityName.contains('宝山'))
             .where(AmapAdcodeCitycode.adcode.startswith(prefix)))

    # 执行查询
    results = query.execute()
    # 处理结果
    for result in results:
        return result.adcode

    # 关闭数据库连接
# 使用示例
api_key = 'e2137b77732935f64df9278f4b84031c'
city_code = get_cityCode('上海','宝山')# 入参可以在前端设置，通过用户输入获取
print(city_code)
stations = get_fire_stations(city_code, api_key)
for station in stations:
    print(f"名称: {station['name']}, 经度: {station['longitude']}, 纬度: {station['latitude']}")

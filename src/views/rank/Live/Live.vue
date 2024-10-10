<template>
  <div class="app-container">
    <!--      表单-->
    <div style="width: 70%;margin-left: 15%;">
      <el-input v-model="form.name" placeholder="请输入路线名称" style="margin-bottom: 3px;">
        <template slot="prepend"><label style="width: 120px;">路线名称</label></template>
      </el-input>
      <el-input :value="startCoordinateDescription" disabled style="; margin-bottom: 3px;">
        <el-button slot="prepend" style="width: 120px; background: #13ce66; color: white" @click="isStart = true">选择起点</el-button>
      </el-input>
      <el-input :value="endCoordinateDescription" >
        <el-button slot="prepend" style="width: 120px; background: #cc3333; color: white" @click="isStart = false">选择终点</el-button>
      </el-input>
    </div>
    <!--      搜索组件-->
    <div>
      搜索：
      <el-select
        v-model="keywords"
        filterable
        remote
        placeholder="请输入关键词"
        :remote-method="remoteMethod"
        :loading="loading"
        :clearable="true"
        size="mini"
        @change="currentSelect"
        style="width: 500px"
      >
        <el-option
          v-for="item in options"
          :key="item.id"
          :label="item.name"
          :value="item"
          class="one-text"
        >
          <span style="float: left">{{ item.name }}</span>
          <span style="float: right; color: #8492a6; font-size: 13px">{{
              item.district
            }}</span>
        </el-option>
      </el-select>
    </div>
    <!--      地图组件-->
    <div id="guide-map" style="height: 500px;"></div>

  </div>
</template>
<script>
import AMapLoader from "@amap/amap-jsapi-loader";
// 设置安全密钥
window._AMapSecurityConfig = {
  securityJsCode: 'xxxxxxxxxxxxxxxxx',
}
export default {
  mounted() {
    this.initMap();
  },
  data(){
    return {
      //提交表单
      form:{},
      //地图实例
      map: null,
      //路径坐标点集合
      coordinateList: [],
      //起点坐标
      startCoordinate: {lonlat:121.252282,lnglat:31.366108},
      //终点坐标
      endCoordinate: {lonlat:108.320004,lnglat:22.82402},
      //起点坐标描述
      startCoordinateDescription: '经度：请选择起点' + ',     纬度：请选择起点' ,
      //终点坐标描述
      endCoordinateDescription: '经度：请选择终点' + ',     纬度：请选择终点',
      //选择起点
      isStart: true,
      //起点Marker
      startMarker: null,
      //终点Marker
      endMarker: null,
      //搜索点Marker
      searchMarker: null,
      // 搜索提示
      AutoComplete: null,
      // 搜索关键字
      keywords: "",
      // 搜索节流阀
      loading: false,
      // 搜索提示信息
      options: [],

    }
  },
  methods: {
    //初始化地图
    initMap() {
      AMapLoader.reset()
      AMapLoader.load({
        key: '6ceef6e3cda0b91c618e8e8f8d23f87f',
        version: '2.0',   // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
        plugins: ['AMap.AutoComplete', 'AMap.PlaceSearch', 'AMap.Marker'],  // 需要使用的的插件列表
        AMapUI: {
          version: '1.1',
          plugins: []
        }
      }).then((AMap)=>{
        // 初始化地图
        this.map = new AMap.Map('guide-map',{
          viewMode : "2D",  //  是否为3D地图模式
          zoom : 13,   // 初始化地图级别
          center : [106.628201,26.646694], //中心点坐标  广州
          resizeEnable: true,
          willreadoften: true
        });
        //鼠标点击事件
        this.map.on('click', this.clickMapHandler(this.startCoordinate))
        // 搜索提示插件
        this.AutoComplete = new AMap.AutoComplete({ city: "全国" });
      }).catch(e => {
        console.log(e);
      });
    },
    // 点击地图事件
    clickMapHandler(e){
      //选择起点
      console.log("1:"+this.startMarker)
      if (this.isStart){

        if (this.startMarker !== null){
          this.map.remove(this.startMarker)
        }
        this.startCoordinate.lon = e.lonlat
        this.startCoordinate.lat = e.lnglat
        this.startCoordinateDescription = '经度：' + this.startCoordinate.lon + ',     纬度：' + this.startCoordinate.lat

        //标点AMap.Marker
        this.startMarker = new AMapLoader.Marker({
          position: new AMapLoader.LngLat(e.loglat, e.lnglat),   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
          title: '起点',
          label: {
            content: '起点'
          }
        })
        // 将创建的点标记添加到已有的地图实例
        this.map.add(this.startMarker)
      }
      //选择终点
      else {
        if (this.endMarker !== null){
          this.map.remove(this.endMarker)
        }
        this.endCoordinate.lon = e.loglat
        this.endCoordinate.lat = e.lnglat
        this.endCoordinateDescription = '经度：' + this.endCoordinate.lon + ',     纬度：' + this.endCoordinate.lat

        this.endMarker = new AMapLoader.Marker({
          position: new AMapLoader.LngLat(e.loglat, e.lnglat),   // 经纬度对象，也可以是经纬度构成的一维数组[116.39, 39.9]
          title: '终点',
          label: {
            content: '终点'
          }
        })
        this.map.add(this.endMarker)
      }
    },
    // 搜索地址
    remoteMethod(query) {
      if (query !== "") {
        this.loading = true;
        setTimeout(() => {
          this.loading = false;
          this.AutoComplete.search(query, (status, result) => {
            this.options = result.tips;
          });
        }, 200);
      } else {
        this.options = [];
      }
    },
    // 选中提示
    currentSelect(val) {
      // 清空时不执行后面代码
      if (!val) {
        return ;
      }
      // 自动适应显示想显示的范围区域
      this.map.setFitView();
      //清除marker
      if (this.searchMarker){
        this.map.remove(this.searchMarker)
      }
      //设置marker
      this.searchMarker = new AMapLoader.Marker({
        map: this.map,
        position: [val.location.lng, val.location.lat],
      });

      this.keywords = val.name
      //定位
      this.map.setCenter([val.location.lng, val.location.lat])
    }
  }
}
</script>
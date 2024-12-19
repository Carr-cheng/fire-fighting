<template>
  <div class="app-container">
    <!-- 表单 -->
    <div style="width: 70%; margin-left: 15%;">
      <el-input v-model="form.name" placeholder="请输入路线名称" style="margin-bottom: 3px;">
        <template slot="prepend"><label style="width: 120px;">路线名称</label></template>
      </el-input>
      <el-button style="width: 120px; background: #13ce66; color: white" @click="setStartFlag(true)">选择起点</el-button>
      <el-input :value="startCoordinateDescription" disabled style="margin-bottom: 3px;"></el-input>
      <el-button style="width: 120px; background: #cc3333; color: white" @click="setStartFlag(false)">选择终点</el-button>
      <el-input :value="endCoordinateDescription" disabled></el-input>
    </div>
    <!-- 搜索组件 -->
    <div>
      搜索：
      <el-select
        v-model="selectedOption"
        filterable
        remote
        placeholder="请输入关键词"
        :remote-method="remoteMethod"
        :loading="loading"
        :clearable="true"
        size="mini"
        style="width: 500px"
      >
        <el-option
          v-for="item in options"
          :key="item.id"
          :label="item.name"
          :value="item"
        >
          <span style="float: left">{{ item.name }}</span>
          <span style="float: right; color: #8492a6; font-size: 13px">{{ item.district }}</span>
        </el-option>
      </el-select>
    </div>
    <!-- 地图组件 -->
    <div id="guide-map" style="height: 500px;"></div>
  </div>
</template>

<script>
import AMapLoader from "@amap/amap-jsapi-loader";

// 设置安全密钥
window._AMapSecurityConfig = {
  securityJsCode: 'xxxxxxxxxxxxxxxxx',
};

export default {
  mounted() {
    this.initMap();
  },
  data() {
    return {
      form: {},
      map: null,
      coordinateList: [],
      startCoordinate: { lng: null, lat: null },
      endCoordinate: { lng: null, lat: null },
      startCoordinateDescription: '经度：请选择起点, 纬度：请选择起点',
      endCoordinateDescription: '经度：请选择终点, 纬度：请选择终点',
      isStart: true,
      startMarker: null,
      endMarker: null,
      searchMarker: null,
      AutoComplete: null,
      keywords: "",
      loading: false,
      options: [],
      selectedOption: null,
    };
  },
  methods: {
    initMap() {
      AMapLoader.load({
        key: '6ceef6e3cda0b91c618e8e8f8d23f87f',
        version: '2.0',
        plugins: ['AMap.AutoComplete', 'AMap.Marker'],
        AMapUI: {
          version: '1.1',
          plugins: []
        }
      }).then((AMap) => {
        this.map = new AMap.Map('guide-map', {
          viewMode: "2D",
          zoom: 13,
          center: [106.628201, 26.646694],
          resizeEnable: true,
        });

        this.map.on('click', this.clickMapHandler);

        this.AutoComplete = new AMap.AutoComplete({ city: "全国" });
      }).catch(e => {
        console.log(e);
      });
    },
    clickMapHandler(event) {
      const lnglat = event.lnglat;
      console.log('isStart:', this.isStart); // 调试用

      if (this.isStart) {
        if (this.startMarker) {
          this.map.remove(this.startMarker);
        }
        this.startCoordinate.lng = lnglat.lng;
        this.startCoordinate.lat = lnglat.lat;
        this.startCoordinateDescription = `经度：${lnglat.lng}, 纬度：${lnglat.lat}`;

        this.startMarker = new AMap.Marker({
          position: [lnglat.lng, lnglat.lat],
          title: '起点',
          label: { content: '起点' },
        });
        this.map.add(this.startMarker);
      } else {
        if (this.endMarker) {
          this.map.remove(this.endMarker);
        }
        this.endCoordinate.lng = lnglat.lng;
        this.endCoordinate.lat = lnglat.lat;
        this.endCoordinateDescription = `经度：${lnglat.lng}, 纬度：${lnglat.lat}`;

        this.endMarker = new AMap.Marker({
          position: [lnglat.lng, lnglat.lat],
          title: '终点',
          label: { content: '终点' },
        });
        this.map.add(this.endMarker);
      }
    },
    setStartFlag(flag) {
      this.isStart = flag;
    },
    remoteMethod(query) {
      if (query !== "") {
        this.loading = true;
        this.AutoComplete.search(query, (status, result) => {
          this.loading = false;
          this.options = result.tips || [];
        });
      } else {
        this.options = [];
      }
    },
    currentSelect(val) {
      if (!val) return;

      if (this.searchMarker) {
        this.map.remove(this.searchMarker);
      }

      const position = [val.location.lng, val.location.lat];
      this.searchMarker = new AMap.Marker({
        position: position,
      });
      this.map.setCenter(position);
      this.map.add(this.searchMarker);

      this.keywords = val.name;
    },
  },
};
</script>
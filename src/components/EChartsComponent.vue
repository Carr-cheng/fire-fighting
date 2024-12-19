<template>
  <div ref="resizableElement" style="width: 100%; height: 200px;">
    <!-- ECharts 图表 -->
    <div id="chart" style="height: 400px; width: 100%"></div>

    <!-- 标题 -->
    <div class="table-title">消防应急方案表</div>

    <!-- 筛选区域 -->
    <div class="filter-container">
      <span class="filter-label">筛选框：</span>
      <el-select
        v-model="selectedFireLevel"
        placeholder="选择火灾等级"
        @change="filterTable"
        clearable
      >
        <el-option
          v-for="item in fireLevels"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select>

      <el-select
        v-model="selectedFirePlace"
        placeholder="选择火灾地点"
        @change="filterTable"
        clearable
      >
        <el-option
          v-for="item in firePlaces"
          :key="item"
          :label="item"
          :value="item"
        />
      </el-select>
    </div>

    <!-- 表格展示区域 -->
    <el-table
      :data="filteredTableData"
      style="width: 100%; margin-top: 20px"
      border
      height="300"
    >
      <el-table-column prop="programme" label="方案" width="350" />
      <el-table-column prop="firelevelinfo" label="火灾等级" />
      <el-table-column prop="fireplaceinfo" label="起火地点" />
    </el-table>
  </div>
</template>

<script>
import * as echarts from "echarts";
import axios from "axios";
import { throttle } from 'lodash';
import ResizeObserver from 'resize-observer-polyfill';

export default {
  data() {
    return {
      fireLevels: [], // 火灾等级选项
      firePlaces: [], // 火灾地点选项
      selectedFireLevel: "", // 选中的火灾等级
      selectedFirePlace: "", // 选中的火灾地点
      tableData: [], // 原始表格数据
      filteredTableData: [], // 筛选后的表格数据
      resizeObserver: null, // 声明ResizeObserver实例
    };
  },
  mounted() {
    this.initChart();
    this.fetchFilterData(); // 获取筛选数据
    this.fetchTableData(); // 获取表格数据
    const element = this.$refs.resizableElement;
    let lastWidth = null;
    let lastHeight = null;
    const handleResize = throttle((entries) => {
      entries.forEach((entry) => {
        console.log('Element size changed:', entry.contentRect);
        // 处理尺寸变化的逻辑
      });
    }, 200);

    this.resizeObserver = new ResizeObserver(handleResize);
    this.resizeObserver.observe(element);
  },
  beforeUnmount() {
    if (this.resizeObserver) {
      this.resizeObserver.unobserve(this.$refs.resizableElement);
      this.resizeObserver.disconnect();
    }
  },
  methods: {
    // 初始化 ECharts 图表
    initChart() {
      const chartDom = document.getElementById("chart");
      const myChart = echarts.init(chartDom);
      const option = {
        title: {
          text: "消防物资储备量统计",
          left: "center",
        },
        xAxis: {
          type: "category",
          data: ["水罐车", "灭火器", "消防员", "水带"],
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            data: [50, 120, 80, 100],
            type: "bar",
            itemStyle: {
              color: "#73C0DE",
            },
          },
        ],
      };
      myChart.setOption(option);
    },

    // 获取筛选框数据
    fetchFilterData() {
      // 获取火灾等级数据
      axios.get("/layout/firelevelinfo").then((response) => {
        this.fireLevels = response.data.data.result.map((item) => item.firelevelinfo);
      });

      // 获取火灾地点数据
      axios.get("/layout/fireplaceinfo").then((response) => {
        this.firePlaces = response.data.data.result.map((item) => item.fireplaceinfo);
      });
    },

    // 获取表格数据
    fetchTableData() {
      axios.get("/layout").then((response) => {
        this.tableData = response.data.data.result || [];
        this.filteredTableData = this.tableData; // 初始展示所有数据
      });
    },

    // 筛选表格数据
    filterTable: throttle(function() {
      this.filteredTableData = this.tableData.filter((item) => {
        const matchesFireLevel = this.selectedFireLevel
          ? item.firelevelinfo === this.selectedFireLevel
          : true;
        const matchesFirePlace = this.selectedFirePlace
          ? item.fireplaceinfo === this.selectedFirePlace
          : true;
        return matchesFireLevel && matchesFirePlace;
      });
    }),
  },
};
</script>

<style scoped>
.table-title {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  font-weight: bold;
}

.filter-container {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-top: 10px;
}

.filter-label {
  font-size: 14px;
  font-weight: bold;
  margin-right: 10px;
}

.el-select {
  width: 200px;
}
</style>
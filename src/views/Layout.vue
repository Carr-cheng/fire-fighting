<!-- 布局 -->
<template>
  <div class="layout">
    <div class="header"><global-header /></div>
    <div class="main">
      <div class="leftMenu"><global-aside /></div>
      <el-main class="mainContainer">
        <el-scrollbar style="height: 100%; background-color: #fff">
          <router-view />
          <EChartsComponent v-if="shouldShowChart"/>
        </el-scrollbar>
      </el-main>
    </div>
  </div>
</template>

<script>
import bus from "@/store/bus.js";
import GlobalAside from "../components/GlobalAside.vue";
import GlobalHeader from "../components/GlobalHeader.vue";
import EChartsComponent from "@/components/EChartsComponent.vue";

export default {
  name: "",
  data: function () {
    return {};
  },

  components: { EChartsComponent, GlobalAside, GlobalHeader },

  computed: {
    // 通过路由路径判断是否显示 ECharts 图表
    shouldShowChart() {
      // 如果是某些页面路径，则显示图表
      return this.$route.path === '/Layout';  // 请替换为你希望显示图表的页面路径
    },
  },

  mounted: function () {},

  methods: {},

  created() {
    //this.$router.push({ path: "/member/Workbench" });
    bus.on("selectMenu", (menu) => this.$router.push({ path: menu.path }));
  },
};
</script>
<style lang="scss" scoped>
.layout {
  width: 100%;
  min-width: 1200px;
  height: 100%;
  .header {
    height: 64px;
  }
  .main {
    width: 100%;
    height: calc(100% - 64px);
    display: flex;

    .leftMenu {
      width: 200px;
      height: calc(100vh - 64px);
    }

    .mainContainer {
      background-color: RGB(246, 247, 251);
      height: calc(100vh - 64px);
      display: flex;
      flex-direction: column;
      padding: 20px;
    }
  }
}
</style>

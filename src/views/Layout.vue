<!-- 布局 -->
<template>
  <div class="layout">
    <div class="header"><global-header /></div>
    <div class="main">
      <div class="leftMenu"><global-aside /></div>
      <el-main class="mainContainer">
        <el-scrollbar style="height: 100%; background-color: #fff">
          <router-view />
        </el-scrollbar>
      </el-main>
    </div>
  </div>
</template>

<script>
import bus from "@/store/bus.js";
import GlobalAside from "../components/GlobalAside.vue";
import GlobalHeader from "../components/GlobalHeader.vue";

export default {
  name: "",
  data: function () {
    return {};
  },

  components: { GlobalAside, GlobalHeader },

  computed: {},

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
    }
  }
}
</style>

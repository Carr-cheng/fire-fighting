<template>
  <div id="header">
    <div class="l-header">
      <el-button type="primary" icon="el-icon-menu" size="mini"></el-button>
      <el-breadcrumb separator="/">
        <el-breadcrumb-item><font color="white">首页</font></el-breadcrumb-item>
        <el-breadcrumb-item>
          <font color="white">{{ currentMenu.label }}</font>
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div class="r-header">
      <el-dropdown trigger="click">
        <span class="el-dropdown-link"><img :src="userImg" /></span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item icon="el-icon-user">个人信息</el-dropdown-item>
          <el-dropdown-item icon="el-icon-lock">修改密码</el-dropdown-item>
          <el-dropdown-item icon="el-icon-unlock">退出</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import bus from "@/store/bus.js";
export default {
  data() {
    return {
      currentMenu: {},
      userImg: require("../assets/logo.png"),
    };
  },
  computed: {},
  methods: {},
  created() {
    //bus.$off("selectMenu");
    bus.on("selectMenu", (menu) => (this.currentMenu = menu));
  },
};
</script>

<style lang="scss" scoped>
#header {
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: RGB(24, 144, 255);
  .l-header {
    display: flex;
    align-items: center;
    .el-button {
      margin-right: 20px;
    }
  }
  .r-header {
    img {
      width: 40px;
      height: 40px;
      border-radius: 50%;
    }
  }
}
</style>

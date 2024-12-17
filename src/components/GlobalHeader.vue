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
      <el-dropdown @command="handleCommand" trigger="click">
        <span class="el-dropdown-link">
          <img :src="userImg" />
        </span>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile" icon="el-icon-user">个人信息</el-dropdown-item>
            <el-dropdown-item command="changePwd" icon="el-icon-lock">修改密码</el-dropdown-item>
            <el-dropdown-item command="logout" icon="el-icon-unlock">退出</el-dropdown-item>
          </el-dropdown-menu>
        </template>
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
      userImg: require("../assets/logo.png"), // 替换为实际头像路径
    };
  },
  methods: {
    handleCommand(command) {
      if (command === "profile") {
        alert("个人信息功能");
      } else if (command === "changePwd") {
        alert("修改密码功能");
      } else if (command === "logout") {
        localStorage.removeItem("token"); // 示例清除 token
        localStorage.removeItem("userInfo");  // 示例清除用户信息
        // 跳转到登录页面
        this.$router.push("/");
      }
    },
  },
  created() {
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
      cursor: pointer;
    }
  }
}
</style>


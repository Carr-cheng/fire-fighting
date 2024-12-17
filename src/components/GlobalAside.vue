<template>
  <div class="box">
    <el-scrollbar style="height: 100%">
      <el-menu
        background-color="#fff"
        text-color="gray"
        active-text-color="#fb5d87"
        style="height: 100%"
      >
        <template v-for="item in asideMenu">
          <el-menu-item
            :index="item.label"
            v-if="!Object.prototype.hasOwnProperty.call(item, 'children')"
            :key="item.label"
            @click="selectMenu(item)"
          >
            <i :class="item.icon"></i><span slot="title">{{ item.label }}</span>
          </el-menu-item>
          <el-submenu
            :index="item.label"
            v-if="Object.prototype.hasOwnProperty.call(item, 'children')"
            :key="item.label"
          >
            <template slot="title">
              <i :class="item.icon"></i><span>{{ item.label }}</span>
            </template>
            <el-menu-item
              :index="subitem.label"
              v-for="subitem in item.children"
              :key="subitem.label"
              @click="selectMenu(subitem)"
            >
              <i :class="subitem.icon"></i>{{ subitem.label }}
            </el-menu-item>
          </el-submenu>
        </template>
      </el-menu>
    </el-scrollbar>
  </div>

</template>

<script>
import bus from "@/store/bus";
export default {
  props: {},
  data() {
    return {
      asideMenu: [
        { path: "", label: "工作台", icon: "el-icon-s-home" },
        {
          path: "/",
          label: "火灾",
          icon: "el-icon-setting",
          children: [
            {
              path: "/Layout/search/fire",
              label: "火灾情况",
              icon: "el-icon-setting",
            },
            {
              path: "/Layout/dispatch/mapPath",
              label: "路径规划",
              icon: "el-icon-setting",
            },
            {
              path: "/Layout/dispatch/car",
              label: "资源调度",
              icon: "el-icon-setting",
            },
            {
              path: "/Layout/search/station",
              label: "消防站信息",
              icon: "el-icon-setting",
            }
          ],
        },
      ],
    };
  },
  methods: {
      selectMenu(menu) {
        console.log(menu);
        bus.emit("selectMenu", menu);
      },
  },
};
</script>

<style lang="scss" scoped>
#asider {
  height: 100%;
  .el-menu {
    height: 100%;
    border: none;
  }
}
</style>

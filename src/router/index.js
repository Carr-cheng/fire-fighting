// import { Vue } from "vue";
import {createRouter, createWebHistory} from 'vue-router'
import Layout from "../views/Layout.vue";

import search_fire from "./search_fire";
import dispatch_mapPath from "./dispatch_mapPath";
import dispatch_car from "./dispatch_car";
import search_station from "./search_station"
import Login from '../components/LoginForm.vue'; // 引入 Login 组件
import Register from '../components/RegisterForm.vue';


const routes = [

  {
    path: '/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register, // 替换为你的注册页面组件
  },
  {
    path: "/layout",
    name: "Layout",
    component: Layout,
    children: [
      ...search_fire,
      ...dispatch_mapPath,
      ...dispatch_car,
      ...search_station,
    ],
    meta: { requiresAuth: true }, // 添加一个标记，表示需要登录}
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const isLoggedIn = localStorage.getItem("token"); // 检查登录状态，假设通过 token 判断
  console.log(isLoggedIn)
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // 如果目标路由需要登录
    if (!isLoggedIn) {
      // 未登录，跳转到登录页
      next({ path: "/", query: { redirect: to.fullPath } });
    } else {
      // 已登录，允许访问
      next();
    }
  } else {
    // 不需要登录的页面，直接放行
    next();
  }
});
export default router


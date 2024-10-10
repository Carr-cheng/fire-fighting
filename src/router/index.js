// import { Vue } from "vue";
import {createRouter, createWebHistory} from 'vue-router'
import Layout from "../views/Layout.vue";

import search_fire from "./search_fire";
import rank_live from "./rank_live";
import rank_gift from "./rank_gift";
import search_station from "./search_station"


// //获取原型对象上的push函数
// const originalPush = VueRouter.prototype.push;
// //修改原型对象中的push方法
// VueRouter.prototype.push = function push(location) {
//   return originalPush.call(this, location).catch((err) => err);
// };
const routes = [
  {
    path: "/",
    name: "Layout",
    component: Layout,
    children: [
      ...search_fire,
      ...rank_live,
      ...rank_gift,
      ...search_station,
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router


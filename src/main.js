import App from "./App.vue";
import router from "./router";
import store from "./store";

import { createApp } from 'vue';
import "@/plugins/axios.js";
// Vue.prototype.$axios = axios;
// Vue.config.productionTip = false;
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'
// import { BootstrapVue } from "bootstrap-vue";
// 注册全局
import axios from "axios";
axios.defaults.withCredentials = true;


const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(ElementPlus)
app.use(router)
app.use(store)
app.provide('$axios',axios)
app.mount("#app")



axios.defaults.baseURL = 'http://localhost:33333/api/v1/'
// new Vue({
//   router,
//   render: (h) => h(App),
// }).$mount("#app");

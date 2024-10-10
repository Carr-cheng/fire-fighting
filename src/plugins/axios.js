import axios from "axios";

// 创建axios实例
const axios01 = axios.create({
  baseURL: "http://localhost:33333/api/v1/", // api的base_url
  timeout: 5000, // 请求超时时间
});

import NProgress from "nprogress";
import "nprogress/nprogress.css";

axios01.interceptors.request.use(
  (config) => {
    NProgress.start();
    // if (sessionStorage.user) {
    //   config.headers.Authorization = JSON.parse(sessionStorage.user)['token']
    // }
    return config;
  },
  (error) => {
    console.log("axios.js报错", error); // for debug
    return Promise.reject(error);
  }
);

axios01.interceptors.response.use((config) => {
  NProgress.done();
  return config;
});

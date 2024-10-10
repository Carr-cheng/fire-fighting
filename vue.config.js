const { defineConfig } = require("@vue/cli-service");
var path = require("path");
// var webpack = require('webpack')
// 压缩
// const WebpackBar = require("webpackbar");
// const TerserPlugin = require("terser-webpack-plugin");
// // 压缩
// const CompressionPlugin = require("compression-webpack-plugin");
// const productionGzipExtensions = /\.(js|css|json|txt|html|ico|svg)(\?.*)?$/i;

function resolve(dir) {
  return path.join(__dirname, dir);
}
const name = "title"; //项目标题名字
module.exports = {
  publicPath: "/",
  pages: {
    index: {
      // page 的入口
      entry: "src/main.js",
      // 模板来源
      template: "public/index.html",
      // 在 dist/index.html 的输出
      filename: "index.html",
      // 当使用 title 选项时，
      title: "我的地盘我做主",
      // 在这个页面中包含的块，默认情况下会包含
      // 提取出来的通用 chunk 和 vendor chunk。
      chunks: ["chunk-vendors", "chunk-common", "index"],
    },
  },
  devServer: {
    port: 3333,
    open: true,
    proxy: {
        '/api': {
          target: 'http://localhost:33333/',
          changeOrigin: true
        }
    }
  },
  transpileDependencies: true,
  lintOnSave: false,
  outputDir: "dist",
  assetsDir: "assets",
  productionSourceMap: false,


  // 设置css的主入口文件
  css: {
    // css预设器配置项
    // loader: "less-loader",
    loaderOptions: {

      scss: {
        additionalData: '@import "./src/styles/index.scss";', //主入口css文件路径
      },
    },
  },

};

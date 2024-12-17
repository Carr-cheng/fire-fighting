<template>
  <div id="app">
    <!-- 路由占位符 -->
    <router-view></router-view>
  </div>
</template>
<script>
import LoginForm from './components/LoginForm.vue';
export default {
  name: 'app',
  components:{
    LoginForm
  }
}
</script>
<style></style>
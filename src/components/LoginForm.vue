<template>
  <div class="background">
    <div class="login-container">
      <h2>登录</h2>
      <form @submit.prevent="handleLogin">
        <input v-model="username" type="text" placeholder="用户名" required />
        <input v-model="password" type="password" placeholder="密码" required />
        <button type="submit">登录</button>
      </form>
      <button class="register-button" @click="goToRegister">注册</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",
      errorMsg: "",
    };
  },
  methods: {
    async handleLogin() {
     // alert(`用户名: ${this.username}\n密码: ${this.password}`);
      try {
        const response = await axios.post('/login', {
          username: this.username,
          password: this.password
        });
        console.log(response)
        if (response.data && response.data.success) {
          // 登录成功，跳转到首页
          localStorage.setItem("token", response.data.token);
          ElMessage.success("登录成功！");
          this.$router.push("/Layout")
        } else {
          // 后端返回登录失败的信息
          this.errorMsg = response.data.message || "用户名或密码错误";
          ElMessage.error(this.errorMsg);
        }
        // this.message = response.data.message;

      } catch (error) {
        this.errorMsg = "登录失败，请稍后再试！";
        ElMessage.error(this.errorMsg);
        console.error(error);
      }
      // 在这里添加登录逻辑，例如通过 axios 向后端发送请求
    },
    goToRegister() {
      // 跳转到注册页面，可以使用 Vue Router
      this.$router.push("/register"); // 确保 Vue Router 已配置
    },
  },
};
</script>

<style scoped>
/* 背景样式 */
.background {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: url('https://source.unsplash.com/1600x900/?nature,abstract') no-repeat center center fixed;
  background-size: cover;
}

/* 登录框样式 */
.login-container {
  background: rgba(255, 255, 255, 0.9);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

.login-container h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.login-container input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.login-container button {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  background-color: #4CAF50;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-container button:hover {
  background-color: #45a049;
}

.register-button {
  background-color: #2196F3;
  margin-top: 10px;
}

.register-button:hover {
  background-color: #1e88e5;
}
</style>

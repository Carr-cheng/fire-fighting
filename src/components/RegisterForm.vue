<template>
  <div class="background">
    <div class="register-container">
      <h2>注册</h2>
      <form @submit.prevent="handleRegister">
        <input v-model="username" type="text" placeholder="用户名" required />
        <input v-model="password" type="password" placeholder="密码" required />
        <button type="submit">注册</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ElMessage } from "element-plus";

export default {
  name: "Register",
  data() {
    return {
      username: "",
      password: "",
      usernameError: "", // 用户名校验错误信息
      errorMsg: "", // 注册错误信息
    };
  },
  methods: {
    async handleRegister() {
      //alert(`注册信息:\n用户名: ${this.username}\n密码: ${this.password}`);
      // 在这里添加注册逻辑
      try {
        const response = await axios.post('/register', {
          username: this.username,
          password: this.password
        });
        if (response.data && response.data.success) {
          // 登录成功，跳转到首页
          ElMessage.success("注册成功！");
          this.$router.push("/")
        } else {
          // 后端返回登录失败的信息
          this.errorMsg = response.data.message || "用户名或密码错误";
          ElMessage.error(this.errorMsg);
        }
      } catch (error) {
        this.message = "注册失败，请稍后再试！";
      }
    },
  },
};
</script>

<style scoped>
/* 类似于登录页面的样式 */
.background {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: url('https://source.unsplash.com/1600x900/?city') no-repeat center center fixed;
  background-size: cover;
}

.register-container {
  background: rgba(255, 255, 255, 0.9);
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

.register-container h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.register-container input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 16px;
}

.register-container button {
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

.register-container button:hover {
  background-color: #45a049;
}
</style>

<template>
  <div class="container">
    <h1>车辆调度过程</h1>
    <input v-model="query" placeholder="输入查询参数 q" />
    <button @click="fetchData" type="button">获取数据</button>
    <p v-if="loading">加载中...</p>
    <p v-if="error" class="error">{{ error }}</p>
    <img id="fire-fighting-image" :src="imgSrc" @error="handleImageError" alt="灭火过程图" v-if="imgSrc" />
    <div class="data-container" v-if="data">
      <div class="data-item">
        <h2>数据项</h2>
        <p>最小卡车数量: {{ data.min_trucks }}辆  灭火时间: {{ data.time_taken }} 秒      总用水量: {{ data.total_water_used }} 升</p>
        <h3>卡车移动记录</h3>
        <ul>
          <li v-for="(movement, index) in data.movements" :key="index">
            {{ movement.movement }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      imgSrc:'',
      data: {
        min_trucks: 0,
        time_taken: 0,
        total_water_used: 0,
        movements: [],
        imageUrl: null,
      },
     // 假设图片路径是这个
      loading: false,
      error: null
    };
  },
  methods: {
    fetchData() {
      if (!this.query) {
        this.error = '请输入查询参数 q';
        return;
      }
      this.loading = true;
      this.error = null;
      axios.get('/diaodu/'+this.query )
        .then(response => {
          if (Array.isArray(response.data.data.result) && response.data.data.result.length > 0) {

            this.data = response.data.data.result[0];
            console.log(this.data)
            if (this.data.img.startsWith('data:image/png;base64,')) {
              this.imgSrc = this.data.img;
            } else {
              this.imgSrc = 'data:image/png;base64,' + this.data.img;
            }
          } else {
            console.error('数据格式不正确');
            this.error = '数据格式不正确';
          }
        })
        .catch(error => {
          console.error('获取数据失败:', error);
          this.error = '获取数据失败，请重试';
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  handleImageError(event) {
    console.error('图片加载失败', event);
  }
  // created() {
  //   axios.post('/diaodu')
  //     .then(response => {
  //       console.log(
  //         response
  //       )
  //       if (Array.isArray(response.data.data.result) && response.data.data.result.length > 0) {
  //         this.data = response.data.data.result[0];
  //       } else {
  //         console.error('数据格式不正确');
  //       }
  //     })
  //     .catch(error => {
  //       console.error('获取数据失败:', error);
  //     });
  // }
};
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.data-container {
  width: 80%;
}

.data-item {
  border: 1px solid #ccc;
  padding: 20px;
  margin: 20px 0;
  width: 100%;
}
.movement-list {
  max-height: 300px; /* 根据需要调整高度 */
  overflow-y: auto;
  margin-top: 20px;
  border: 1px solid #ccc;
  padding: 10px;
}
img {
  width: 100%;
  max-width: 1000px;
  margin-bottom: 20px;
}
.error {
  color: red;
}
</style>
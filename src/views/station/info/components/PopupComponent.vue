<template>
  <div class="popup">
    <div class="popup-content">
      <h2>填写信息的弹出框</h2>
      <div class="mb-0">消防站名称</div>
      <label>
        <textarea
          v-model="localData.name"
          type="textarea"
          :rows="4"
          style="width: 200px;height: 30px;line-height: 20px; resize:none;"
          placeholder="请输入要填写的信息"
          maxlength="512"
        />
      </label>
      <div class="mb-0">所在区</div>
      <label>
      <textarea
        v-model="localData.district"
        type="textarea"
        :rows="4"
        style="width: 200px;height: 30px;line-height: 20px; resize:none;"
        placeholder="请输入要填写的信息"
        maxlength="512"
      />
    </label>
      <div class="mb-0">地址</div>
      <label>
        <textarea
          v-model="localData.address"
          append-icon="mdi-comment"
          type="textarea"
          :rows="4"
          style="width: 200px;height: 30px;line-height: 20px; resize:none;"
          placeholder="请输入要填写的信息"
          maxlength="512"
        />
      </label>
      <div class="mb-0">经纬度</div>
      <label>
        <textarea
          v-model="localData.position"
          type="textarea"
          :rows="4"
          style="width: 200px;height: 30px;line-height: 20px; resize:none;"

          maxlength="512"
        />
      </label>
      <div class="mb-0">电话</div>
      <label>
        <textarea
          v-model="localData.tel"
          type="textarea"
          :rows="4"
          style="width: 200px;height: 30px;line-height: 20px; resize:none;"
          placeholder="请输入要填写的信息"
          maxlength="5120"
        />
      </label>

      <button @click="closePopup">取消</button>
      <button @click="confirmPopup">确认</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  data() {
    // 创建本地副本以供修改
    return {
      localData: { ...this.data },
    };
  },
  methods: {
    closePopup() {
      this.$emit("closePopup");

      console.log(this.$parent);
      // this.$parent.$parent.getData();
    },
    confirmPopup() {
      this.id=this.localData.id;
      console.log("data:"+this.data)
      console.log("localData："+this.localData)
      axios.put("/search/station/update/"+this.localData.id,this.localData).then(res => {
        if(res.data.status==200){
          res.data=this.localData
          console.log(res.data)
          this.$message({
            type:"success",
            message: '更新成功',
            center: true,
          })
          this.$emit("closePopup");
        }else {
          console.log(res.data)
          this.$message({
            type:"error",
            message: '更新失败',
            center: true,
          })
        }
      })

    },
  },
};
</script>

<style scoped>
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.01);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background: #fff;
  padding: 200px;
  border-radius: 80px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.03);
}
</style>


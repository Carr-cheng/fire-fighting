<template>
  <el-table :data="this.tableData" @getData="getData" style="width: 100%">
<!--    <el-table-column fixed prop="id" label="序号" width="150" />-->
    <el-table-column prop="name" label="消防站名称" width="240" />
    <el-table-column prop="district" label="所在区" width="120" />
    <el-table-column prop="address" label="地址" width="300" />
    <el-table-column prop="position" label="经纬度" width="200" />
    <el-table-column prop="tel" label="电话" width="120" />
    <el-table-column fixed="right" label="操作" min-width="120">
      <template #default="{ row }">
        <el-button link type="primary"  icon="el-icon-delete" size="small" @click="deleteData(row)">
          删除
        </el-button>
        <el-button link type="primary" size="small" @click="showPopupV(row)">编辑</el-button>
        <popupComponent v-if="showPopup" :data="parentData" @closePopup="closePopup" />
      </template>
    </el-table-column>
  </el-table>
</template>
<script>

import popupComponent from "@/views/station/info/components/PopupComponent.vue";

import axios from 'axios'
export default {
  name: "",
  data: function () {
    return {
      tableData:[],
      val:[],
      showPopup: false,
      parentData: {}
    };
  },
  components: {popupComponent,
  },

  computed: {},
  mounted: function () {

    this.getData();
  },

  methods: {
    //获取表单数据
    async getData (){
      this.tableData=[];
      const { data: list } = await axios.get("/search/station/info",{headers: { "X-Webexp-Connect": "IAF" },timeout: 2000,
        credentials: false
      })
      this.val = JSON.parse(JSON.stringify(list.data.result));//list.data.result;
      for (var i=0;i<this.val.length;i++) {
        this.tableData.push(JSON.parse(JSON.stringify(this.val[i])).__data__);
      }
    },
    //删除表单数据
    async deleteData(row){
      var  than=this;
      this.id=row.id;
      axios.delete("/search/station/delete/"+than.id).then(res => {
        if(res.data.status==200){
          console.log(res.data)
          this.$message({
            type:"success",
            message: '删除成功',
            center: true,
          })
          than.getData();
        }else {
          console.log(res.data)
          this.$message({
            type:"error",
            message: '删除失败',
            center: true,
          })
          this.getData();
        }
        this.getData();
      })
    },
    //更新表单数据,后台逻辑根据id更新
    showPopupV(row) {
      this.parentData=Object(row);
      this.showPopup = true;
    },
    closePopup() {
      this.getData();
      this.showPopup = false;
    },
  },
}
</script>

<style>
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}
</style>
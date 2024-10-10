<template>
  <div style="padding: 40px">
<!--    <el-input v-model="search" style="width: 240px" placeholder="Please input" />-->
<!--    <h1>火灾数据信息</h1>-->
      <el-input v-model="search" suffix-icon="el-icon-search" placeholder="请输入搜索内容"></el-input>
      <el-table :data="tables.slice((currentPage-1)*PageSize,currentPage*PageSize)" border  style="width: 100%">
        <el-table-column prop="start_date" label="开始日期" width="120" />
        <el-table-column prop="start_time" label="开始时间" width="100" />
        <el-table-column prop="main_thing" label="主要物资" width="140" />
        <el-table-column prop="type" label="类型" width="60" />
        <el-table-column prop="level" label="水平" width="100" />
        <el-table-column prop="position" label="位置经纬度" width="160"/>
        <el-table-column prop="province" label="省份" width="100" />
        <el-table-column prop="city" label="城市" width="100" />
        <el-table-column prop="address" label="地址" width="160" />
        <el-table-column prop="distance" label="消防站距离" width="160" >
          <template #default="row">
            <div >
              <el-popover placement="right" :width="500" trigger="click">
                <template #reference>
                  <el-button style="margin-right: 16px" @click="getDistance(row)">查看距离</el-button>
                </template>
                <div class="threedlist">
                  <el-table :data="gridData">
                    <el-table-column width="150" property="address" label="火灾地点" />
                    <el-table-column width="100" property="station" label="消防站" />
                    <el-table-column width="300" property="distance" label="距离/千米" />
                  </el-table>
                </div>

              </el-popover>
            </div>
          </template>

        </el-table-column>

      </el-table>
      <div class="tabListPage">
        <el-pagination @size-change="handleSizeChange"
                       @current-change="handleCurrentChange"
                       :current-page="currentPage"
                       :page-sizes="pageSizes"
                       :page-size="PageSize" layout="total, sizes, prev, pager, next, jumper"
                       :total="tables.length">
        </el-pagination>
      </div>
      </div>
</template>

<script>
// import popupComponent from "@/views/search/Fire/components/PagedResult.vue";
import axios from "axios";
import { number } from "echarts";
export default {
  name: "",

  data() {
    return {
      search: "",
      val:[],
      tableData :[],
      gridData: [],
      showPopup: false,
      parentData: {},
      currentPage:1,
      // 总条数，根据接口获取数据长度(注意：这里不能为空)
      // 个数选择器（可修改）
      pageSizes:[10,20,40,50,100],
      // 默认每页显示的条数（可修改）
      PageSize:10,

    };
  },

  components: {
  },

  computed: {
    tables() {
      const search = this.search;
      if (search) {
        return this.val.filter((data) => {
          return Object.keys(data).some((key) => {
            return String(data[key]).toLowerCase().indexOf(search) > -1;
          });
        });
      }
      // this.handleCurrentChange(1);
      return this.val;
    },
    sortBykey(ary, key) {

      let arr1=JSON.stringify(ary)
      //console.log( arr1)
      let arr =arr1.map(item => Object.values(item))
      //console.log(typeof ary)
      arr.sort((a, b) => { return  b.distance - a.distance })

      return arr
    },
  },

  mounted: function () {
    this.test();
  },

  methods: {
    async test (){
      const { data: list } = await axios.get("/search/fire/info",{headers: { "X-Webexp-Connect": "IAF" },timeout: 2000,
        credentials: false
      })
      this.tableData = JSON.parse(JSON.stringify(list.data.result));//list.data.result;
      for (var i=0;i<this.tableData.length;i++) {
        this.val.push(JSON.parse(JSON.stringify(this.tableData[i])).__data__);
      }
    },
    async getDistance(row){
      const { data: list } = await axios.get("/search/fire/getDistance/"+row.row.id,{headers: { "X-Webexp-Connect": "IAF" },timeout: 2000,
        credentials: false
      })
      this.gridData = JSON.parse(JSON.stringify(list.data.result));//list.data.result;

     // console.log("1:"+JSON.stringify(this.gridData))
      this.gridData.sort((a, b) => { return  a.distance - b.distance })
      // for (var i=0;i<this.gridData.length;i++) {
      //   this.gridData.push(JSON.parse(JSON.stringify(this.gridData[i])).__data__);
      // }
    },

    handleSizeChange(var1) {
      // 改变每页显示的条数
      this.PageSize = var1;
      // 注意：在改变每页显示的条数时，要将页码显示到第一页
      this.currentPage = 1;
    },
    // 显示第几页
    handleCurrentChange(var1) {
      // 改变默认的页数
      this.currentPage = var1;
    },
    clickShowMore() {
      this.showMore = !this.showMore;
    },
    showPopupV(row) {

      this.$router.push({name: 'dispatchDict', params: row })
      // this.parentData=Object(row);
      // this.showPopup = true;
    },
    closePopup() {
      // this.getData();
      this.showPopup = false;
    },
  },

}

</script>
<!--<script lang="ts" setup>-->
<!--import { reactive } from 'vue'-->
<!--import { ref } from "vue";-->
<!--const dialogTableVisible = ref(false);-->

<!--const form = reactive({-->
<!--  name: '',-->
<!--  region: '',-->
<!--  date1: '',-->
<!--  date2: '',-->
<!--  delivery: false,-->
<!--  type: [],-->
<!--  resource: '',-->
<!--  desc: '',-->
<!--})-->


<!--</script>-->

<style lang="scss" scoped>
.threedlist {
  cursor: pointer;
  width: 400px;
  padding: 20px;
  padding-top: 10px;
  //position: fixed;
  height: 90vh; /* 定义父容器高度 */
  overflow-y: scroll; //只有在内容超过元素高度时才出现滚动条。
  //overflow-y: auto; /* 只有在内容超过父容器高度时才出现滚动条 */

}
</style>

<template>
    <div class='articleSquareForm'>
        <el-col :offset="2" :span="18">
        <div v-for="i in currentPage" style="border-radius:10px;padding:10px;margin:10px;background-color:white">
            <el-container class="record">
            <div @click="goToPost(i.record_id)">
            <el-container>
                <el-header height="30px" style="text-align:center">{{i.title}}</el-header>
                <el-main>{{i.content}}</el-main>
            </el-container>
            </div>
            <el-aside width="200px">
                <div style="text-align:center">{{i.commit_time}}</div>
                <div style="text-align:center;margin-top:10px">
                    <UserPanel :username="i.username" :size="25"></UserPanel>
                    <span style="margin:10px">{{i.username}}</span>
                </div>
                <div style="margin-top:15px">  
                    <span class="postDetail"><el-tooltip effect="dark" content="View" placement="top-start"><i class="el-icon-view" /></el-tooltip> {{i.view}}</span>
                    <span class="postDetail"><el-tooltip effect="dark" content="Start" placement="top-start"><i class="el-icon-star-off" /></el-tooltip> {{i.star}}</span>
                    <span class="postDetail"><el-tooltip effect="dark" content="Comment" placement="top-start"><i class="el-icon-chat-dot-square" /></el-tooltip> {{i.comment}}</span>
                </div>
            </el-aside>
            </el-container>
        </div>
        
        <div class="block" style="text-align:center">
            <el-pagination
            @current-change="handleCurrentChange"
            @prev-click="handelPrevClick"
            @next-click="handelNextClick"
            :current-page="currentPageNum"
            :page-size="1"
            layout="total, prev, pager, next, jumper"
            :total="total">
            </el-pagination>
        </div>
        </el-col>
    </div>
</template>

<script>
import https from '../../api/https.js'
import UserPanel from '@/components/userPanel';
export default{
    name: 'articleSquare',
    components:{
        UserPanel
    },
    data(){
        return{
            currentPageNum: 0,
            currentPage:[],
            allPages:[],
            total: 0,
        }
    },
    created(){
        https.fetchGet('getUserPost/1').then((res) => {
            if(res.data.code === 200){
                this.total=Math.ceil(res.data.total/5);
                for (let i=0;i<this.total;i++){
                    this.allPages.push([])
                }
                for(let i=0;i<res.data.retInfo.length;i++){
                    if(res.data.retInfo[i].content.length>100){
                        res.data.retInfo[i].content = res.data.retInfo[i].content.substr(0,100)+'...';
                    }
                }
                this.allPages[0] = res.data.retInfo;
                this.currentPage = res.data.retInfo;
                this.currentPageNum = 1
            }
        })
    },
    methods: {
        goToPost(record_id){
            this.$router.push({path: 'post', query: {record_id: record_id}});
        },
        handelPrevClick(page){
            if(this.allPages[page-1].length >0){
                this.currentPage = this.allPages[page-1];
            }else{
                https.fetchGet('getUserPost/'+page).then((res) => {
                    if(res.data.code === 200){
                        for(let i=0;i<res.data.retInfo.length;i++){
                            if(res.data.retInfo[i].content.length>100){
                                res.data.retInfo[i].content = res.data.retInfo[i].content.substr(0,100)+'...';
                            }
                        }
                        this.allPages[page-1] = res.data.retInfo;
                        this.currentPage = res.data.retInfo;
                        this.currentPageNum = page;
                    }
                })
            }
        },
        handelNextClick(page){
            if(this.allPages[page-1].length >0){
                this.currentPage = this.allPages[page-1];
            }else{
                https.fetchGet('getUserPost/'+page).then((res) => {
                    if(res.data.code === 200){
                        for(let i=0;i<res.data.retInfo.length;i++){
                            if(res.data.retInfo[i].content.length>100){
                                res.data.retInfo[i].content = res.data.retInfo[i].content.substr(0,100)+'...';
                            }
                        }
                        this.allPages[page-1] = res.data.retInfo;
                        this.currentPage = res.data.retInfo;
                        this.currentPageNum = page;
                    }
                })
            }
        },
        handleCurrentChange(page){
            if(this.allPages[page-1].length >0){
                this.currentPage = this.allPages[page-1];
            }else{
                https.fetchGet('getUserPost/'+page).then((res) => {
                    if(res.data.code === 200){
                        for(let i=0;i<res.data.retInfo.length;i++){
                            if(res.data.retInfo[i].content.length>100){
                                res.data.retInfo[i].content = res.data.retInfo[i].content.substr(0,100)+'...';
                            }
                        }
                        this.allPages[page-1] = res.data.retInfo;
                        this.currentPage = res.data.retInfo;
                        this.currentPageNum = page;
                    }
                })
            }
        },
    }
}
</script>


<style scoped>
  .articleSquareForm{
      padding:10px;
      background-color:rgb(245, 245, 245);
      height:767px;
      width:98.8%;
  }
  .el-header{
    text-align: center;
    line-height: 40px;
    font-size: 20px;
  }
  
  .el-aside {
    line-height: 30px;
    margin-top:10px;
  }
  
  .el-main {
    line-height: 30px;
  }
  .postDetail{
      margin:15px;
      size:20px;
  }
  .userPage{
      width: 300px;
      height: 250px;
  }
  .record:hover{
      cursor:pointer;
  }
</style>
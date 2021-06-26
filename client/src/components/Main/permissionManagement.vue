<template>
    <div class="PMform">
        <el-tabs type="border-card" :stretch=true style="margin:auto;height:99%">
        <el-tab-pane >
            <span slot="label"><i class="el-icon-user-solid"></i> 用户管理</span>
            <div class="search">
                <el-input
                type="text"
                v-model="searchUserContent"
                placeholder="输入用户名快速查找"
                class = 'search'
                @input="checkEmpty"
                prefix-icon="el-icon-search">
                </el-input>
                <el-button type="primary" icon="el-icon-search" @click="searchUser()">搜索</el-button>
            </div>
            <div v-show="!this.userSearch">
            <el-table
                :data="currentPage"
                stripe
                style="width: 85%;margin:auto">
                <el-table-column
                prop="register_time"
                label="注册日期"
                width="180">
                </el-table-column>
                <el-table-column
                prop="username"
                label="用户名"
                width="180">
                </el-table-column>
                <el-table-column
                prop="email"
                label="注册邮箱">
                </el-table-column>
                <el-table-column
                prop="total_record"
                label="发帖总数">
                </el-table-column>
                <el-table-column
                label="管理">
                <template slot-scope="scope">
                    <el-button type="danger" icon="el-icon-delete" @click="handleUserDelete(scope.row)">删除用户</el-button>
                    <el-button type="success" icon="el-icon-user-solid" @click="handleUserUpdate(scope.row)">设为管理员</el-button>
                </template>
                </el-table-column>
            </el-table>
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
            </div>
            <div v-show="this.userSearch">
                <div v-show="this.emptyUserSearch" style="font-size:30px;text-align:center;margin:10px;color:rgb(110, 106, 106);">没有找到用户</div>
                <div v-show="!this.emptyUserSearch">
                    <el-table
                        :data="searchUserInfo"
                        stripe
                        style="width: 85%;margin:auto">
                        <el-table-column
                        prop="register_time"
                        label="注册日期"
                        width="180">
                        </el-table-column>
                        <el-table-column
                        prop="username"
                        label="用户名"
                        width="180">
                        </el-table-column>
                        <el-table-column
                        prop="email"
                        label="注册邮箱">
                        </el-table-column>
                        <el-table-column
                        prop="total_record"
                        label="发帖总数">
                        </el-table-column>
                        <el-table-column
                        label="管理">
                        <template slot-scope="scope">
                            <el-button type="danger" icon="el-icon-delete" @click="handleUserDelete(scope.row)">删除用户</el-button>
                            <el-button type="success" icon="el-icon-user-solid" @click="handleUserUpdate(scope.row)">设为管理员</el-button>
                        </template>
                        </el-table-column>
                    </el-table>
                </div>
            </div>
        </el-tab-pane>



        <el-tab-pane>
            <span slot="label"><i class="el-icon-document"></i> 发布管理</span>
            <div class="search">
                <el-input
                type="text"
                v-model="searchPostContent"
                @input="searchHistory()"
                placeholder="输入作文标题快速查找"
                class = 'search'
                prefix-icon="el-icon-search">
                </el-input>
                <el-button type="primary" icon="el-icon-search">搜索</el-button>
            </div>
        </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
import https from '../../api/https.js'

export default {
    data(){
        return{
            userSearch: false,
            emptyUserSearch: false,
            searchUserInfo: [],
            searchUserContent: '',
            searchPostContent: '',
            currentPageNum: 0,
            currentPage:[],
            allPages:[],
            total: 0,
        }
    },
    created(){
        https.fetchGet('getUser/1').then((res) => {
            if(res.data.code === 200){
                console.log(res.data.retInfo)
                this.total=res.data.total;
                for (let i=0;i<this.total/1;i++){
                    this.allPages.push([])
                }
                this.allPages[0] = res.data.retInfo;
                this.currentPage = res.data.retInfo;
                this.currentPageNum = 1
            }
        })
    },
    methods: {
        handelPrevClick(page){
            if(this.allPages[page-1].length >0){
                this.currentPage = this.allPages[page-1];
            }else{
                https.fetchGet('getUser/'+page).then((res) => {
                    if(res.data.code === 200){
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
                https.fetchGet('getUser/'+page).then((res) => {
                    if(res.data.code === 200){
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
                https.fetchGet('getUser/'+page).then((res) => {
                    if(res.data.code === 200){
                        this.allPages[page-1] = res.data.retInfo;
                        this.currentPage = res.data.retInfo;
                        this.currentPageNum = page;
                    }
                })
            }
        },
        handleUserDelete(info){
            this.$confirm('此操作将永久删除该用户, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
            }).then(() => {
                https.fetchGet('deleteUser/'+info.username).then((res) => {
                    if(res.data.code === 200){
                        for(let i=0;i<1;i++){
                            if(this.currentPage[i].username == info.username){
                                this.currentPage.splice(i,1);
                            }
                        }
                        this.$notify({
                        title: '成功',
                        message: '删除用户成功！',
                        type: 'success'
                        });
                    }
                })
            }).catch(() => {
            this.$message({
                type: 'info',
                message: '已取消删除'
            });          
            });
        },
        handleUserUpdate(info){
            this.$confirm('此操作将会把用户'+info.username+'设置为管理员, 是否继续?', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
            }).then(() => {
                https.fetchGet('updateUser/'+info.username).then((res) => {
                    if(res.data.code === 200){
                        for(let i=0;i<1;i++){
                            if(this.currentPage[i].username == info.username){
                                this.currentPage.splice(i,1);
                            }
                        }
                        this.$notify({
                        title: '成功',
                        message: '设置管理员成功！',
                        type: 'success'
                        });
                    }
                })
            }).catch(() => {
            this.$message({
                type: 'info',
                message: '已取消设置'
            });          
            });
        },
        searchUser(){
            https.fetchGet('searchUser/'+this.searchUserContent).then((res) => {
                this.userSearch = true;
                if(res.data.code === 200){
                    this.emptyUserSearch = false;
                    this.searchUserInfo = res.data.retInfo;
                }else{
                    this.emptyUserSearch = true;
                }
            })
        },
        checkEmpty(){
            if(this.searchUserContent == ''){
                this.userSearch = false;
            }
        }
    }
}
</script>

<style scoped>
    .PMform{
        width:100%;
        height:785px;
        box-sizing: border-box;
        background-color:rgb(245, 245, 245);
        padding:1%;
        margin:0;
    }

    .search{
        width:90%;
        box-sizing: border-box;
        margin:0 auto;
    }
</style>
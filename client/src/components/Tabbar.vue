<template>
  <div>
    <el-menu
    :default-active="activeIndex2"
    class="el-menu-demo"
    mode="horizontal"
    @select="handleSelect"
    text-color="#fff"
    active-text-color="#ffd04b"
    background-color= "#545c64"
    style="margin:0"
    >
      <el-menu-item index= "/main"><i class="icon iconfont icon-tubiaozhizuomoban-" style="font-size:60px" ></i></el-menu-item>
      <el-menu-item index="/main/articleSquare"><i class="el-icon-document" />作文广场</el-menu-item>
      <el-menu-item index="/main/personalCenter"><i class="el-icon-view" />个人中心</el-menu-item>
      <el-menu-item v-if="this.$store.state.user_type=='administrator'" index="/main/permissionManagement"><i class="icon iconfont icon-guanli" style="font-size:25px"/>用户管理</el-menu-item>
    </el-menu>

    <el-col class="grid-content" :span="1"> 
        <el-row class="sideBar" style="width:80px;">
          <el-tooltip class="item" content="消息" placement="top">
            <el-badge :value="200" :max="99" class="item">
            <i class="el-icon-bell" style="font-size: 40px;" />
            </el-badge>
          </el-tooltip>
        </el-row>

        <el-row class="sideBar" style="width:80px;">
          <el-tooltip class="item" content="笔记本" placement="right">
          <el-popover
          placement="right"
          width="220"
          v-model="visible">
          <el-tabs>
            <el-tab-pane label="错词本" style='overflow:auto'>
              <el-collapse accordion style='height:200px'>
                <el-collapse-item v-for="i in notebook.error">
                  <template slot="title">
                    <div class="context" v-html="i.context_html"></div>
                  </template>
                  <span>
                    <span class="wrongChar">{{i.origin_text}}</span><span style="font-size:25px">&rarr;</span><span class="correctChar">{{i.correct_text}}</span>
                  </span>
                </el-collapse-item>
              </el-collapse>
            </el-tab-pane>

            <el-tab-pane label="积累本">

            </el-tab-pane>
          </el-tabs>
          <i class="el-icon-notebook-1" style="font-size: 40px;" slot="reference" />
          </el-popover>
          </el-tooltip>
        </el-row>


        <el-row class="sideBar" style="width:80px">
          <el-tooltip class="item" content="FAQ" placement="right">
            <i class="el-icon-question" style="font-size: 40px;" />
              <el-popover
              placement="right"
              width="200"
              trigger="click">
              <el-collapse accordion>
                <el-collapse-item title="功能清单">
                  <el-collapse accordion>
                    <el-collapse-item>
                      <template slot="title">
                        <i class="el-icon-question"></i>作文批改
                      </template>
                      <span>您可以在主页面点击新建或上传作文照片创建记录，写完后点击提交按钮将会为您指出作文中用词错误的地方以及推荐给您参考的优秀作文。写作过程中还可以使用右侧的查词或查找素材功能辅助您进行写作。</span>
                    </el-collapse-item>
                    <el-collapse-item>
                      <template slot="title">
                        <i class="el-icon-question"></i>用户评论
                      </template>
                      <span>当您写完一篇作文后，您可以在‘用户评论’里的选择是否公开您的作文。如果您选择公开，您可以在作文广场看到您的文章，同时其他用户也可以看到并给您提出建议。</span>
                    </el-collapse-item>
                    <el-collapse-item>
                      <template slot="title">
                        <i class="el-icon-question"></i>个人报告
                      </template>
                      <span>您可以在用户主页点击个人中心查看您的个人写作报告，包括系统对您的评分以及您收藏的错误用词记录。</span>
                    </el-collapse-item>
                  </el-collapse>
                </el-collapse-item>
                <el-collapse-item title="常见问题">
                  <el-collapse accordion>
                    <el-collapse-item>
                      <template slot="title">
                            <i class="el-icon-question"></i>隐私安全
                      </template>
                      <span>除非您选择公开您的文章，否则其他用户无法在作文广场查看到您的文章内容。</span>
                    </el-collapse-item>
                  </el-collapse>
                </el-collapse-item>
                <el-collapse-item title="关于我们">
                  <span>邮箱：2819238408@qq.com</span>
                </el-collapse-item>
              </el-collapse>
              <i class="el-icon-question" style="font-size: 40px;" slot="reference" />
            </el-popover>
          </el-tooltip>
        </el-row>

        <el-row class="sideBar" style="width:80px">
          <el-tooltip class="item" content="登出" placement="bottom">
            <i class="el-icon-s-home" style="font-size: 40px;" @click="logout"/>
          </el-tooltip>
        </el-row>
    </el-col>
  </div>
</template>

<script>
  import https from '../api/https.js'

  export default {
    data() {
      return {
        visible: false,
        activeIndex: '1',
        activeIndex2: '1',
        name: '',
        notebook: {
          error: [],
          accumulation: [],
        }
      };
    },
    methods: {
      logout(){
        this.$store.commit('del_token');
        sessionStorage.clear();
        this.$router.push('/')
      },
      handleSelect(key, keyPath) {
        this.$router.push({
        path: key,
        params: {data: 'query' }
      })
      }
    },
    created() {
      https.fetchGet('getNotebook').then((res) => {
        if (res.data['code'] === 200) {
          this.notebook.error = res.data.errorInfo;
        }
      });
    }
  }

</script>

<style scoped>
  .sideBar{
    margin:10px 0;
  }
  .grid-content {
    margin-top: 100px;
  }
  i:hover{
    cursor:pointer;
  }
  el-row{
    margin-bottom: 20px;
    display: flex;
    flex-wrap: wrap
  }
  .wrongChar{
    font-size:25px;
    text-decoration: line-through red;
    margin: 15px;
  }
  .correctChar{
    font-size:25px;
    margin: 15px;
  }

</style>

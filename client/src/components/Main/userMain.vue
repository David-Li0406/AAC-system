<template>
    <div class = 'newPageform'>
        <el-main v-loading="imageUpLoad.loading" element-loading-text="识别中" element-loading-background="rgba(255, 255, 255, 0.7)">
            <el-row>
                <el-col :offset="2" :span="20">
                    <el-input
                    type="text"
                    v-model="searchContent"
                    @input="searchHistory()"
                    placeholder="输入作文标题快速查找"
                    class = 'search'
                    prefix-icon="el-icon-search">
                    </el-input>
                </el-col>
            </el-row>

            <el-row>
                <el-col :offset="2" :span="3" class='recordCol'>
                    <el-card style="width: 200px;height:300px;" class='recordCard'>
                        <div class= 'buildPage'><el-link href="/#/main/newPage" style= "color: rgb(43, 144, 226);font-size: 20px"><i class="el-icon-edit" />新建</el-link></div>
                        <el-divider></el-divider>
                        <el-upload
                        class="imageUpLoader"
                        :class="{disabled:imageUpLoad.uploadDisabled}"
                        action="#"
                        list-type="picture-card"
                        :file-list="imageUpLoad.imagelist"
                        :auto-upload="false"
                        style="text-align:center;"
                        :on-change="handleChange">
                            <i slot="default" class="el-icon-plus"></i>
                            <div slot="file" slot-scope="{file}">
                                <img
                                    class="el-upload-list__item-thumbnail"
                                    :src="file.url" alt=""
                                >
                                <span class="el-upload-list__item-actions">
                                    <span
                                    class="el-upload-list__item-preview"
                                    @click="handlePictureCardPreview(file)"
                                    >
                                    <i class="el-icon-zoom-in"></i>
                                    </span>
                                    <span
                                    class="el-upload-list__item-delete"
                                    @click="handleUpLoad(file)"
                                    >
                                    <i class="el-icon-upload2"></i>
                                    </span>
                                    <span
                                    class="el-upload-list__item-delete"
                                    @click="handleRemove(file)"
                                    >
                                    <i class="el-icon-delete"></i>
                                    </span>
                                </span>
                            </div>
                        </el-upload>
                        <span style="font-size:5px;text-align:center;">
                            <el-link>*支持上传jpg/jpeg/png/bmp格式,文件大小不超过4MB</el-link>
                        </span>
                        <el-dialog :visible.sync="imageUpLoad.dialogVisible">
                            <img width="100%" :src="imageUpLoad.dialogImageUrl" alt="" style="margin:0">
                        </el-dialog>
                    </el-card>
                </el-col>

                <el-col v-for="index in first_row" :offset="1" :span="3" class='recordCol'>
                    <el-card v-show="userHistory[index-1]['visible']" class='recordCard'>
                        <div @click=goToResult(index-1)>
                            <div style="font-size:15px;text-align:center;height=200px">{{userHistory[index-1]['article_title']}}</div>
                            <div style="font-size:10px;text-align:center;margin:5px;">{{userHistory[index-1]['commit_time']}}</div>
                            <div style="font-size:10px">{{userHistory[index-1]['article_content']}}</div>
                        </div>
                        <el-col :span="5">
                            <span style="font-size:10px">{{userHistory[index-1]['article_count']}}字</span>
                        </el-col>
                        <el-col :span="5" :offset="4">
                            <span style="font-size:10px">{{userHistory[index-1]['article_time_cost']}}</span>
                        </el-col>
                        <el-col :offset="7" :span="3">
                            <span @click="deleteHistory(index-1)"><i class="el-icon-delete"></i></span>
                        </el-col>
                    </el-card>
                </el-col>

            </el-row>

            <el-row v-for="j in lines">
                <el-col v-for="index in columns(j)" :span="3" :offset="index==1 ? 2:1">
                    <el-card v-show="userHistory[idx(j,index)]['visible']" class='recordCard'>
                        <div @click=goToResult(idx(j,index))>
                            <div style="font-size:15px;text-align:center;height=200px">{{userHistory[idx(j,index)]['article_title']}}</div>
                            <div style="font-size:10px;text-align:center;margin:50x;">{{userHistory[idx(j,index)]['commit_time']}}</div>
                            <div style="font-size:10px">{{userHistory[idx(j,index)]['article_content']}}</div>
                        </div>
                        <el-col :span="5">
                            <span style="font-size:10px">{{userHistory[idx(j,index)]['article_count']}}字</span>
                        </el-col>
                        <el-col :span="5" :offset="4">
                            <span style="font-size:10px">{{userHistory[idx(j,index)]['article_time_cost']}}</span>
                        </el-col>
                        <el-col :offset="7" :span="3">
                            <span @click="deleteHistory(idx(j,index))"><i class="el-icon-delete"></i></span>
                        </el-col>
                    </el-card>
                </el-col>
            </el-row>
        </el-main>
    </div>
</template>

<script scoped> 
import https from '../../api/https.js'
export default{
    name: 'userMain',
    data() {
      return {
        imageUpLoad: {
            seeUpLoad: true,
            dialogImageUrl: '',
            dialogVisible: false,
            disabled: false,
            imagelist: [],
            uploadDisabled: false,
            loading: false,
        },
        userHistory: [],
        searchContent: '',
      };
    },
    created() {
        https.fetchGet('getHistory').then((res) => {
            if(res.data.message=='查找成功'){
                this.userHistory = res.data.records;
                for(let i=0;i<this.userHistory.length;i++){
                    console.log(this.userHistory[i]['article_count'])
                    if(this.userHistory[i]['article_count']==null){
                        this.userHistory[i]['article_count'] = this.userHistory[i]['article_content'].length;
                    }
                    if(this.userHistory[i]['article_title'].length>9){
                        this.userHistory[i]['article_title'] = this.userHistory[i]['article_title'].substr(0,9)+'...';
                    }
                    if(this.userHistory[i]['article_content'].length>150){
                        this.userHistory[i]['article_content'] = this.userHistory[i]['article_content'].substr(0,150)+'...';
                    }
                    this.userHistory[i]['visible']=true;
                }
                console.log(this.userHistory);
            }
        })
    },
    methods: {
      goToResult(idx){
          this.$router.push({path: 'result', query: {recordId: this.userHistory[idx]['id']}});
      },
      deleteHistory(idx){
          this.$confirm("删除记录后不可恢复，确认删除吗？").then(() => {
              let id = this.userHistory[idx]['id'];
              let deleteInfo = {
                  'id': id,
              };
              https.fetchPost('deleteHistory', deleteInfo).then((res) => {
                  if(res.data['code'] == 200){
                      this.userHistory.splice(idx, 1);
                  }
              })
          });
      },
      searchHistory(){
          if(this.searchContent==''){
              for(let i=0;i<this.userHistory.length;i++){
                  this.userHistory[i]['visible'] = true;
              }
          }else{
              for(let i=0;i<this.userHistory.length;i++){
                let pos = this.userHistory[i]['article_title'].indexOf(this.searchContent, 0);
                if(pos==-1){
                    this.userHistory[i]['visible'] = false;
                }else{
                    this.userHistory[i]['visible'] = true;
                }
            }
          }
      },
      handleRemove(file) {
        this.$confirm(`确定移除 ${ file.name }？`).then(() => {
            this.imageUpLoad.imagelist.splice(0,1);
            // 等图片框延迟消失的动画过后再显示添加图片框
            setTimeout(() => {
                        this.imageUpLoad.uploadDisabled = false;
                    }, 1100);
        });
      },
      handlePictureCardPreview(file) {
        this.imageUpLoad.dialogImageUrl = file.url;
        this.imageUpLoad.dialogVisible = true;
      },
      handleChange(file, filelist){
          this.imageUpLoad.imagelist.push(file);
          this.imageUpLoad.uploadDisabled = true;
      },
      handleUpLoad(file){
        let types = ['image/jpeg', 'image/jpg', 'image/bmp', 'image/png'];
        const isImage = types.includes(file.raw.type);
        const isLtSize = file.size / 1024 / 1024 < 4;
        if (!isImage) {
            this.$message.error('上传图片只能是 JPG、JPEG、bmp、PNG 格式!');
            return false;
        }
        if (!isLtSize) {
            this.$message.error('上传图片大小不能超过 4MB!');
            return false;
        }
        let reader = new FileReader();
        reader.readAsDataURL(file.raw);
        reader.onload = () => {
            var imgInfo = {
                'img_base64': reader.result,
            }
            this.$confirm(`确定上传 ${ file.name }并根据识别内容新建批改页？`).then(() => {
                this.imageUpLoad.loading = true;
                https.fetchPost('imgOCR', imgInfo).then((res) => {
                    this.imageUpLoad.loading = false;
                    if (res.data['code'] === 200) {
                        console.log(res.data['OCR_res'])
                        this.$router.push({name: 'newPage', params: {title: res.data['OCR_res']['title'], content: res.data['OCR_res']['content']}});
                        return true;
                    } else {
                        return false;
                    }
                })
            })
        };
        return true;
      }
    },
    computed:{
        first_row: function() {
            console.log(this.userHistory.length>=4? 4:this.userHistory.length)
            return this.userHistory.length>=4? 4:this.userHistory.length;
        },
        lines: function(){
            return Math.ceil((this.userHistory.length-4)/5);
        },
        columns: function(){
            return (j) => {
                let remain = this.userHistory.length-4-(j-1)*5;
                return remain>=5 ? 5:remain;
            }
        },
        idx: function(){
            return (j, index) => {
                return (j-1)*5+index+3;
            }
        }   
    }
}
</script>

<style>
    .newPageform{
        margin-top: 10px;
    }

    .recordCol{
        margin-top: 15px;
    }

    .buildPage{
        text-align: center;
        color: rgb(43, 144, 226);
    }
    .disabled .el-upload--picture-card{
        display: none;
    }

    .recordCard{
    border-radius:20px;
    width: 200px;
    height: 300px;
    /* display: flex; */
    box-shadow: 0 2px 12px 0 rgb(243, 102, 102);
    box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
    }

    .recordCard :hover{
        cursor:pointer;
    }
</style>
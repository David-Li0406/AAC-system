<template>
    <div class = 'newPageform'>
        <el-main v-loading="loading" :element-loading-text="waiting_message" element-loading-background="rgba(255, 255, 255, 0.7)">
            <el-row>
                <el-col :span="12" :offset="1">
                    <el-form status-icon :model="articleForm" :rules="rules" ref="articleForm">
                        <el-form-item prop="title">
                            <el-input placeholder="请输入作文题目" type="text" v-model="articleForm.title" autocomplete="off" @input="change()"></el-input>
                        </el-form-item>
                        <el-form-item prop="content">
                            <el-input type="textarea" rows="27" placeholder="请输入作文内容" v-model="articleForm.content" autocomplete="off" @input="change()"></el-input>
                        </el-form-item>
                        <el-form-item :inline-message="true">
                            <el-col :span="4" :offset="2" :stop="stop">
                                <i v-if="!stop" class="el-icon-video-pause" @click=setMode() />
                                <i v-else class="el-icon-video-play" @click=setMode() />
                                    {{hourShow}}:{{minutesShow}}:{{secondsShow}}
                            </el-col>
                            <el-col :span="3" :offset="5">
                                <div>字数：{{count}}</div>
                            </el-col>
                            <el-col :span="4" :offset="6">
                                <el-button type="primary"  @click="submitForm('articleForm')" size='large'>
                                    批改
                                </el-button>
                            </el-col>
                        </el-form-item>
                    </el-form>
                </el-col>

                <el-col :span="6" :offset="2">
                    <el-collapse accordion v-model="activeNames" @change="handleChange" style="height:700px;overflow:auto">
                        <!-- 查词助手 -->
                        <el-collapse-item name="1">
                            <template slot="title">
                                <i class="icon iconfont icon-cidianshangchuan"></i><span style="font-size:15px;margin:10px">查词助手</span>
                            </template>
                            <el-input
                            v-model = "word.searchWord"
                            placeholder="请输入待查找词语"
                            class = 'search'>
                                <el-button slot="append" icon="el-icon-search" @click="searchForWord()"></el-button>
                            </el-input>
                            <el-main v-loading="word.loading" element-loading-background="rgba(255, 255, 255, 0.7)">
                                <el-card
                                v-show="word.showWord">
                                    <div slot="header" class="clearfix" style="text-align: center;">
                                        <span>词语解释</span>
                                    </div>
                                    <div>
                                        释义：{{word.definition}}
                                    </div>
                                    <div>
                                        近义词：<span v-for="i in word.synonyms"> {{i}}</span>
                                    </div>
                                    <div>
                                        反义词：<span v-for="i in word.antonym"> {{i}}</span>
                                    </div>
                                </el-card>
                            </el-main>
                        </el-collapse-item>
                        <!-- 素材搜索 -->
                        <el-collapse-item name="2">
                            <template slot="title">
                                <i class="icon iconfont icon-sucai"></i><span style="font-size:15px;margin:10px">素材搜索</span>
                            </template>
                            <el-input
                            placeholder="请输入素材类型"
                            class = 'search'
                            v-model='searchMaterial.searchWord'>
                            <el-button slot="append" icon="el-icon-search" @click='searchForMaterial()'>
                            </el-button>
                            </el-input>
                            <el-main v-loading="searchMaterial.loading"  element-loading-background="rgba(255, 255, 255, 0.7)">
                            <div sytle="max-height:180px;overflow:auto;">
                                <el-divider></el-divider>
                                <div v-for="i in searchMaterial.searchRes">
                                    <h2 style="text-align: center;">{{i.title}}</h2>
                                    <span><el-link :href="i.url" target="_blank">{{i.content}}</el-link></span>
                                    <el-divider></el-divider>
                                </div>
                            </div>
                            </el-main>
                        </el-collapse-item>
                        <el-collapse-item name="3">
                            <template slot="title">
                                <i class="icon iconfont icon-chazhaoxiangsi"></i><span style="font-size:15px;margin:10px">相似作文</span>
                            </template>
                            <div style="text-align: center;">
                                <el-tooltip class="item" effect="dark" content="点击按钮根据题目匹配网站中的相似作文" placement="top">
                                    <el-button :loading="similarArticle.loading" type="primary" plain @click=matchArticle()>
                                        <span v-if="!loading">点击匹配相似作文</span>
                                        <span v-else>loading...</span>
                                    </el-button>
                                </el-tooltip>
                             </div>
                        </el-collapse-item>
                    </el-collapse>
                </el-col>
            </el-row>
        </el-main>
    </div>
</template>

<script> 
import https from '../../api/https.js';

export default{
    data(){
        var validateTitle = (rule, value, callback) => {
            if (value === '') {
                console.log(1);
                callback(new Error('请输入题目'));
            }else {
                console.log(this.articleForm.title);
                callback();
            }
        };
        var validateContent = (rule, value, callback) => {
            if (value === '') {
                callback(new Error('请输入作文内容'));
            } else {
                callback();
            }
        };
        return{
            word: {
                loading: false,
                searchWord: '',
                showWord: false,
                definition: '',
                pronunciation : '',
                synonyms: [],
                antonym: [],
            },
            searchMaterial: {
                searchWord: '',
                searchRes: [],
                loading: false,
            },
            similarArticle: {
                loading: false,
            },
            activeNames: ['1'],
            stop: false,
            loading: false,
            count: 0,
            waiting_message: "批改中",
            timer: "",
            hour: 0,
            minutes: 0,
            seconds: 0,
            hourShow: '00',
            minutesShow: '00',
            secondsShow: '00',
            articleForm: {
                title: '',
                content: '',
            },
            rules: {
                title: [
                    {validator: validateTitle , trigger: 'blur' }
                ],
                content: [
                    {validator: validateContent , trigger: 'blur' }
                ]
            }
        }
    },
    created(){
        this.timer = setInterval(this.startTimer, 1000);
        this.articleForm.title = this.$route.params.title;
        this.articleForm.content = this.$route.params.content;
        var re = /[\u4E00-\u9FA5]/g;
        if (this.articleForm.content.match(re)) {
            this.count = this.articleForm.content.match(re).length;
        } else {
            this.count = 0;
        }
    },
    methods: {
        searchForWord(){
            if(this.word.searchWord != ''){
                var searchInfo = {
                    'query': this.word.searchWord,
                };
                this.word.loading = true;
                https.fetchPost('searchWord', searchInfo).then((res) =>{
                    if(res.data['code'] === 200 ){
                        var item = res.data.wordInfo['result'][0]['response']['entity'][0]['attrs'];
                        console.log(item);
                        this.word.showWord = true;
                        for(var i = 0 ; i < item.length ; i++){
                            if(item[i]['label'] === '近义词'){
                                for(let j = 0; j<item[i]['objects'].length ; j++){
                                    this.word.synonyms.push(item[i]['objects'][j]['@value']);
                                }
                            }else if(item[i]['label'] === '反义词'){
                                for(let j = 0; j<item[i]['objects'].length ; j++){
                                    this.word.antonym.push(item[i]['objects'][j]['@value']);
                                }
                            }else if(item[i]['label'] === '释义'){
                                this.word.definition = item[i]['objects'][0]['@value'];
                            }
                        }
                        this.word.loading = false;
                    }
                })
            }
        },
        searchForMaterial(){
            if (this.searchMaterial.searchWord != ''){
                var searchInfo = {
                    'material': this.searchMaterial.searchWord,
                };
                this.searchMaterial.loading = true;
                https.fetchPost('searchMaterial', searchInfo).then((res) => {
                    if(res.data['code'] === 200){
                        console.log(res.data['materialInfo']);
                        this.searchMaterial.searchRes = res.data['materialInfo'];
                        this.searchMaterial.loading = false;
                    }
                })
            }
        },
        matchArticle(){
            if(this.articleForm.title == ''){
                this.$message('请先输入作文题目再进行匹配');
                return false;
            }else{
                this.similarArticle.loading = true;
                return true;
            }
        },
        submitForm(formName){
            var title = this.articleForm['title'];
            var content = this.articleForm['content'];
            var count = this.count;
            var time_cost = this.hourShow+':'+this.minutesShow+':'+this.secondsShow
            console.log(time_cost)
            var articleInfo = {
                'title': title,
                'content': content,
                'count': count,
                'time_cost': time_cost,
            };
            this.$refs[formName].validate((valid) => {
                if (valid) {
                        this.loading = true;
                        https.fetchPost('records', articleInfo).then((res) => {
                            if (res.data['code'] === 200) {
                                this.loading = false;
                                // 跳转到结果界面，并传递记录id
                                this.$router.push({path: '/Main/result', query: {recordId: res.data['recordId']}});
                                return true;
                            } else {
                                return false;
                            }
                        })
                    } else {
                        this.dialogVisible = true;
                        return false;
                    }
            });
        },
        change (e) {
            // 检测中文字符正则
            var re = /[\u4E00-\u9FA5]/g;
            if (this.articleForm.content.match(re)) {
                this.count = this.articleForm.content.match(re).length;
            } else {
                this.count = 0;
            }
        },
        startTimer() {
            this.seconds += 1;
            if (this.seconds >= 60) {
                this.seconds = 0;
                this.minutes = this.minutes + 1;
            }

            if (this.minutes >= 60) {
                this.minutes = 0;
                this.hour = this.hour + 1;
            }
            this.hourShow = this.hour < 10 ? '0' + this.hour: this.hour;
            this.minutesShow = this.minutes < 10 ? '0' + this.minutes: this.minutes;
            this.secondsShow = this.seconds < 10 ? '0' + this.seconds: this.seconds;
        },
        setMode(){
            this.stop = !this.stop;
            if(this.stop){
                clearInterval(this.timer);
            }else{
                this.timer = setInterval(this.startTimer, 1000);
            }
        },
        handleChange(val) {
            this.word.showWord = false;
            this.word.searchWord = '';
        }
    }
}
</script>

<style scoped>
  .el-row {
    margin-top: 25px;
  }

</style>
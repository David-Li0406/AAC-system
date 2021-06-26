<template>
    <div class = 'resultForm' style="margin:15px">
        <el-col :offset="1" :span="10">
        <Article :title="record.title" :content="record.content"></Article>
        </el-col>
        <el-col :offset="1" :span="10">
        <el-tabs type="border-card" style="height:750px;">

        <el-tab-pane label="批改结果">
            <div v-html="correction.origin_html" class="correctionEssay" style="height:300px;overflow:auto">
            </div>
            <div style="color:green;font-size:25px;text_align:center;padding:10px">修改建议:</div>
            <div style='overflow:auto;height:320px'>
                <el-collapse>
                <el-collapse-item v-for="content, pos_id, index in correction.correction">
                    <template slot="title">
                         <div class="context" v-html="content.context_html"></div>
                    </template>
                    <span>
                        <span class="wrongChar">{{content.origin_text}}</span><span style="font-size:25px">&rarr;</span><span class="correctChar">{{content.correct_text}}</span>
                    </span>
                    <span>
                        <el-tooltip class="item" effect="dark" content="替换" placement="top"><span  class='icon'><i class='el-icon-d-arrow-right' style="font-size: 25px;margin:10px;align:right" @click="place(content)"/></span></el-tooltip>
                        <el-tooltip :class={star:content.collected}  class="item" effect="dark" content="添加到笔记本" placement="top"><span  class='icon'><i class='el-icon-star-on' style="font-size: 25px;margin:10px;align:right" @click="addCollected(pos_id)" /></span></el-tooltip>
                        <el-tooltip class="item" effect="dark" content="查找释义" placement="top"><span  class='icon'><i class='el-icon-search' style="font-size: 25px;margin:10px;align:right" @click="searchWord(content.correct_text, index)" /></span></el-tooltip>
                    </span>
                    <el-main v-loading="word[index]['loading']" element-loading-background="rgba(255, 255, 255, 0.7)">
                        <el-card
                        v-show="word[index].showWord"
                        style="width:100%">
                            <div slot="header" class="clearfix" style="text-align: center;">
                                <span>词语解释</span>
                            </div>
                            <div>
                                释义：{{word[index].definition}}
                            </div>
                            <div>
                                近义词：<span v-for="i in word[index].synonyms"> {{i}}</span>
                            </div>
                            <div>
                                反义词：<span v-for="i in word[index].antonym"> {{i}}</span>
                            </div>
                        </el-card>
                    </el-main>
                </el-collapse-item>
                </el-collapse>
            </div>
        </el-tab-pane>

        <el-tab-pane label="作文推荐" style='overflow:auto'>
            <div class='recommand_article' style='height:650px'>
                <el-divider></el-divider>
                <div v-for="i in recommand_article">
                    <h2 style="text-align: center;">{{i.title}}</h2>
                    <span><el-link :href="i.url" target="_blank">{{i.content}}</el-link></span>
                    <el-divider></el-divider>
                </div>
            </div>
        </el-tab-pane>
           
        <el-tab-pane label="用户评论">
            <div v-if="!public" @click="makePublic()">
                <el-link>
                点击此处公开您的作文，让其他用户进行评论
                </el-link>
            </div>
            <div v-else style="height:690px;overflow-y:auto;overflow-x:hidden">
            <el-divider></el-divider>
            <div v-loading="loading">
            <div class="comment_content" v-for="content, comment_id, index in comment">
                <Comment :is_audio="content.is_audio" :reply="content.reply" :username="content.username" :comment_content="content.content" :commit_time="content.commit_time" :star="content.stars" :comment_id="comment_id" v-on:starComment="starComment" v-on:postReply="postReply"></Comment>
            </div>
            </div>
            </div>
        </el-tab-pane>
        </el-tabs>
        </el-col>
        <el-dialog
            title="公开成功！"
            :visible.sync="dialogVisible"
            width="30%">
            <span>您已公开这篇作文，其它用户现在可以在作文广场看到它</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import https from '../../api/https.js'
import Article from '@/components/article'
import Comment from '@/components/comment';

export default{
    name: 'result',
    components: {
        Article,
        Comment,
    },
    data(){
        return{
            loading:false,
            visible: false,
            record: {},
            correction: {
                origin_html: '',
                correction: {},
            },
            word: [],
            recommand_article:[],
            id: '',
            dialogVisible: false,
            comment: {},
            public: false,
        }
    },
    created(){
        https.fetchGet('record/' + this.$route.query.recordId).then((res) => {
            if(res.data.code === 200){
                this.record = res.data.recordInfo;
                this.id = res.data.record_id;
                this.public = res.data.public;
                this.recommand_article = res.data.recommand_article;
                this.correction.origin_html = res.data.correctionInfo['origin_html'];
                this.correction.correction = res.data.correctionInfo['correction'];
                for(let i=0;i<Object.keys(this.correction.correction).length;i++){
                    let dict={};
                    dict['loading'] = false;
                    dict['showWord'] = false;
                    dict['definition'] = '';
                    dict['synonyms'] = [];
                    dict['antonym'] = [];
                    this.word.push(dict)
                }
                if(this.public == true){
                    this.fetchComment();   
                }
            }
        })
    },
    methods: {
        postReply(replyInfo){
            console.log(replyInfo)
            replyInfo['record_id'] = this.id
            https.fetchPost('postReply', replyInfo).then((res) => {
                if(res.data.code === 200){
                    this.$notify({
                        title: '成功',
                        message: '回复成功',
                        type: 'success'
                    });
                    this.loading = true;
                    this.fetchComment();
                    this.loading = false;
                    return true;
                }
                return false;
            })
        },
        starComment(id){
            var commentInfo = {
                'comment_id':id,
            };
            https.fetchPost('starComment',commentInfo).then((res) => {
                if(res.data.code === 200){
                    this.comment[id].stars += 1;
                }
            })
        },
        fetchComment(){
            https.fetchGet('getComment/'+this.$route.query.recordId).then((res) => {
                if(res.data.code === 200){
                    if(res.data.message == '没有评论'){
                        return false;
                    }else{
                        this.comment = res.data.commentInfo;
                        for(let key in this.comment){
                            if(this.comment[key].is_audio){
                                this.comment[key].content = this.dataURItoBlob(this.comment[key].audio_record)
                                this.comment[key].content = URL.createObjectURL(this.comment[key].content);
                            }
                        }
                    }
                }
            })
        },
        dataURItoBlob(base64Data) {
            var byteString;
            if(base64Data.split(',')[0].indexOf('base64') >= 0)
                byteString = atob(base64Data.split(',')[1]);//base64 解码
            else{
                byteString = unescape(base64Data.split(',')[1]);
            }
            var mimeString = base64Data.split(',')[0].split(':')[1].split(';')[0];//mime类型 -- image/png
            var ia = new Uint8Array(byteString.length);//创建视图
            for(var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            var blob = new Blob([ia], {
                type: mimeString
            });
            return blob;
        },
        makePublic(){
            var recordInfo={
                'id':this.id,
            }
            https.fetchPost('makePublic', recordInfo).then((res)=>{
                if(res.data.code==200){
                    this.dialogVisible = true;
                    this.public = true;
                }
            })
        },
        addCollected(pos_id){
            var id = this.correction.correction[pos_id].id;
            var collectInfo={
                'id': id,
            }
            https.fetchPost('addError', collectInfo).then((res) => {
                if(res.data.code === 200){
                    this.correction.correction[pos_id].collected = true;
                    this.$message({
                        message: '添加成功！',
                        type: 'success'
                    });
                }
            })
        },
        place(content){
            this.correction.origin_html = this.correction.origin_html.replace(content.origin_text_html, content.correct_text_html);
        },
        searchWord(word, index){
            var searchInfo = {
                'query': word,
            };
            this.word[index]['loading'] = true;
            https.fetchPost('searchWord', searchInfo).then((res) =>{
                if(res.data['code'] === 200 ){
                    var item = res.data.wordInfo['result'][0]['response']['entity'][0]['attrs'];
                    this.word[index].showWord = true;
                    for(var i = 0 ; i < item.length ; i++){
                        if(item[i]['label'] === '近义词'){
                            for(let j = 0; j<item[i]['objects'].length ; j++){
                                this.word[index].synonyms.push(item[i]['objects'][j]['@value']);
                            }
                        }else if(item[i]['label'] === '反义词'){
                            for(let j = 0; j<item[i]['objects'].length ; j++){
                                this.word[index].antonym.push(item[i]['objects'][j]['@value']);
                            }
                        }else if(item[i]['label'] === '释义'){
                            this.word[index].definition = item[i]['objects'][0]['@value'];
                        }
                    }
                    this.word[index].loading = false;
                }
            })
        }
    }
}
</script>

<style>
    .origin-text-class{
        border-bottom: 2px solid red;
        text-decoration:none
    }
    .origin-text-class:hover{
        background-color: rgb(255, 148, 148);
    }
    .correct-text-class{
        background-color: rgb(14, 204, 7);
    }
    .origin-text-class-re{
        color:red;
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
    .icon:hover{
        cursor:pointer;
    }
    .star{
        color:red;
    }
</style>
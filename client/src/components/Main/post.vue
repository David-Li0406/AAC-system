<template>
    <div class = 'postform'>

        <el-dialog
        title="确认您的语言内容"
        :visible.sync="dialogVisible"
        width="30%"
        :close-on-click-modal="false"
        :close-on-press-escape="false">
        <audio :src="wavsrc" controls="controls">
            您的浏览器不支持 audio 标签。
        </audio>
        <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false;wavsrc = ''">取 消</el-button>
            <el-button type="primary" @click="uploadRecording">上 传</el-button>
        </span>
        </el-dialog>

        <el-col :span="10" :offset="1">
        <el-row>
            <el-col :span="2">
            <UserPanel :username="record.username" :size="40"></UserPanel>
            </el-col>
            <el-col :span="8" :offset="0">
                <el-row style="vertical-align:center">{{record.username}}</el-row>
                <el-row style="vertical-align:center">{{record.commit_time}}</el-row>
            </el-col>
            <el-col :offset="8" :span="6">
                <el-row>
                <el-col :span="8"><span class="postIcon"><el-tooltip effect="dark" content="View" placement="top-start"><i class="el-icon-view" /></el-tooltip> </span></el-col>
                <el-col :span="8"><span class="postIcon"><el-tooltip effect="dark" content="Start" placement="top-start"><i class="el-icon-star-off" @click="starPost" /></el-tooltip></span></el-col>
                <el-col :span="8"><span class="postIcon"><el-tooltip effect="dark" content="Comment" placement="top-start"><i class="el-icon-chat-dot-square" /></el-tooltip></span></el-col>
                </el-row>
                <el-row>
                    <el-col :span="8">
                    <span class="postDetail">{{record.view}}</span>
                    </el-col>
                    <el-col :span="8">
                    <span class="postDetail">{{record.star}}</span>
                    </el-col>
                    <el-col :span="8">
                    <span class="postDetail">{{record.total_comment}}</span>
                    </el-col>
                </el-row>
            </el-col>
        </el-row>
        <Article :title="record.title" :content="record.content"></Article>
        </el-col>

        <el-col :span="10" :offset="1">
            <div class="comment_title" style="font-size:30px;">Comment:
            </div>
            <div class="add_comment" style="margin-top:15px">
                <div v-if="!wantPost" class="commentEntry" @click="wantPost=true"><i class="el-icon-chat-round" style="margin:0 5px;font-size:20px;"></i>Add comment</div>
                <div v-if="wantPost" class="commentArea">
                    <el-input
                    type="textarea"
                    placeholder="请输入评论内容"
                    v-model="comment_text"
                    rows="3"
                    maxlength="200"
                    show-word-limit
                    >
                    </el-input>
                    <div style="margin:10px 0">
                        <el-button size="small" @click="wantPost=false;comment_text='';">取消</el-button>
                        <el-button type="primary" size="small" @click="postComment">提交</el-button>
                        <el-button v-if="ifRecording" type="primary" size="small" @click="stopRecording" icon="icon iconfont icon-yinpin">录音中</el-button>
                        <el-button v-else type="primary" size="small" @click="recording" icon="icon iconfont icon-yinpin">语音输入</el-button>
                    </div>
                </div>    
            </div>
            <div style="height:590px;overflow-y:auto;overflow-x:hidden">
            <el-divider></el-divider>
            <div v-loading="loading">
            <div class="comment_content" v-for="content, comment_id, index in comment">
                <Comment :is_audio="content.is_audio" :reply="content.reply" :username="content.username" :comment_content="content.content" :commit_time="content.commit_time" :star="content.stars" :comment_id="comment_id" v-on:starComment="starComment" v-on:postReply="postReply"></Comment>
            </div>
            </div>
            </div>
        </el-col>
    </div>
</template>

<script>
import Recorder from 'js-audio-recorder'
import Player from 'js-audio-recorder';
import https from '../../api/https.js';
import Article from '@/components/article';
import Comment from '@/components/comment';
import UserPanel from '@/components/userPanel';
const recorder = new Recorder({
                sampleBits: 16,                 // 采样位数，支持 8 或 16，默认是16
                sampleRate: 48000,              // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
                numChannels: 1,                 // 声道，支持 1 或 2， 默认是1
                // compiling: false,(0.x版本中生效,1.x增加中)  // 是否边录边转换，默认是false
            })
const player = new Player();

export default{
    name: 'post',
    components: {
        Article,
        Comment,
        UserPanel,
    },
    data(){
        return{
            ifRecording: false,
            record: {},
            wantPost: false,
            comment_text: '',
            comment: {},
            loading: false,
            wavsrc:'',
            audio_base64: '',
            dialogVisible:false,
        }
    },
    created(){
        https.fetchGet('post/'+this.$route.query.record_id).then((res) => {
            if(res.data.code === 200){
                this.record = res.data.recordInfo;
                console.log(this.record)
            }
        })
        this.fetchComment();
    },
    methods: {
        uploadRecording(){
            this.dialogVisible = false;
            var commentInfo = {
                'is_audio': true,
                'content': this.audio_base64,
                'record_id': this.record.record_id
            };
            https.fetchPost('postComment', commentInfo).then((res) => {
                if(res.data.code === 200){
                    this.$notify({
                        title: '成功',
                        message: '评论成功',
                        type: 'success'
                    });
                    this.audio_base64 = '';
                    this.wantPost = false;
                    this.loading = true;
                    this.fetchComment();
                    this.loading = false;
                }
            })
        },
        stopRecording(){
            this.ifRecording = false;
            recorder.stop();
            let WAVBlob = recorder.getWAVBlob();//获取 WAV 数据
            this.wavsrc = URL.createObjectURL(WAVBlob);
            console.log(this.wavsrc)
            this.dialogVisible = true;
            var reader = new FileReader();
            let that = this;
            reader.onload = function() 
            {   
                that.audio_base64 = this.result;
                console.log(that.audio_base64)
                console.log(that.audio_base64.length)
            }
            reader.readAsDataURL(WAVBlob);
        },
        recording(){
            this.ifRecording = true;
            const lamejs = require('lamejs')
            // 获取麦克风权限
            Recorder.getPermission();
            recorder.start()
        },
        dataURItoBlob(base64Data) {
            //console.log(base64Data);//data:image/png;base64,
            var byteString;
            if(base64Data.split(',')[0].indexOf('base64') >= 0)
                byteString = atob(base64Data.split(',')[1]);//base64 解码
            else{
                byteString = unescape(base64Data.split(',')[1]);
            }
            var mimeString = base64Data.split(',')[0].split(':')[1].split(';')[0];//mime类型 -- image/png

            // var arrayBuffer = new ArrayBuffer(byteString.length); //创建缓冲数组
            // var ia = new Uint8Array(arrayBuffer);//创建视图
            var ia = new Uint8Array(byteString.length);//创建视图
            for(var i = 0; i < byteString.length; i++) {
                ia[i] = byteString.charCodeAt(i);
            }
            var blob = new Blob([ia], {
                type: mimeString
            });
            return blob;
        },
        postReply(replyInfo){
            console.log(replyInfo)
            replyInfo['record_id'] = this.record.record_id
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
        starPost(){
            var recordInfo = {
                'record_id': this.record.record_id
            }
            https.fetchPost('starPost',recordInfo).then((res) => {
                if(res.data.code === 200){
                    this.record.star += 1;
                }
            })
        },
        fetchComment(){
            https.fetchGet('getComment/'+this.$route.query.record_id).then((res) => {
            if(res.data.code === 200){
                if(res.data.message == '没有评论'){
                    return false;
                }else{
                    console.log(res.data.commentInfo)
                    this.comment = res.data.commentInfo;
                    for(let key in this.comment){
                        if(this.comment[key].is_audio){
                            console.log(this.comment[key].audio_record)
                            console.log(this.comment[key].audio_record.length)
                            this.comment[key].content = this.dataURItoBlob(this.comment[key].audio_record)
                            this.comment[key].content = URL.createObjectURL(this.comment[key].content);
                        }
                    }
                }
            }
        })
        },
        postComment(){
            if(this.comment_text == ''){
                this.$message({
                    message: '评论内容不能为空！',
                    type: 'warning'
                });
            }else{
                var commentInfo = {
                    'content': this.comment_text,
                    'record_id': this.record.record_id
                };
                https.fetchPost('postComment', commentInfo).then((res) => {
                    if(res.data.code === 200){
                        this.$notify({
                            title: '成功',
                            message: '评论成功',
                            type: 'success'
                        });
                        this.comment_text = '';
                        this.wantPost = false;
                        this.loading = true;
                        this.fetchComment();
                        this.loading = false;
                    }
                })
            }
        }
    }
}
</script>

<style scoped>
    .postform{
        margin:10px;
    }
    .commentEntry{
        border:solid 1px rgb(150, 144, 144);
        height:30px;
        /* width:100%; */
        border-radius:5px;
        color: rgb(150, 144, 144);
    }
    .commentEntry:hover{
        cursor: text;
    }
    .postIcon:hover{
        cursor:pointer;
    }
</style>
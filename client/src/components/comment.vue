<template>
    <div class='commentForm'>
        <el-row>
            <el-col :span="1">
                <UserPanel :username="username" :size="20"></UserPanel>
            </el-col>
            <el-col :span="6">
                <span style="padding:10px">{{username}}</span>
            </el-col>
            <el-col :span="7" :offset="10">
                <span>{{commit_time}}</span>
            </el-col>
        </el-row>
        <div class="content" >
            <span v-if="!this.is_audio">{{comment_content}}</span>
            <span v-else>
                <audio :src="comment_content" controls="controls">
                    您的浏览器不支持 audio 标签。
                </audio>
            </span>
        </div>
        <el-col :offset="20">
            <span class="postDetail" @click="myclick(comment_id)"><el-tooltip effect="dark" content="Start" placement="top-start"><i class="el-icon-star-off" /></el-tooltip>{{star}}</span>
            <span class="postDetail" @click="wantReply=true"><i class="el-icon-chat-dot-square" />reply</span>
        </el-col>
        <div v-if="wantReply" class="commentArea">
            <el-input
            type="textarea"
            placeholder="请输入回复内容"
            v-model="reply_text"
            rows="5"
            maxlength="200"
            show-word-limit
            >
            </el-input>
            <div style="margin:10px 0"><el-button size="small" @click="wantReply=false;reply_text='';">取消</el-button><el-button type="primary" size="small" @click="post()">提交</el-button></div>
        </div>
        <el-divider></el-divider>

        <div v-for="reply in thisreply">
            <Reply :reply="reply" v-on:post="postText"></Reply>
        </div>

    </div>
</template>

<script>
import Reply from '@/components/reply';
import UserPanel from '@/components/userPanel';
import Recorder from 'js-audio-recorder'
import Player from 'js-audio-recorder';

const recorder = new Recorder({
                sampleBits: 16,                 // 采样位数，支持 8 或 16，默认是16
                sampleRate: 48000,              // 采样率，支持 11025、16000、22050、24000、44100、48000，根据浏览器默认值，我的chrome是48000
                numChannels: 1,                 // 声道，支持 1 或 2， 默认是1
                // compiling: false,(0.x版本中生效,1.x增加中)  // 是否边录边转换，默认是false
            })

export default {
    name: 'comment',
    components:{
        Reply,
        UserPanel,
    },
    data(){
        return{
            wantReply: false,   
            reply_text: '',
            thisreply: this.reply,
        }
    },
    methods: {
        post(){
            if(this.reply_text == ''){
                this.$message({
                    message: '回复内容不能为空！',
                    type: 'warning'
                });
            }else{
                var replyInfo = {
                    'comment_id': this.comment_id,
                    'reply_content': this.reply_text,
                    'username': this.username,
                };
                if(this.$emit('postReply',replyInfo)){
                    this.reply_text = '';
                    this.wantReply = false;
                }
            }
        },
        myclick(id){
            this.$emit('starComment', id);
        },
        postText(replyInfo){
            replyInfo['comment_id'] = this.comment_id;
            return this.$emit('postReply',replyInfo)
        },
    },
    props:['is_audio', 'reply', 'username', 'comment_content', 'commit_time', 'star', 'comment_id', 'type'],
}
</script>

<style scoped>
    .postDetail{
        margin:5px;
    }
    .postDetail:hover{
        cursor:pointer;
    }
</style>

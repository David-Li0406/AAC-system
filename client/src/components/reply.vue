<template>
    <div class="replyForm">
        <div style="margin:0 0 0 60px">
                <el-row>
                    <el-col :span="1">
                        <UserPanel :username="reply.username" :size="20"></UserPanel>
                    </el-col>
                    <el-col :span="6">
                        <span style="padding:10px">{{reply.username}}对{{reply.receive_user}}说：</span>
                    </el-col>
                    <el-col :span="7" :offset="10">
                        <span>{{reply.commit_time}}</span>
                    </el-col>
                </el-row>
                <div class="content">{{reply.content}}</div>
                <el-col :offset="21">
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
                    <div style="margin:10px 0"><el-button size="small" @click="wantReply=false;reply_text='';">取消</el-button><el-button type="primary" size="small" @click="postText">提交</el-button></div>
                </div>
                <el-divider></el-divider>      
        </div>
    </div>
</template>

<script>
import UserPanel from '@/components/userPanel';
export default {
    name: 'reply',
    components:{
        UserPanel,
    },
    data(){
        return{
            wantReply: false,   
            reply_text: '',
        }
    },
    methods:{
        postText(){
            if(this.reply_text == ''){
                this.$message({
                    message: '回复内容不能为空！',
                    type: 'warning'
                });
            }else{
                var replyInfo = {
                    'reply_content': this.reply_text,
                    'username': this.reply.username,
                };
                if(this.$emit('post',replyInfo)){
                    this.reply_text = '';
                    this.wantReply = false;
                }
            }
        }
    },
    props:['reply'],
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
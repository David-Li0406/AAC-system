<template>
        <el-popover
            placement="top-start"
            width="300"
            trigger="hover"
            popper-class='area_popper'
            >
            <div class='userPage'>
                <div class="block" style="text-align:center;"><el-avatar icon="el-icon-user-solid" :size='100' style="font-size:70px"></el-avatar></div>
                <div style="text-align:center;margin:10px">
                    用户名：{{username}}
                </div>
                <div style="text-align:center;margin:10px">
                    发帖：{{post}}
                </div>
                <div style="text-align:center;margin:10px">
                    回复：{{reply}}
                </div>
                <div style="text-align:center;margin:10px">
                    <el-tooltip effect="dark" content="私聊" placement="top-start">
                    <el-button type="info" icon="el-icon-message" circle></el-button>
                    </el-tooltip>
                    <el-tooltip effect="dark" content="举报" placement="top-start">
                    <el-button icon="el-icon-warning-outline" circle></el-button>
                    </el-tooltip>
                </div>
            </div>
            <i class="el-icon-user-solid" slot="reference" :style="{fontSize:this.size+'px'}"></i>
        </el-popover>
</template>

<script>
import https from '../api/https.js'

export default {
    name: 'userPanel',
    props: ['username', 'size'],
    data(){
        return{
            thissize: this.size,
            post:0,
            reply:0,
        }
    },
    watch: {
        username: { 
            handler(newVal,oldVal){
                if(typeof(newVal) != "undefined"){
                    https.fetchGet('getUserInfo/'+newVal).then((res) => {
                        if(res.data.code === 200){
                            this.post = res.data.post;
                            this.reply = res.data.total_reply;
                        }
                    })
                }
            }, 
            immediate:true,
            deep:true,
        } 
    },
}
</script>

<style scoped>
    .el-icon-user-solid:hover{
        cursor:pointer;
    }
</style>
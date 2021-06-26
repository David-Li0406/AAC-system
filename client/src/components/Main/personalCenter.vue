<template>
    <div class='statForm'>
        <div class="userInfomation">
            <div class="logo">
                <img src="../../assets/写作.png" style="border-radius:50%;width:100%;height:100%">
            </div>
            <div class="username">
                <div style="font-size:40px;line-height:100px;font-weight:bolder;">{{showInfo.nickname}}</div>
            </div>
            <div class="welcome">
                <div class="welcome1">欢迎回到个人中心</div>
                <div class="welcome2">这是爱写作平台陪伴您的第<span style="font-size:25px;color:red">{{showInfo.num_day}}</span>天</div>
            </div>
            <div class="writeNum">
                <div class="num"><span style="font-size:45px;color:blue">{{showInfo.record}}</span>篇</div>
                <div class="write">已写下</div>
            </div>
            <div class="writeNum">
                <div class="num"><span style="font-size:45px;color:blue">{{showInfo.count}}K</span>字</div>
                <div class="write">总字数</div>
            </div>
            <div class="writeNum">
                <div class="num"><span style="font-size:45px;color:blue">{{showInfo.time}}</span>小时</div>
                <div class="write">训练时长</div>
            </div>
        </div>
        <div class="bottom">
            <div class="chart">
                <div id="raderChart"></div>
                <div class="indicator">
                <div v-for="v,k,index in score">
                    <span style="font-weight:bolder;">{{k}}:</span>
                    <STAR 
                    :key=v
                    :grade=v
                    >
                    </STAR>
                </div>
                </div>
            </div>
            <div class="collection">
                <div style="font-size:30px;text-align:center;margin:1%;height:10%">错词积累</div>
                <div style="overflow:auto;height:90%">
                    <el-collapse class="correction" style="height:98%">
                        <el-collapse-item v-for="i in error">
                        <template slot="title">
                            <div class="context" v-html="i.context_html"></div>
                        </template>
                        <span>
                            <span class="wrongChar">{{i.origin_text}}</span><span style="font-size:30px">&rarr;</span><span class="correctChar">{{i.correct_text}}</span>
                        </span>
                        </el-collapse-item>
                    </el-collapse>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import https from '../../api/https.js'
import * as echarts from 'echarts';
import STAR from '@/components/Main/star'
export default{
    name: 'personalCenter',
    components:{
        STAR
    },
    data(){
        return{
            score: {},
            error: [],
            showInfo: {},
        }
    },
    created(){
        https.fetchGet('getUserStat').then((res) => {
            if(res.data.code === 200){
                this.score = res.data.userStat;
                this.showInfo = res.data.showInfo
                this.draw();
            }
        })
        https.fetchGet('getNotebook').then((res) => {
            if (res.data['code'] === 200) {
            this.error = res.data.errorInfo;
            }
        });
    },
    methods: {
        draw(){
            console.log(this.score.count_score,this.score.precision_score,this.score.time_cost_score)
            var chartDom = document.getElementById('raderChart');
            var myChart = echarts.init(chartDom);
            var option;

            option = {
                title: {
                    text: '写作能力分析'
                },
                radar: {
                    indicator: [
                        { name: '篇章长度', max: 10},
                        { name: '用词正确率', max: 10},
                        { name: '写作时长', max: 10},
                    ]
                },
                series: [{
                    type: 'radar',
                    data: [
                        {
                            value: [this.score.篇章长度,this.score.用词正确率,this.score.写作时长],
                        }
                    ]
                }],
            };

            option && myChart.setOption(option);
        }
    }
}
</script>

<style scoped>

    .statForm{
        width:100%;
        height:785px;
        box-sizing: border-box;
        background-color:rgb(245, 245, 245);
        padding:1%;
        margin:0;
    }

    .userInfomation{
        background-color:white;
        width: 80%;
        height:20%;
        border-radius:10px;
        box-sizing: border-box;
        padding: 1.5%;
        margin:1% auto
    }

    .logo{
        float:left;
        width:8%;
        height:95%;
        border-radius:50%;
        border:solid 1px;
        background-color:rgb(24, 100, 240);
        margin:auto 1%;
    }

    .username{
        float:left;
        height:95%;
        margin:auto 1%;
    }

    .welcome{
        float:left;
        height:95%;
        margin:auto 1%;
        width:25%;
    }

    .welcome1{
        height:30%;
        margin-left:0;
        width:80%;
        margin:solid;
        margin-top:6%;
        color:rgb(175, 172, 172);
    }

    .welcome2{
        height:30%;
        margin-left:0;
        width:80%;
        margin:solid;
        margin-bottom:6%;
        color:rgb(175, 172, 172);
    }

    .bottom{
        width:80%;
        height:70%;
        border-radius:10px;
        box-sizing: border-box;
        margin:2% auto
    }

    .chart{
        background-color:white;
        width: 49%;
        height: 100%;
        box-sizing: border-box;
        float:left;
        margin-right:1%;
        border-radius:10px;
    }

    #raderChart{
        height:55%;
        width:90%;
        margin:1% auto;
    }

    .indicator{
        height:43%;
        width:90%;
        padding: 0 auto;
        margin-left:10px;
    }

    .collection{
        background-color:white;
        width:49%;
        height: 100%;
        float:left;
        box-sizing: border-box;
        margin-left:1%;
        border-radius:10px;
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

    .userInfo{
        float:left;
        width:8%;
        height:95%;
        border-radius:50%;
        border:solid 1px;
        background-color:rgb(24, 100, 240);
        margin:auto 1%;
    }

    .writeNum{
        float:right;
        width:13%;
        height:95%;
        margin:auto 1%;
    }

    .num{
        height:60%;
        width:100%;
        margin:auto;
        width:80%;
        font-size:25px;
        font-weight:bolder;
    }

    .write{
        height:30%;
        width:100%;
        width:80%;
        margin:auto;
        font-size:15px;
        color:rgb(175, 172, 172);
    }

</style>
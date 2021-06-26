<template>
    <div>
        <div class='outline' >
            <div class='border'>
                <div class='paper'>
                    <div class='title'>{{title}}</div>
                    <div class='content'>{{content}}</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default{
    props:['title', 'content',]
}
</script>

<style scoped>
    .outline{
        padding:10px;
        background-color:rgb(255, 232, 198);
        height:710px;
    }
    .border{
        padding:5px;
        border: 1px dashed rgb(99, 97, 97);
        border-radius:10px;
        height:700px;
    }
    .content{
        margin-top:20px;
        font-size:15px;
        line-height: 25px;
        text-decoration:underline dashed 1px rgb(167, 157, 157);
    }
    .title{
        text-align:center;
        font-size:25px;
        line-height:40px;
    }

</style>
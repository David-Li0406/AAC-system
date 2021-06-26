<template>
    <div class = 'mainform'>
        <Tabbar></Tabbar>
        <router-view/>
    </div>
</template>

<script>
import Tabbar from '@/components/Tabbar'
export default{
    name: 'Main',
    components:{
        Tabbar,
    },
}
</script>

<style>
</style>

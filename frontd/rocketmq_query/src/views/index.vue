<template>
            <el-main style="height: 100%">
                <main-part />
                <router-view/>
            </el-main>
</template>

<script>

    import MainPart from '../components/main.vue'

    export default {
        name: 'Index',
        components: { MainPart },
    }

</script>

<style scoped>

    .el-main {
        background-color: #E9EEF3;
        color: #333;
        text-align: center;
        line-height: 10px;
    }


</style>
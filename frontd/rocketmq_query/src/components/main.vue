<template>

    <el-row>
        <el-col :span="24"><div class="grid-content bg-purple-dark"></div>
            <el-menu
                    default-active="activeIndex2"
                    class="el-menu-demo"
                    mode="horizontal"
                    background-color="#545c64"
                    text-color="#fff"
                    active-text-color="#ffd04b"
                    router>
                <el-submenu index="topic">
                    <template slot="title">topic</template>
                    <el-menu-item index="topic_route">topic_route</el-menu-item>
                    <el-menu-item index="topic_status">topic_status</el-menu-item>
                    <el-menu-item index="topic_consumergroup">topic_consumergroup</el-menu-item>
                </el-submenu>
                <el-submenu index="consumergroup">
                    <template slot="title">consumergroup</template>
                    <el-menu-item index="consumergroup_status">consumergroup_status</el-menu-item>
                    <el-menu-item index="consumergroup_connection">consumergroup_connection</el-menu-item>
                </el-submenu>

                <el-submenu index="producergroup">
                    <template slot="title">producergroup</template>
                    <el-menu-item index="producergroup_connection">producergroup_connection</el-menu-item>
                </el-submenu>
                <el-submenu index="message">
                    <template slot="title">Message</template>
                    <el-menu-item index="message_key">by_msgkey</el-menu-item>
                    <el-menu-item index="message_id">by_msgid</el-menu-item>
                </el-submenu>
                <el-menu-item index="consumergroup_tag">consumergroup_by_tag</el-menu-item>
            </el-menu></el-col>
    </el-row>



</template>

<script>


    export default {
        name: "MainPart",
        components: {} ,
        methods: {
            my: function(){
                // eslint-disable-next-line no-console
                console.log(this.env)
            }
        }
    }
</script>

<style scoped>

</style>
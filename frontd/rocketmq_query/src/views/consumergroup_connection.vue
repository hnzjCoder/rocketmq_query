<template>
    <el-row>
        <el-col :span="4"><div class="grid-content bg-purple">
            <div class="demo-input-suffix">
                <el-input
                        maxlength="400"
                        type="text"

                        rows="1"

                        placeholder="请输入内容"
                        v-model="input1">
                    <template slot="prepend">ConsumerGroup</template>
                </el-input>
            </div>
        </div></el-col>
        <el-col :span="4"><div class="grid-content bg-purple-light"></div>
            <el-select v-model="value" placeholder="环境">
                <el-option
                        v-for="item in options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                </el-option>
            </el-select>
        </el-col>

        <el-col :span="4"><div class="grid-content bg-purple-light"></div>
            <div class="demo-input-suffix">
                <el-button type="primary" v-on:click=load_data() @click="loading=true"  icon="el-icon-search">搜索</el-button>
            </div>
        </el-col>

        <el-table
                :data="tableData"
                v-loading="loading"
                height="1000px"
                border
                style="width: 100%"
                fit:true>


            <el-table-column
                    prop="client_id"
                    label="client_id"
                    width="400px">
            </el-table-column>
            <el-table-column
                    prop="client_addr"
                    label="client_addr"
                    width="200px">
            </el-table-column>
            <el-table-column
                    prop="language"
                    label="language"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="version"
                    label="version"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="version_desc"
                    label="version_desc"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="consumer_from_where"
                    label="consumer_from_where"
                    width="300px">
            </el-table-column>
            <el-table-column
                    prop="consumer_type"
                    label="consumer_type"
                    width="200px">
            </el-table-column>
            <el-table-column
                    prop="message_model"
                    label="message_model"
                    width="200px">
            </el-table-column>


        </el-table>


    </el-row>
</template>

<script>

    import { baseURL } from "./baseConfig";
    export default {
        name: "topic",
        data() {
            return {
                tableData: [],
                input1: 'orderSideService',
                options: [{
                    value: 'prod_unit',
                    label: '生产-阿里云-unit'
                }, {
                    value: 'prod_gw',
                    label: '生产-阿里云-gw'
                },{
                    value: 'qa1_unit',
                    label: '测试环境1-unit'
                }],
                value: 'prod_unit',
                loading: false
            }
        },

        methods:{
            load_failed: function(argu) {
                this.$notify({
                    title: '失败',
                    message: argu,
                    type: 'error'
                });

            },
            load_success: function() {
                this.$notify({
                    title: '成功',
                    message: '查询成功',
                    type: 'success'
                });

            },

            load_data: function () {
                this.tableData = []
                this.$http.get(

                    baseURL + '/consumerGroupClientConnection',
                    {params: {
                            env: this.value,
                            consumerGroup: this.input1,
                        },
                        headers:{
                            'Access-Control-Allow-Origin':'*'
                        }},

                ).then(function (res) {
                    // eslint-disable-next-line no-console
                    console.log('请求环境', this.value)

                    let _tableData = []

                    let _data = res.body['data']
                    if (_data === 'null'){
                        this.load_failed(res.body['errMsg'])
                        this.loading = false
                        return this.tableData, this.loading
                    }

                    // eslint-disable-next-line no-console
                    console.log('原数据',_data)
                    // eslint-disable-next-line no-console
                    console.log('长度', _data.length)
                    for (let i=0;i<_data.length;i++){
                        _tableData.push({
                            'client_addr': _data[i]['client_addr'],
                            'client_id': _data[i]['client_id'],
                            'consumer_from_where': _data[i]['consumer_from_where'],
                            'consumer_type': _data[i]['consumer_type'],
                            'language': _data[i]['language'],
                            'message_model': _data[i]['message_model'],
                            'version': _data[i]['version'],
                            'version_desc': _data[i]['version_desc']
                        })

                    }

                    this.tableData = _tableData
                    let _loading = false
                    this.loading = _loading
                    // eslint-disable-next-line no-console
                    console.log('我又被点击了', _tableData)
                    this.load_success()

                    return this.tableData, this.loading
                })

            }


        }


    }
</script>

<style scoped>

</style>
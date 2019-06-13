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
                    <template slot="prepend">Topic</template>
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
                <el-button type="primary" v-on:click=load_data() @click="loading=true" icon="el-icon-search">搜索</el-button>
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
                    prop="consumer_group"
                    label="consumer_group"
                    width="400px">
            </el-table-column>
            <el-table-column
                    prop="topic"
                    label="topic"
                    width="180px">
            </el-table-column>
            <el-table-column
                    prop="broker_name"
                    label="broker_name"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="queueId"
                    label="queueId"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="broker_offset"
                    label="broke_offset"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="consumer_offset"
                    label="consumer_offset"
                    width="150px">
            </el-table-column>
            <el-table-column
                    prop="diff_offset"
                    label="diff_offset"
                    width="100px">
            </el-table-column>
            <el-table-column
                    prop="diff_total"
                    label="diff_total"
                    width="100px">
            </el-table-column>
            <el-table-column
                    prop="consumer_id"
                    label="consumer_id"
                    width="400px">
            </el-table-column>
            <el-table-column
                    prop="last_update_timestamp"
                    label="last_update_timestamp"
                    :formatter="lastupdate_timestampToTime"
                    width="180px">
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
                input1: 'dispatch',
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
            lastupdate_timestampToTime (row,) {
                let date = new Date(row.last_update_timestamp) //时间戳为10位需*1000，时间戳为13位的话不需乘1000
                let Y = date.getFullYear() + '-'
                let M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-'
                let D = date.getDate() + ' '
                let h = date.getHours() + ':'
                let m = date.getMinutes() + ':'
                let s = date.getSeconds()
                return Y+M+D+h+m+s
            },
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
                    baseURL + '/topicConsumerGroup',
                    {params: {
                            env: this.value,
                            topic: this.input1,
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
                            'consumer_group': _data[i]['consumer_group'],
                            'topic': _data[i]['topic'],
                            'broker_name': _data[i]['broker_name'],
                            'queueId': _data[i]['queueId'],
                            'broker_offset': _data[i]['broker_offset'],
                            'consumer_offset': _data[i]['consumer_offset'],
                            'diff_offset': _data[i]['diff_offset'],
                            'diff_total': _data[i]['diff_total'],
                            'consumer_id': _data[i]['consumer_client'],
                            'last_update_timestamp': _data[i]['last_update_timestamp']
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
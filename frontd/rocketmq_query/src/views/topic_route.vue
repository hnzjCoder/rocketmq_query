<template>
    <el-row >
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
                :default-sort = "{prop: 'broker_name'}"
                fit:true>
            <el-table-column
                    prop="broker_name"
                    label="broker_name"
                    width="180px"
            >
            </el-table-column>
            <el-table-column
                    prop="broker_addr_master"
                    label="broker_addr_master"
                    width="300px">
            </el-table-column>
            <el-table-column
                    prop="broker_addr_slave"
                    label="broker_addr_slave"
                    width="300px">
            </el-table-column>
            <el-table-column
                    prop="broker_perm"
                    label="broker_perm"
                    width="300px">
            </el-table-column>
            <el-table-column
                    prop="broker_readQueueNums"
                    label="broker_readQueueNums"
                    width="200px">
            </el-table-column>
            <el-table-column
                    prop="broker_writeQueueNums"
                    label="broker_writeQueueNums"
                    width="200px"
            >
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
                input1: 'order-service',
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
                    baseURL + '/topicRoute',
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
                    // eslint-disable-next-line no-console
                    console.log('返回值', res.body)
                    // eslint-disable-next-line no-console
                    console.log('返回值data', res.body['data'])
                    let _data = res.body['data']
                    if (_data === 'null'){
                        this.load_failed(res.body['errMsg'])
                        this.loading = false
                        return this.tableData, this.loading
                    }
                    let _brokerData = _data['brokerDatas']
                    let _queueData = _data['queueDatas']
                    // eslint-disable-next-line no-console
                    console.log('原数据',_data)
                    // eslint-disable-next-line no-console
                    console.log('长度', _data.length)

                    for (let i=0;i<_brokerData.length;i++){
                        for (let m=0;m<_queueData.length;m++){
                            let _brokername = _brokerData[i]['brokerName']
                            if ( _queueData[m]['brokerName'] == _brokername) {
                                _tableData.push({
                                    'broker_name': _brokername,
                                    'broker_addr_master': _brokerData[i]['brokerAddrs'][0],
                                    'broker_addr_slave':  _brokerData[i]['brokerAddrs'][1],
                                    'broker_perm': _queueData[m]['perm'],
                                    'broker_readQueueNums': _queueData[m]['readQueueNums'],
                                    'broker_writeQueueNums': _queueData[m]['writeQueueNums']
                                })
                            }

                        }
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
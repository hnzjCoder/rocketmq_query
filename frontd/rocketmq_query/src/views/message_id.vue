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
        </div>
        </el-col>
        <el-col :span="4"><div class="grid-content bg-purple-light"></div>
            <div class="demo-input-suffix">
                <el-input
                        maxlength="400"
                        type="text"
                        rows="1"

                        placeholder="请输入内容"
                        v-model="input2">
                    <template slot="prepend">MessageId</template>
                </el-input>
            </div>
        </el-col>
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
            <el-button type="primary" v-on:click=load_data() @click="loading=true"  icon="el-icon-search">搜索</el-button>
        </el-col>
        <el-table
                :data="tableData_info"
                v-loading="loading"
                height="200px"
                border
                style="width: 100%"
                fit:true>
            <el-table-column
                    prop="topic"
                    label="topic"
                    width="180px">
            </el-table-column>
            <el-table-column
                    prop="message_key"
                    label="message_key"
                    width="300px">
            </el-table-column>
            <el-table-column
                    prop="message_uniq_key"
                    label="message_uniq_key"
                    width="300px">
            </el-table-column>
            <el-table-column
                    prop="tag"
                    label="Tag"
                    width="180px">
            </el-table-column>
            <el-table-column
                    prop="born_host"
                    label="BronHost"
                    width="180px"
                    >
            </el-table-column>
            <el-table-column
                    prop="born_time"
                    label="born_time"
                    :formatter="born_timestampToTime"
                    width="180px"
                    >
            </el-table-column>

            <el-table-column
                    prop="store_host"
                    label="store_host"
                    width="180px">
            </el-table-column>
            <el-table-column
                    prop="store_time"
                    label="store_time"
                    :formatter="store_timestampToTime"
                    width="180px">
            </el-table-column>

            <el-table-column
                    prop="message_body"
                    label="message_body"
                    min-width="180px">
            </el-table-column>
        </el-table>
        <el-table
                :data="tableData_properties"
                height="100"
                border
                style="width: 100%; margin-top: 50px"
                v-loading="loading">
            <el-table-column
                    prop="properties"
                    label="properties"
                    width="500px">
            </el-table-column>

        </el-table>
        <el-table
                :data="tableData"
                height="750"
                border
                style="width: 100%; margin-top: 50px"
                v-loading="loading"
                :default-sort = "{prop: 'track_type'}">
            <el-table-column
                    prop="consumergroup"
                    label="consumerGroup"
                    width="500px">
            </el-table-column>
            <el-table-column
                    prop="track_type"
                    label="trackType"
                    width="300px">
            </el-table-column>
            <el-table-column
                    prop="exception"
                    label="Exception"
                    min-width="300px">
            </el-table-column>
        </el-table>

    </el-row>




</template>

<script>
    import { baseURL } from "./baseConfig";

    export default {
        name: "message_id",
        data() {
            return {
                tableData: [],
                tableData_info:[],
                tableData_properties:[],
                input1: 'order-service',
                input2: '0AC8145C0001774598770B23714D000A',
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

        methods : {
            born_timestampToTime (row,) {
                let date = new Date(row.born_time) //时间戳为10位需*1000，时间戳为13位的话不需乘1000
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
            store_timestampToTime (row,) {
                let date = new Date(row.store_time) //时间戳为10位需*1000，时间戳为13位的话不需乘1000
                let Y = date.getFullYear() + '-'
                let M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-'
                let D = date.getDate() + ' '
                let h = date.getHours() + ':'
                let m = date.getMinutes() + ':'
                let s = date.getSeconds()
                return Y+M+D+h+m+s
            },
            load_data: function () {
                this.tableData = []
                this.$http.get(
                    baseURL + '/msgById',
                    {
                        params: {
                            env: this.value,
                            topic: this.input1,
                            msgId: this.input2
                        },
                        headers: {
                            'Access-Control-Allow-Origin': '*'
                        }
                    },
                ).then(function (res) {
                    // eslint-disable-next-line no-console
                    console.log('请求环境', this.value)
                    let _tableData = []
                    let _tableData_info = []
                    let _tableData_properties = []
                    // eslint-disable-next-line no-console
                    console.log('返回数据', res.body['data'])
                    let _msg_track_list_data = res.body['data']['messageTrackList']
                    if (_msg_track_list_data === 'null'){
                        this.load_failed(res.body['errMsg'])
                        this.loading = false
                        return this.tableData, this.loading
                    }
                    let _msg_message_view = res.body['data']['messageView']
                    if (_msg_message_view === 'null'){
                        this.load_failed(res.body['errMsg'])
                        this.loading = false
                        return this.tableData, this.loading
                    }

                    _tableData_properties.push({
                        'properties': _msg_message_view['properties'].value
                    })
                    this.tableData_properties = _tableData_properties
                    // eslint-disable-next-line no-console
                    console.log('tableData_properties', this.tableData_properties)
                    //构造tableData_info数据
                    _tableData_info.push({
                        'topic': _msg_message_view['topic'],
                        'born_host': _msg_message_view['bornHost'],
                        'born_time': _msg_message_view['bornTimestamp'],
                        'message_body': _msg_message_view['messageBody'],
                        'message_key': _msg_message_view['properties']['KEYS'],
                        'message_uniq_key': _msg_message_view['properties']['UNIQ_KEY'],
                        'tag': _msg_message_view['properties']['TAGS'],
                        'store_host': _msg_message_view['storeHost'],
                        'store_time': _msg_message_view['storeTimestamp']
                    })
                    this.tableData_info = _tableData_info



                    // eslint-disable-next-line no-console
                    console.log('原始数据', _msg_track_list_data)
                    // eslint-disable-next-line no-console
                    console.log('长度', _msg_track_list_data.length)
                    for (let i = 0; i < _msg_track_list_data.length; i++) {
                        // eslint-disable-next-line no-console
                        console.log('我是数据', _msg_track_list_data[i])
                        _tableData.push({
                            'consumergroup': _msg_track_list_data[i]['consumerGroup'],
                            'track_type': _msg_track_list_data[i]['trackType'],
                            'exception': _msg_track_list_data[i]['exceptionDesc']
                        }),
                            // eslint-disable-next-line no-console
                            console.log('_tableData', _tableData)

                    }
                    this.tableData = _tableData
                    let _loading = false
                    this.loading = _loading
                    // eslint-disable-next-line no-console
                    console.log('我又被点击了', _tableData)
                    this.load_success()
                    return this.tableData, this.loading


                })
            },
        }

    }


</script>

<style scoped>

</style>
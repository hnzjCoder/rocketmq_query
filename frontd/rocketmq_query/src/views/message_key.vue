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
            <div class="demo-input-suffix">
                <el-input
                        maxlength="400"
                        type="text"

                        rows="1"

                        placeholder="请输入内容"
                        v-model="input2">
                    <template slot="prepend">Messagekey</template>
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
            <div class="demo-input-suffix">
                <el-button type="primary" v-on:click=load_data() @click="loading=true" icon="el-icon-search">搜索</el-button>
            </div>
        </el-col>
        <el-table
                :data="tableData"
                border
                fit:true
                height="1000"
                v-loading="loading"
                style="width: 100%; margin-top: 50px">
            <el-table-column
                    prop="message_key"
                    label="message_key"
                    width="180px">
            </el-table-column>
            <el-table-column
                    prop="message_id"
                    label="message_id"
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
                    label="born_host"
                    width="180px">
            </el-table-column>
            <el-table-column
                    :formatter="born_timestampToTime"
                    prop="born_time"
                    label="born_time"
                    width="180px">
            </el-table-column>
            <el-table-column
                    prop="store_host"
                    label="store_host"
                    width="180px">
            </el-table-column>
            <el-table-column
                    :formatter="store_timestampToTime"
                    prop="store_time"
                    label="store_time"
                    width="180px">
            </el-table-column>
            <el-table-column
                    prop="message_body"
                    label="message_body"
                    min-width="180px">
            </el-table-column>
        </el-table>
    </el-row>




</template>

<script>
    import { baseURL } from "./baseConfig";
    export default {
        name: "message_key",
        data() {
            return {
                tableData: [],
                input1: 'order-service',
                input2: '441377546995505152',
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
        methods: {
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
                    baseURL + '/msgByKey',
                    {params: {
                            env: this.value,
                            topic: this.input1,
                            msgKey: this.input2
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
                    for (let i=0; i<_data.length; i++){
                        // eslint-disable-next-line no-console
                        console.log('我是数据', _data[i])
                        _tableData.push({
                            'message_body': _data[i]['messageBody'],
                            'store_host': _data[i]['storeHost'],
                            'store_time': _data[i]['storeTimestamp'],
                            'message_uniq_key': _data[i]['properties']['UNIQ_KEY'],
                            'message_key': _data[i]['properties']['KEYS'],
                            'tag': _data[i]['properties']['TAGS'],
                            'born_time': _data[i]['bornTimestamp'],
                            'born_host': _data[i]['bornHost'],
                            'message_id': _data[i]['msgId']
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
            },

        }

    }


</script>

<style scoped>

</style>
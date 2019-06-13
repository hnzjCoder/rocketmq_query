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
                    <template slot="prepend">Tag</template>
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
        <el-button type="primary" v-on:click=load_data()  @click="loading=true" icon="el-icon-search">搜索</el-button>
        </el-col>
        <el-table
                :data="tableData"
                ref="multipleTable"
                border
                v-loading="loading"
                style="width: 100%"
                height="1000px"
                >
            <el-table-column
                    prop="consumergroup"
                    label="consumerGroup"

                    style="width: 100%">
            </el-table-column>
        </el-table>
    </el-row>

</template>

<script>

    import { baseURL } from "./baseConfig";
    export default {

        name: "ConsumerGroupTag",
        components:{},
        data() {
            return {
                tableData: [],
                input1: 'order-service',
                input2: '*',
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
                // eslint-disable-next-line no-console
                console.log('我被点击了')
                // eslint-disable-next-line no-console
                console.log('env',this.value)
                this.$http.get(
                    baseURL + '/consumerGroupByTag',
                    {params: {
                        env: this.value,
                        topic: this.input1,
                        tag: this.input2
                    },
                    headers:{
                        'Access-Control-Allow-Origin':'*'
                    }},

                ).then(function (res) {

                    let _tableData = []
                    let _data = res.body['data']
                    if (_data === 'null'){
                        this.load_failed(res.body['errMsg'])
                        this.loading = false
                        return this.tableData, this.loading
                    }
                    // eslint-disable-next-line no-console
                    console.log('长度', _data.length)
                    for (let  i = 0; i<=_data.length; i++){
                        // eslint-disable-next-line no-console
                        console.log('我是数据', _data[i])
                        _tableData.push({
                            'consumergroup': _data[i]
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
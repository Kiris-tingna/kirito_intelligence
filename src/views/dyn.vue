<style>
.ivu-block {
    width: 320px;
    display: inline-block;
    height: 340px;
}
</style>
<template>
<Row>
    <Col span="17" style="min-width: 650px; max-width: 700px">
    <span class="ivu-inline-align">&nbsp; *contribution of major actors &nbsp;</span>
    <div>
        <div id="ivu-circle-1" class="ivu-block"></div>
        <div id="ivu-circle-2" class="ivu-block"></div>
        <div id="ivu-circle-3" class="ivu-block"></div>
        <div id="ivu-circle-4" class="ivu-block"></div>
        <div id="ivu-circle-5" class="ivu-block"></div>
    </div>
    </Col>
    <Col span="7">
        <div style="margin-left: 50px">
        <h1>Dynamic Contribution of Major Actors</h1>
        <span style="color: rgb(158, 167, 180);">
            contribution of actors evolve during releasing a film
        </span>
        </div>
        <Form :model="form" :label-width="50" style="margin-top: 20px;">
            <FormItem label="movie">
            <Select v-model="form.fname" clearable>
                <Option v-for="item in filmList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="vimpact()" long>Repaint</Button>
            </FormItem>
        </Form>
    </Col>
</Row>
</template>

<script>
import echarts from 'echarts';
import {getdyn, postdyn, getlist} from '../apis.js';
export default {
    data(){
        return {
            filmList: [
                {label:'\u6218\u72fc2', value:'\u6218\u72fc2'},
                {label:'\u6625\u5a07\u6551\u5fd7\u660e', value:'\u6625\u5a07\u6551\u5fd7\u660e'},
                {label:'\u5efa\u519b\u5927\u4e1a', value:'\u5efa\u519b\u5927\u4e1a'},
                {label:'\u609f\u7a7a\u4f20', value:'\u609f\u7a7a\u4f20'}
            ],

            form: {
                fname: ''
            },
            CircleOption: {
                backgroundColor: '#fff',
                title: {
                    text: '',
                    subtext: '',
                    x:'center'
                },
                tooltip: {
                    trigger: 'item',
                    confine: true,
                    formatter: "{a} <br/>{b} : {d}%"
                },
                legend: {
                    type: 'scroll',
                    orient: 'horizontal',
                    itemHeight: 12,
                    itemWidth: 15,
                    x : 'center',
                    y : 'bottom'
                },
                toolbox: {
                    show : false
                },
                calculable : true,
                series : [
                    {
                        name: '',
                        type:'pie',
                        radius : ['12%', '40%'],
                        roseType : 'radius',
                        data:[]
                    }
                ]
            }
        }
    },
    mounted: function(){
        this.vlist();

        this.circhart1 = echarts.init(document.getElementById('ivu-circle-1'));
        this.circhart2 = echarts.init(document.getElementById('ivu-circle-2'));
        this.circhart3 = echarts.init(document.getElementById('ivu-circle-3'));
        this.circhart4 = echarts.init(document.getElementById('ivu-circle-4'));
        this.circhart5 = echarts.init(document.getElementById('ivu-circle-5'));

        this.getcontribute();
    },
    methods: {
        vlist(){
            getlist().then(res => {
                this.filmList = res.data
            })
        },
        vimpact () {
            postdyn({filter: this.form}).then(res => {
                this.drawContribute([this.circhart1, this.circhart2, this.circhart3, this.circhart4, this.circhart5], res.data)
            })
        },
        deepClone(obj){
            var result = typeof obj.splice === 'function'?[]:{},key;
            if (obj && typeof obj === 'object'){
                for (key in obj ){
                    if (obj[key] && typeof obj[key] === 'object'){
                        result[key] = this.deepClone(obj[key]);
                    }else{
                        result[key] = obj[key];
                    }
                }
                return result;
            }
            return obj;
        },
        getcontribute() {
            getdyn().then(res => {
                this.drawContribute([this.circhart1, this.circhart2, this.circhart3, this.circhart4, this.circhart5], res.data)
            })
        },
        drawContribute(obj, data){
            for(var i in data){
                var movie = data[i].name

                var singleConfig = this.deepClone(this.CircleOption)
                singleConfig.title.subtext = 'Util Released No. '+ movie +' week'
                singleConfig.series[0].name = 'Util Released No. '+ movie +' week'

                var len = data[i].value[0].length
       
                for (var j = 0; j<len; j++){
                    singleConfig.series[0].data.push({name:data[i].value[0][j], value: data[i].value[1][j]})
                }
                obj[i].setOption(singleConfig)
            }
        }
    }
}


</script>
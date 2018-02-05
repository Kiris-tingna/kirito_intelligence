<style>
.ivu-bar-con{
    width: 48%;
    display: inline-block;
    height: 350px;
}
.ivu-prd-price{
    font-size: 25px;
    padding-left: 30px;
    color: #495060;
}
</style>

<template>
<Row>
    <Col span="16">
        <div id="ivu-bar-chart1" class="ivu-bar-con"></div>
        <div id="ivu-bar-chart2" class="ivu-bar-con"></div>
        <div id="ivu-bar-chart3" class="ivu-bar-con"></div>
        <div id="ivu-bar-chart4" class="ivu-bar-con"></div>
    </Col>
    <Col span="7">
        <div style="margin-left: 50px">
        <h1>Predition</h1>
        <span style="color: rgb(158, 167, 180);">
            premiere week box-oce predicting
        </span>
        </div>
        <Form :model="form" :label-width="50" style="margin-top: 20px;">
            <FormItem label="add actor">
                <Input v-model="form.ainputValue" icon="android-contact" placeholder="Enter something..." style="width: 200px"></Input>
                <Button type="primary" icon="plus-round" @click="handleActorConfirm()"></Button>
            </FormItem>

            <FormItem label="actors">
                <Tag  v-for="tag in form.wactor" :key="tag" closable @on-close="handleClose_actor(tag)"> {{tag}} </Tag>
            </FormItem>

            <FormItem label="add director">
                <Input v-model="form.dinputValue" icon="film-marker" placeholder="Enter something..." style="width: 200px"></Input>
                <Button type="primary" icon="plus-round" @click="handleDirConfirm()"></Button>
            </FormItem>

            <FormItem label="directors">
                <Tag  v-for="tag in form.wdirector" :key="tag" closable @on-close="handleClose_director(tag)"> {{tag}} </Tag>
            </FormItem>

            <FormItem label="year">
                <Select v-model="form.wyear" clearable>
                    <Option v-for="item in form.years" :value="item.value" :key="item.value">{{ item.label }}</Option>
                </Select>
            </FormItem>

            <FormItem label="scheldue">
                <Select v-model="form.wschedule" clearable>
                    <Option v-for="item in form.options" :value="item.value" :key="item.value">{{ item.label }}</Option>
                </Select>
            </FormItem>

            <FormItem>
                <Button type="primary" @click="vprediction()">Predict</Button>
            </FormItem>

            <FormItem label="estimate">
                <div class="ivu-prd-price"> <Icon type="social-yen-outline"></Icon>{{form.wprice}} </div>
            </FormItem>
        </Form>
    </Col>
</Row>
</template>

<script>
import echarts from 'echarts';
import {getprd, postprd} from '../apis.js';
export default {
    data(){
        return {
            form: {
                wactor: ['杨幂yangmi', '李易峰yifengli'],
                wdirector: [],
                wyear: 2017,
                years: [
                    {
                      value: 2017,
                      label: '2017年'
                    }, {
                      value: 2016,
                      label: '2016年'
                    }, {
                      value: 2015,
                      label: '2015年'
                    }, {
                      value: 2014,
                      label: '2014年'
                    }, {
                      value: 2013,
                      label: '2013年'
                    }
                ],
                wschedule: '1',
                wprice: '184.55 million',
                ainputValue: '',
                dinputValue: '',
                options: [
                    {
                      value: '1',
                      label: '寒假档'
                    }, {
                      value: '2',
                      label: '五一档'
                    }, {
                      value: '3',
                      label: '暑假档'
                    }, {
                      value: '4',
                      label: '国庆档'
                    }, {
                      value: '5',
                      label: '其他'
                    }
                ],
            },
            barOption: {
                title: { text: '', left:'center', bottom: '10px'},
                backgroundColor: '#fff',
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                color: ['#4894e1', '#24d1d9'],
                legend: {
                    data: ['predict', 'actual']
                },
                toolbox: {
                    show: true,
                    orient: 'vertical',
                    left: 'right',
                    top: 'center',
                    feature: {
                        mark: {show: true},
                        dataView: {show: true, readOnly: false},
                        magicType: {show: true, type: ['line', 'stack', 'tiled']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                grid: {  
                    left: '2%',
                    containLabel: true  
                },
                calculable: true,
                xAxis: [
                    {
                        type: 'category',
                        axisTick: {show: true},
                        data: []
                    }
                ],
                yAxis: [
                    {
                        type: 'value'
                    }
                ],
                series: [
                    {
                        name: 'predict',
                        type: 'bar',
                        barGap: 0,
                        data: []
                    },
                    {
                        name: 'actual',
                        type: 'bar',
                        data: []
                    }
                ]
            }
        }
    },
    mounted: function () {
        this.barchart1 = echarts.init(document.getElementById('ivu-bar-chart1'));
        this.barchart2 = echarts.init(document.getElementById('ivu-bar-chart2'));
        this.barchart3 = echarts.init(document.getElementById('ivu-bar-chart3'));
        this.barchart4 = echarts.init(document.getElementById('ivu-bar-chart4'));
        this.getPrediction();
    },
    methods: {
        handleClose_actor(tag){
            this.form.wactor.splice(this.form.wactor.indexOf(tag), 1);
        },
        handleClose_director(tag){
            this.form.wdirector.splice(this.form.wdirector.indexOf(tag), 1);
        },
        handleActorConfirm() {
            let inputValue = this.form.ainputValue;
            if (inputValue) {
                this.form.wactor.push(inputValue);
            }
            this.form.ainputValue = '';
        },
        handleDirConfirm() {
            let inputValue = this.form.dinputValue;
            if (inputValue) {
                this.form.wdirector.push(inputValue);
            }
            this.form.dinputValue = '';
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
        vprediction(){
            postprd({dirlist: this.form.wdirector, actlist: this.form.wactor, year: this.form.wyear, schedule: this.form.wschedule}).then(res => {
                this.form.wprice = (res.data.value/100).toFixed(2) + '  million'
            })
        },
        getPrediction(){
            getprd().then(res => {
                this.DrawPrediction([this.barchart1, this.barchart2, this.barchart3, this.barchart4], res.data)
            })
        },
        DrawPrediction(objs, data){
            for(var i in data) {
                var _option = this.deepClone(this.barOption)
                var item = data[i]
                _option.title.text = item.filmname
                _option.series[0].data = item.value[0].value
                _option.series[1].data = item.value[1].value
                _option.xAxis[0].data = ['1th week', '2th week', '3th week', '4th week']
                objs[i].setOption(_option)
            }
        }
    }
}
</script>
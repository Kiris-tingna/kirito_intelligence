<style lang="less">
.ivu-overview-block {
    width: 200px;
    display: inline-block;

    .ivu-overview-number {
        font-size: 30px;
    }
}
.ivu-overview-chart{
    width: 100%;
    height: 400px;
}
</style>
<template>
<Row>
    <Col span="24">
        <h1> <Icon type="ios-pulse"></Icon> &nbsp;Data Overview</h1>
        <Row style="margin-top: 20px; padding-left: 40px;">
        <div class="ivu-overview-block">
            <div class="ivu-overview-number"><Icon type="person-stalker"></Icon> &nbsp;3,172</div>
            <p style="color:#80848f; line-height: 1.5">Chinese Actors and Directors</p>
        </div>
        <div class="ivu-overview-block">
            <div class="ivu-overview-number"><Icon type="android-film"></Icon> &nbsp;970</div>
            <p style="color:#80848f; line-height: 1.5">Chinese Films</p>
        </div>
        <div class="ivu-overview-block">
            <div class="ivu-overview-number"><Icon type="link"></Icon> &nbsp;10,667</div>
            <p style="color:#80848f; line-height: 1.5">links of relation</p>
        </div>
        <div class="ivu-overview-block">
            <div class="ivu-overview-number"><Icon type="ios-calendar-outline"></Icon> &nbsp;7</div>
            <p style="color:#80848f; line-height: 1.5">year spanning</p>
        </div>
        <div class="ivu-overview-block">
            <div class="ivu-overview-number"><Icon type="android-chat"></Icon> &nbsp;88,359</div>
            <p style="color:#80848f; line-height: 1.5">movie reviews</p>
        </div>
        </Row>
    </Col>

    <Col span="24">
    <Row style="margin-top: 40px">
    <h1><Icon type="stats-bars"></Icon> &nbsp; Personas of Actors and Directors</h1>
    <Row style="margin-top: 10px; padding-left: 30px">
    <Col span="12">
        <Form :model="form" :label-width="50">
            <FormItem label="actor">
            <Row>
                <Col span="16">
                    <Select v-model="form.actor" clearable>
                        <Option v-for="item in actList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </Col>
                <Col span="4" offset="1"><Button type="primary" @click="vactor()">Get Personas</Button></Col>
            </Row>
            </FormItem>
        </Form>
        <div id="ivu-overview-actor" class="ivu-overview-chart"></div>
    </Col>
    
    <Col span="12">
        <Form :model="form" :label-width="50">
            <FormItem label="director">
            <Row>
                <Col span="16">
                    <Select v-model="form.dir" clearable>
                        <Option v-for="item in dirList" :value="item.value" :key="item.value">{{ item.label }}</Option>
                    </Select>
                </Col>
                <Col span="4" offset="1"><Button type="primary" @click="vdir()">Get Personas</Button></Col>
            </Row>
            </FormItem>
        </Form>
        <div id="ivu-overview-director" class="ivu-overview-chart"></div>
    </Col>
    </Row>
    </Row>
    </Col>
</Row>
</template>
<script>
import echarts from 'echarts';
import {
    getacts, getdirs, 
    getactpic, getdirpic,
    postactpic, postdirpic
} from '../apis.js';
export default {
    data(){
        return {
            actList: [],
            dirList: [],
            form: {
                actor: '',
                dir: ''
            },
            LineOption: {
                backgroundColor: '#fff',
                color: ['#55a9ec', '#675bba', 'rgb(25, 183, 207)'],
                title: {
                    text: '',
                    subtext: ''
                },
                tooltip: {
                    trigger: 'axis'
                },
                grid: {  
                    left: '3%',  
                    right: '4%',  
                    top: '20%', 
                    bottom: "6%",
                    containLabel: true  
                },
                legend: {
                    data:['Box-Office', 'Box-Office Score', 'Public Praise Score']
                },
                xAxis:  {
                    type: 'category',
                    name: '\n films over past five years',
                    nameLocation: 'middle',
                    boundaryGap: true,
                    data: []
                },
                yAxis: [{
                    name:'Box-Office',
                    type: 'value',
                    splitLine:{
                        show: false
                    },
                    axisLabel: {
                        formatter:function (value){
                            return (value /100 )+'million';
                        }
                    },
                },{
                    name:'BOS',
                    type: 'value',
                    scale: true,
                    max: 10,
                    min: 0,
                    splitLine:{
                        show: false
                    },
                    axisLabel: {
                        formatter:function (value){
                            return value  + 'point';
                        }
                    }
                },{
                    name:'PPS',
                    type: 'value',
                    scale: true,
                    max: 10,
                    min: 0,
                    splitLine:{
                        show: false
                    },
                    offset:50,
                    axisLabel: {
                        formatter:function (value){
                            return value + 'point';
                        }
                    }
                }],
                series: [
                    {
                        name:'Box-Office',
                        type:'bar',
                        yAxisIndex:0,
                        data:[],
                        markPoint: {
                            data: [
                                {type: 'max', name: 'peak value'}
                            ]
                        },
                    },{
                        name:'Box-Office Score',
                        type:'line',
                        yAxisIndex:1,
                        data:[],
                        markLine: {
                            data: [
                                {
                                    symbol: 'none',
                                    label: {
                                    normal: {
                                        position: 'start',
                                        formatter: 'BOS Average'
                                    }
                                },
                                    type: 'average',
                                }
                            ]
                        }
                    },{
                        name:'Public Praise Score',
                        type:'line',
                        data:[],
                        yAxisIndex:2,
                        markLine: {
                            data: [
                                {
                                    symbol: 'none',
                                    label: {
                                    normal: {
                                        position: 'start',
                                        formatter: 'PPS Average'
                                    }
                                    },
                                    type: 'average',
                                }
                            ]
                        }
                    }
                ]
            }
        }
    },
    mounted: function() {
        this.vprepare();
        this.achart = echarts.init(document.getElementById('ivu-overview-actor'));
        this.dchart = echarts.init(document.getElementById('ivu-overview-director'));

        this.getactor()
        this.getdirector()
    },
    methods: {
        vprepare() {
            getacts().then(res => {
                this.actList = res.data.value.map(function (val, index) {return {value: val,label: val}})
            })
            getdirs().then(res => {
                this.dirList = res.data.value.map(function (val, index) {return {value: val,label: val}})
            })
        },
        vactor() {
            postactpic({actorname: this.form.actor}).then(res => {
                this.DrawPic(this.achart, res.data)
            })
        },
        vdir() {
            postdirpic({directorname: this.form.dir}).then(res => {
                this.DrawPic(this.dchart, res.data)
            })
        },
        getactor(){
            getactpic().then(res => {
                this.DrawPic(this.achart, res.data)
            })
        },
        getdirector(){
            getdirpic().then(res=> {
                this.DrawPic(this.dchart, res.data)
            })
        },
        DrawPic(obj, data){
            var inner_x = []
                
            for (var j in data[0].value){
                inner_x.push(data[0].value[j])
            }

            this.LineOption.xAxis.data = inner_x
            
            var _arr = []
            for (var k in inner_x){
                _arr.push({ 'name': data[0].value[k], 
                'year': data[1].value[k], 'price': data[2].value[k], 
                'pf': data[3].value[k], 'kb': data[4].value[k]})
            }
            this.actpf = _arr

            for (var i=0; i<3; i++){
                var inner_data = []
                
                // this.LineOption.series[i].name = data[i+2].name
                for (var j in data[i+2].value){
                    inner_data.push(data[i+2].value[j])
                }
                this.LineOption.series[i].data = inner_data
            }
            obj.setOption(this.LineOption)
        },

    }
}
</script>

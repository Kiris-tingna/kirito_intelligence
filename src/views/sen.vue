<style>
.ivu-line-block {
    width: 100%;
    height: 600px;
}
.ivu-sentiment {
    font-size: 28px;
    line-height: 30px;
    font-weight: 800;
    padding-left: 30px;
}
</style>
<template>
<Row>
    <Col span="17" style="min-width: 650px; max-width: 700px">
    <span class="ivu-inline-align">&nbsp; *sentiment curve &nbsp;</span>
    <div id="ivu-line" class="ivu-line-block"> </div>
    </Col>
    <Col span="7">
        <div style="margin-left: 50px">
        <h1>Sentiment Analyse</h1>
        <span style="color: rgb(158, 167, 180);">
            changable sentiment from reviews of a film
        </span>
        </div>
        <Form :model="form" :label-width="50" style="margin-top: 20px;">
            <FormItem label="movie">
            <Select v-model="form.fname" clearable>
                <Option v-for="item in filmList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="vsentiment()" long>Repaint</Button>
            </FormItem>

            <FormItem label="review">
                <Input v-model="form.texts" type="textarea" :rows="4" placeholder="Enter some Chinese text"></Input>
            </FormItem>

            <FormItem>
                <Button type="default" @click="vpority()" long>Judge Pority</Button>
            </FormItem>

            <FormItem label="name">
                <Tag v-for="item in analyseactor" :key="item" :name="item">{{ item }}</Tag>
            </FormItem>

            <FormItem label="sentiment">
               <div v-show="analysepority == '0'" class="ivu-sentiment" style="color: rgb(28, 100, 237)">NEGITIVE</div>
               <div v-show="analysepority == '1'" class="ivu-sentiment" style="color: rgb(255, 70, 131)">POSITIVE</div>
            </FormItem>

        </Form>
    </Col>
</Row>
</template>

<script>
import echarts from 'echarts';
import {getsent, postsent, getpority, postpority, getlist} from '../apis.js';
export default {
    data(){
        return {
            filmList: [
                {label:'\u6218\u72fc2', value:'\u6218\u72fc2'},
                {label:'\u6625\u5a07\u6551\u5fd7\u660e', value:'\u6625\u5a07\u6551\u5fd7\u660e'},
                {label:'\u5efa\u519b\u5927\u4e1a', value:'\u5efa\u519b\u5927\u4e1a'},
                {label:'\u609f\u7a7a\u4f20', value:'\u609f\u7a7a\u4f20'}
            ],
            analyseactor: [],
            analysepority: null,
            form: {
                fname: '建军大业',
                texts: '鹿哥演的真的不错啊，张艺兴也棒棒的，刘烨社长也是帅炸了',
            },
            LineOption: {
                title: {
                    text: 'Sentiment Trend of Film',
                    subtext: 'Example in MetricsGraphics.js',
                    left: 'center',
                    top: '90%'
                },
                tooltip: {
                    trigger: 'axis',
                },
                toolbox: {
                    show: false,
                    feature: {
                        dataZoom: {
                            yAxisIndex: 'none'
                        }
                    }
                },
                legend: {
                    data:['positive sentiment trend','negative sentiment trend']
                },
                dataZoom: [{
                    type: 'inside',
                    start: 0,
                    end: 100
                }, {
                    start: 0,
                    end: 100,
                    handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                    handleSize: '80%',
                    handleStyle: {
                        color: '#fff',
                        shadowBlur: 3,
                        shadowColor: 'rgba(0, 0, 0, 0.6)',
                        shadowOffsetX: 2,
                        shadowOffsetY: 2
                    }
                }],
                grid: {
                    top: '5%',
                    left: '3%',
                    right: '2%',
                    bottom: '10%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: [],
                    axisLabel: {
                        formatter: function (value, idx) {
                            var date = new Date(value);
                            return idx === 0 ? value : [date.getMonth() + 1, date.getDate()].join('-');
                        }
                    },
                    boundaryGap: false
                },
                yAxis: {
                    axisLabel: {
                        formatter: function (val) {
                            return val;
                        }
                    },
                    type: 'value'
                },
                series: [
                {
            name: 'Lower confidence line',
            type: 'line',
            data: [],
            lineStyle: {
                normal: {
                    opacity: 0
                }
            },
            stack: 'confidence-band',
            symbol: 'none'
        }, {
            name: 'Upper confidence line',
            type: 'line',
            data: [],
            lineStyle: {
                normal: {
                    opacity: 0
                }
            },
            areaStyle: {
                normal: {
                    color: '#ccc'
                }
            },
            stack: 'confidence-band',
            symbol: 'none'
        },
                {
                    name: 'positive sentiment trend',
                    type: 'line',
                    data: [],
                    smooth: true,
                    symbolSize: 6,
                    symbol: 'circle',
                    itemStyle: {
                        normal: {
                            color: 'rgb(255, 70, 131)'
                        }
                    },
                    areaStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgb(255, 158, 68)'
                            }, {
                                offset: 1,
                                color: 'rgb(255, 70, 131)'
                            }])
                        }
                    }
                },
        {
                    name: 'negative sentiment trend',
                    type: 'line',
                    data: [],
                    smooth: true,
                    symbolSize: 6,
                    symbol: 'circle',
                    itemStyle: {
                        normal: {
                            color: 'rgb(28, 100, 237)'
                        }
                    },
                    areaStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                                offset: 0,
                                color: 'rgb(51, 119, 249)'
                            }, {
                                offset: 1,
                                color: 'rgb(132, 166, 231)'
                            }])
                        }
                    }
                }]
            }
        }
    },
    mounted: function() {
        this.vlist();
        this.linechart = echarts.init(document.getElementById('ivu-line'));
        this.getsentiment();

        getpority().then(res => {
            this.analyseactor = res.data[0].value
            this.analysepority = res.data[1].value
        })
    },
    methods: {
        vpority() {
            postpority({moviename:this.form.fname, sentence: this.form.texts}).then(res => {
                this.analyseactor = res.data[0].value
                this.analysepority = res.data[1].value
            })
        },
        vlist(){
            getlist().then(res => {
                this.filmList = res.data
            })
        },
        vsentiment () {
            postsent({filter: this.form}).then(res => {
                this.drawSentiment(this.linechart, res.data)
            })
        },
        getsentiment() {
            getsent().then(res => {
                this.drawSentiment(this.linechart, res.data)
            })
        },
        drawSentiment(obj, data){
            this.LineOption.xAxis.data = data.pos.B.map(function (item) {
                return item.timestamp;
            });
            this.LineOption.series[0].data = data.pos.L.map(function (item) {
                return item.label;
            });
            this.LineOption.series[1].data = data.pos.U.map(function (item) {
                return item.label;
            });
            this.LineOption.series[2].data = data.pos.B.map(function (item) {
                return item.label;
            });
            this.LineOption.series[3].data = data.neg.B.map(function (item) {
                return item.label;
            });
            obj.setOption(this.LineOption)
        }
    }
}

</script>
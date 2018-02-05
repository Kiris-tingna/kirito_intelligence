<style>
#ivu-canvas{
    border: 1px dashed #d3d3d3;
    border-radius: 2px;
}
#legend{
    padding: 15px 50px;
    height: 100px;
}
.ivu-span-le{
    display: inline-block;
}
</style>

<template>
<Row>
    <Col span="17" style="min-width:700px">
        <canvas id="ivu-canvas" width="800px" height="500px"></canvas>
        <div id="ivu-webgl"></div>
        <Row class="ivu-canvas-notation">
        <Col span="15">
        <div>
            <span class="ivu-inline-align">&nbsp; *data source &nbsp;</span>
            <Tag checkable color="blue">douban</Tag>
            <Tag checkable color="blue">weibo</Tag>
            <Tag checkable color="blue">cbooo</Tag>
            <Tag checkable color="blue">entgroup</Tag>
        </div>
        <div>
            <span class="ivu-inline-align">&nbsp; *avaliable years of films &nbsp;</span>
            <Tag checkable >2012</Tag>
            <Tag checkable >2013</Tag>
            <Tag checkable >2014</Tag>
            <Tag checkable >2015</Tag>
            <Tag checkable >2016</Tag>
            <Tag checkable >2017</Tag>
        </div>
        <div>
        <span class="ivu-inline-align">&nbsp; *Using Chrome (canvas on Chrome to achieve higher performance) &nbsp;</span>
        </div>
        </Col>
 
        <Col span="9">
            <span class="ivu-inline-align">&nbsp; *node type mapping &nbsp;</span>
            <svg id="legend"></svg>
        </Col>
        </Row>

    </Col>
    <Col span="7">
        <div style="margin-left: 50px">
        <h1>Hetergenous Information Network</h1>
        <span style="color: rgb(158, 167, 180);">
            hetergenous network for alternative actors
        </span>
        </div>
        <Form :model="form" :label-width="50">
            <FormItem label="Range">
            <Row>
                <Col span="11">
                    <DatePicker type="year" placeholder="Select start year" format="yyyy" v-model="form.syear"></DatePicker>
                </Col>
                <Col span="2" style="text-align: center">-</Col>
                <Col span="11">
                    <DatePicker type="year" placeholder="Select end year" format="yyyy" v-model="form.eyear"></DatePicker>
                </Col>
            </Row>
            <Row>
            <p style="color:#80848f; line-height: 1.5">which means representing data of years range from first year picker to second year picker</p>
            </Row>
            </FormItem>
            <FormItem>
                <Button type="primary" @click="vyear()" long>Repaint</Button>
            </FormItem>

            <FormItem label="query actor">
                <Select v-model="form.queryact">
                    <Option v-for="item in form.actlist" :value="item" :key="item">{{item}}</Option>
                </Select>
                <p style="color:#80848f; line-height: 1.5">which means chooseing an actor and recommend an alternative actor from network with rate score</p>
            </FormItem>

            <FormItem label="Criterion">
                <RadioGroup v-model="form.pathtype">
                    <Radio label="A">AMTMA</Radio>
                    <Radio label="B">AMDMA</Radio>
                </RadioGroup>
                <p style="color:#80848f; line-height: 1.5">which means whether path instance is type of actor-movie-type-movie-actor or actor-movie-director-movie-actor</p>
            </FormItem>

            <FormItem>
                <Button type="default" @click="vactor()" long>Alternative Actor Query</Button>
            </FormItem>

            <FormItem v-show="form.pathtype == 'A'" label="AMTMA meta-path">
                <ul>
                    <li v-for="item in typeActorList">
                        <span class="ivu-span-le">{{ item.name }}</span>
                        <Rate allow-half show-text :value="(item.val * 5).toFixed(2)*1"></Rate>
                    </li>
                </ul>
            </FormItem>

            <FormItem v-show="form.pathtype == 'B'" label="AMDMA meta-path">
                <ul>
                    <li v-for="item in directorActorList">
                        <span class="ivu-span-le">{{ item.name }}</span>
                        <Rate allow-half show-text :value="(item.val * 5).toFixed(2)*1"></Rate>
                    </li>
                </ul>
                
            </FormItem>
        </Form>
    </Col>
</Row>

</div>

</template>

<script>
import * as d3 from 'd3';
import { legendColor } from 'd3-svg-legend';
import {
    gethin, posthin, 
    getsimlist, getsimact, postsimact
} from '../apis.js';

export default {
    data() {return {
        simulation: null,
        form: {
            syear: '2017-01-01',
            eyear: '2017-01-01',
            queryact: '吴京jingwu',
            actlist: [],
            pathtype: 'A'
        },
        typeActorList: [],
        directorActorList: [],
        network: {"nodes": [
            {"name": "d3", "group":1},
            {"name": "d3.svg", "group":1},
            {"name": "d3.svg.area", "group":1},
            {"name": "d3.svg.line", "group":2},
            {"name": "d3.scale", "group":2},
            {"name": "d3.scale.linear", "group":2},
            {"name": "d3.scale.ordinal", "group":3},
            {"name": "d3.scale.ordinal1", "group":3},
            {"name": "d3.scale.ordinal2", "group":3},
            {"name": "d3.scale.ordinal3", "group":4},
            {"name": "d3.scale.ordinal4", "group":4}
          ],
  "links": [
    {"source": 0, "target": 1, "value": 0.8},
    {"source": 1, "target": 2, "value": 0.5},
    {"source": 1, "target": 3, "value": 0.1},
    {"source": 0, "target": 4, "value": 0.2},
    {"source": 4, "target": 5, "value": 0.6},
    {"source": 4, "target": 6, "value": 0.1},
    {"source": 7, "target": 1, "value": 0.7},
    {"source": 7, "target": 2, "value": 0.4},
    {"source": 7, "target": 3, "value": 0.1},
    {"source": 8, "target": 4, "value": 0.1},
    {"source": 8, "target": 5, "value": 0.7},
    {"source": 8, "target": 6, "value": 0.1},
    {"source": 8, "target": 1, "value": 0.6},
  ]}
    }},
    mounted() {
        gethin().then(res => {
            this.network = res.data
            this.render(this.network)
        })
        getsimlist().then(res => {
            this.form.actlist = res.data.value
        })
        getsimact().then(res => {
            this.typeActorList = res.data[0].value
            this.directorActorList = res.data[1].value
        })
    },
    beforeRouteLeave (to, from, next){
        // 离开时时结束仿真回调
        this.simulation.stop();
        next()
    },
    methods: {
        vactor(){
            postsimact({actorname: this.form.queryact}).then(res => {
                this.typeActorList = res.data[0].value
                this.directorActorList = res.data[1].value
            })
        },
        vyear() {
            this.simulation.stop();
            posthin({ filter : this.form} ).then(res=>{
                this.network = res.data
                this.render(this.network)
            })
        },
        render(networks){
            let w = 800;
            let h = 500;
            let r = 5;
            // 颜色映射
            let colors = d3.scaleOrdinal(d3.schemeCategory10);
            // 画布
            let canvas = d3.select('canvas#ivu-canvas');
            let context = canvas.node().getContext("2d");
            // 缩放句柄
            let transform = d3.zoomIdentity;
            // 图例
            let svg = d3.select("svg#legend");
            let legendOrdinal = legendColor()
                .shape("path", d3.symbol().type(d3.symbolCircle).size(100)())
                .shapePadding(80)
                .scale(d3.scaleOrdinal(d3.schemeCategory10).domain(['actor node', 'director node', 'movie node']))
                .orient('horizontal');

            svg.call(legendOrdinal);

            // 力学仿真
            this.simulation = d3.forceSimulation()
                    .force("charge", d3.forceManyBody().strength(-28)) // strength 斥力
                    // .force("link", d3.forceLink().strength(function(d){return d.value}))
                    .force("link", d3.forceLink().distance(30).strength(1).iterations(10)) // strength 0.1-1
                    .force("x", d3.forceX())
                    .force("y", d3.forceY())
                    .force("center", d3.forceCenter(w / 2, h / 2))
                    .restart();

            // 画图帧- canvas
            var canvasDraw = function(context, networks, w, h, t){ // 画图
                context.save();
                context.clearRect(0, 0, w, h);
                context.beginPath();
                context.translate(t.x, t.y);
                context.scale(t.k, t.k);

                networks.links.forEach(function(d){
                    context.moveTo(d.source.x, d.source.y);
                    context.lineTo(d.target.x, d.target.y);
                });
                context.strokeStyle = "#999999";
                context.lineWidth = 1;
                context.globalAlpha=0.6;
                context.stroke();

                context.globalAlpha=1;
                context.strokeStyle = "#ffffff";
                context.lineWidth = 1.5;

                networks.nodes.forEach(function(d){
                    context.beginPath();
                    context.moveTo(d.x + r, d.y);
                    context.arc(d.x, d.y, r, 0, 2 * Math.PI);
                    context.fillStyle = colors(d.group);
                    context.fill();
                    context.stroke();
                });
                      
                    
                context.restore();
            };
            // 缩放
            var zoomed = function () {
                transform = d3.event.transform;
                canvasDraw(context, networks, w, h, transform);
            }

            canvas.call(d3.zoom().scaleExtent([1 / 4, 3]).on('zoom', zoomed));

            this.simulation.nodes(networks.nodes).on("tick", function(){
                canvasDraw(context, networks, w, h, transform);
            });

            this.simulation.force("link")
                .links(networks.links);
            

        }
    }
}
</script>
<style>
#ivu-svg{
    display: inline-block;
    height: 20px;
    width: 170px;
    margin-left: 20px;
    overflow: visible;
}
#ivu-svg .legendLinear{
    padding: 0;
    margin: 0;
}
.ivu-cluster-images {
    width: 600px;
    height: 180px;
}
.ivu-cluster-item{
    margin-left: 10px; 
    font-size: 10px; 
    line-height: 1.8
}
.ivu-cluster-radio {
    width: 35px;
}
</style>

<template>
<Row>
    <Col span="9" style=" min-width: 360px; max-width: 380px">
    <span class="ivu-inline-align">&nbsp; *heatmap of tf-idf &nbsp;</span>
        <canvas id="ivu-heatmap" style="min-height: 800px;"></canvas>
        <div>
            <span class="ivu-inline-align">&nbsp; *data source &nbsp;</span>
            <Tag checkable color="blue">www.acwind.net</Tag>
        </div>
        <div>
            <span class="ivu-inline-align">&nbsp; *avaliable years of animates &nbsp;</span>
            <Tag checkable >1950-1970</Tag>
            <Tag checkable >1970-1990</Tag>
            <Tag checkable >1990-2010</Tag>
            <Tag checkable >2010-2017</Tag>
        </div>
    </Col>
    <Col span="10">
        <div style="margin-left: 80px">
        <h1>Text Cluster</h1>
        <span style="color: rgb(158, 167, 180);">
            tf-idf vector heatmap and hierarchical clsutering
        </span>
        </div>

        <Form :model="form" :label-width="80" style="margin-top: 20px;">
            <FormItem label="Basic information">
                <div><Tag>tf-idf vector length</Tag> <span style="margin-left:20px">{{ weight.width }} dimensions</span></div>
                <div><Tag>shown document length</Tag> <span style="margin-left:20px">{{ weight.height }} items</span></div>
                <div><Tag>threshold</Tag> <span style="margin-left:20px">{{ clus.threshold }}</span></div>
                <div><Tag>clusters number</Tag> <span style="margin-left:20px">{{ clus.number }} clusters</span></div>
                <div style="vertical-align: top;"><Tag>tf-idf color mapping</Tag><svg id="ivu-svg"></svg></div>
            </FormItem>
            <FormItem label="Period">
            <Select v-model="form.period">
                <Option v-for="item in animeList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
            <p style="color:#80848f; line-height: 1.5">split all animate into pharesd period</p>
            </FormItem>
<!-- 
            <FormItem label="Cluster">
                <Input v-model="form.cluster" placeholder="Query Cluster Id (from 1 to end)"></Input>
                <p style="color:#80848f; line-height: 1.5">menas input a cluster id and return cluster entities</p>
            </FormItem>
 -->
            <FormItem label="Cluster">
                <RadioGroup v-model="form.cluster" type="button" size="small">
                    <Radio v-for="item in clus.clusters" :value="item.value" :key="item.value" :label="item.label" class="ivu-cluster-radio"></Radio>
                </RadioGroup>
                <p style="color:#80848f; line-height: 1.5">menas input a cluster id and return cluster entities</p>
            </FormItem>
            
            <FormItem>
                <Button type="primary" @click="vperiod()">Repaint</Button>
                <Button type="ghost" @click="vcluster()">Get Cluster</Button>
            </FormItem>

            <FormItem label="*cluster">
                <div class="ivu-cluster-item" style="width:600px"> {{ clus.cluster }}</div>
            </FormItem>

            <FormItem label="*word mapping (from left to right)">
                <div class="ivu-cluster-item" style="color: #a9a9a9; width:600px">'一位' '一只' '一同' '一名' '一场' '一年' '一点' '一种' '一群' '一部' '三个' '三人' '不可思议' '不明'
 '不知' '世界' '世纪' '东京' '东西' '两个' '两人' '个性' '中心' '主人公' '主角' '主题' '之下' '之中'
 '之间' '事件' '事情' '人气' '人物' '人生' '人类' '人设' '代表' '令人' '众多' '优秀' '伙伴' '作品' '作战'
 '作画' '作者' '依然' '侦探' '保护' '偶像' '偶然' '充满' '全新' '公主' '公司' '关系' '兵器' '内容' '再度'
 '冒险' '出版' '创作' '利用' '制作' '制造' '前往' '剧场版' '剧情' '力量' '动漫' '动画' '动画版' '努力'
 '包括' '单行本' '危机' '危险' '却是' '卷入' '历史' '原作' '原创' '原因' '原本' '参与' '参加' '友情'
 '发售' '发展' '发现' '发生' '发行' '变化' '变得' '召唤' '可爱' '各种各样' '合作' '同伴' '同学' '名为'
 '名叫' '名字' '吸引' '告诉' '周刊' '命运' '和平' '哥哥' '唯一' '喜剧' '喜欢' '回到' '围绕' '国家' '地方'
 '地球' '城市' '声优' '大陆' '天使' '天才' '天空' '太郎' '奇怪' '女主角' '女子' '女孩' '女孩子' '女性'
 '女生' '好友' '妖怪' '妹妹' '姐姐' '学习' '学园' '学校' '学生' '学院' '孩子' '宇宙' '守护' '家族' '对抗'
 '寻找' '封印' '将会' '小姐' '小学' '小说' '少女' '少年' '居住' '展开' '工作' '希望' '带来' '平凡' '年代'
 '年前' '年月日' '年轻' '幻想' '建立' '开发' '强大' '影响' '得知' '性格' '怪物' '恋爱' '恐怖' '情况'
 '情节' '想要' '意外' '感到' '感受' '感情' '感觉' '憧憬' '成功' '成员' '成长' '战争' '战士' '打算' '执导'
 '找到' '技术' '担任' '担当' '拥有' '拯救' '挑战' '接受' '控制' '推出' '描写' '描述' '搞笑' '播出' '播放'
 '改变' '改编' '攻击' '故事' '敌人' '方式' '旅程' '旅行' '无数' '日子' '日常' '日常生活' '日本' '时代'
 '时间' '更是' '最强' '最终' '月刊' '朋友' '期待' '未来' '本作' '机会' '机器人' '机械' '杂志' '来到'
 '某天' '某日' '校园' '梦想' '正式' '武器' '死亡' '毁灭' '母亲' '比赛' '永远' '活动' '消失' '消息' '渐渐'
 '游戏' '漫画' '漫画家' '灵魂' '爱情' '父亲' '父母' '物语' '特别' '王国' '王子' '现实' '生命' '生存'
 '生活' '生物' '电影' '电视' '电视台' '男主角' '男人' '男子' '画面' '留下' '登场' '监督' '目标' '目的'
 '相遇' '真实' '真的' '知名' '破坏' '社会' '神秘' '离开' '秘密' '称为' '第一' '等待' '系列' '组合' '组织'
 '终于' '经历' '结束' '统治' '继承' '美丽' '美国' '美少女' '老师' '背景' '能力' '自称' '舞台' '英雄'
 '著名' '表现' '袭击' '观众' '角色' '解决' '计划' '记忆' '讲述' '设定' '设计' '诞生' '该作' '负责' '超级'
 '踏上' '身上' '身为' '身份' '身体' '身边' '过程' '迎来' '这位' '这是' '这部' '连载' '选择' '途中' '遇见'
 '遥远' '邂逅' '邪恶' '部队' '都市' '配音' '阵容' '阻止' '陷入' '隐藏' '青年' '青春' '青梅竹马' '面前'
 '面对' '音乐' '预定' '题材' '风格' '高中' '高中生' '魅力' '魔法' '黑暗'</div>
            </FormItem>
            <FormItem label="*hierarchical tree (ward minimum variance)">
                <img src="../images/cluster.png" class="ivu-cluster-images">
            </FormItem>
        </Form>
    </Col>
</Row>
</template>

<script>
import * as d3 from 'd3';
import { legendColor } from 'd3-svg-legend';
import {getani, postani, postcluster} from '../apis.js';
export default {

    data() {return {
        animeList: [
            {label: '第1-1000动漫资料热力图', value: 1},
            {label: '第1001-2000动漫资料热力图', value: 2},
            {label: '第2001-3000动漫资料热力图', value: 3},
            {label: '第3001-最后动漫资料热力图', value: 4},
        ],
        form: {
            period: 1,
            cluster: '1'
        },
        clus: {
            threshold: 3.7,
            number: 27,
            clusters: [],
            cluster: ''
        },
        weight: {
            width: 2,
            height: 2,
            value: [0.5, 0.7, 0.2, 0.4]
        }
    }},
    mounted() {
        this.clus.clusters = this.createArray(this.clus.number);

        getani().then(res => {
            this.weight = res.data
            this.render(this.weight)
        })
        postcluster({ filter : this.form} ).then(res=>{
            this.clus.cluster = res.data
        })
    },
    methods: {
        // http://d3-legend.susielu.com/
        createArray(n) {
            return Array.from(new Array(n), (x, i) => ({ label: i + 1, value: i + 1 }));
        },
        vperiod() {
            postani({ filter : this.form} ).then(res=>{
                this.weight = res.data
                this.render(this.weight)
            })
        },
        vcluster() {
            postcluster({ filter : this.form} ).then(res=>{
                this.clus.cluster = res.data
            })
        },
        render(weight){
            //height of each row in the heatmap
            //width of each column in the heatmap

            let gridSize = 1;
            let ncol = weight.width;
            let nrow = weight.height;

            let width = gridSize * ncol;
            let height = gridSize * nrow;
            
            let canvas = d3.select('canvas#ivu-heatmap');
            canvas.attr('width', width).attr('height', height);

            let context = canvas.node().getContext("2d");
            let image = context.createImageData(width, height);
            let colorLow = 'green', colorMed = 'yellow', colorHigh = 'red';
            let colorScale = d3.scaleLinear()
                .domain([0, 0.5, 1])
                .range([colorLow, colorMed, colorHigh]);

            var svg = d3.select("svg#ivu-svg");
            svg.append("g")
                .attr("class", "legendLinear");

            var legendLinear = legendColor()
              .shapeWidth(30)
              .cells([0.1, 0.25, 0.5, 0.75, 1])
              .orient('horizontal')
              .scale(colorScale);

            svg.select(".legendLinear")
              .call(legendLinear);

            for (var t = 0, k = 0, l = 0; t < gridSize * nrow -1; ++t){ // 每行
                // 当前元素的颜色的控制
                if (!((t+1) % gridSize)){
                    k += ncol
                }

                for (var r = 0, j = k - 1; r < gridSize * ncol; ++r, l += 4){ // 每列
                    // 当前元素的颜色的控制
                    if (!(r % gridSize)){
                        ++j
                    }
                            
                    var c = d3.rgb(colorScale(weight.value[j]));
                    image.data[l + 0] = c.r;
                    image.data[l + 1] = c.g;
                    image.data[l + 2] = c.b;
                    image.data[l + 3] = 255;

                }

            }

            context.putImageData(image, 0, 0);
        }

        //     let svg = d3.select("#heatmap").append("svg")
        //         .attr('width', '200px').attr('height', '1000px')
        //         .attr('overflow-y', 'scroll')
        //         .append("g");

        //     let heatMap = svg.selectAll(".heatmap")
        //         .data(weight, function(d) { return d.row + ':' + d.col; })
        //         .enter().append("svg:rect")
        //         .attr("x", function(d) { return d.col * w; })
        //         .attr("y", function(d) { return d.row * h; })
        //         .attr("width", function(d) { return w; })
        //         .attr("height", function(d) { return h; })
        //         .style("fill", function(d) { return colorScale(d.value); });
        // }
    }
}
</script>

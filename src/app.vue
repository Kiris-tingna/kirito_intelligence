<style lang='less'>
@import "styles/common.less";

.layout{
    background: #f5f7f9;
    position: relative;
    overflow: hidden;

    .ivu-menu-dark{
        background: transparent !important;
    }

    // 左侧
    .layout-menu-left{
        position: fixed;
        top: 0;
        left: 0;
        bottom: 0;
        width: @left_menu_width;
        height: 100%;
        overflow-y: hidden;
        background: #464c5b;

        .layout-logo-left{
            width: 90%;
            height: 30px;
            color: #fff;
            font-size: 24px;
            line-height: 30px;
            text-align: center;
            background: #5b6270;
            border-radius: 3px;
            margin: 15px auto;
        }
    }

    // 右侧
    .layout-right{
        position: relative;
        margin-left: @left_menu_width;

        .layout-breadcrumb{
           padding: 10px 15px 0;
        }
        .layout-content{
            min-height: 500px;
            margin: 15px;
            overflow: hidden;
            background: #fff;
            border-radius: 4px;
            
            .layout-content-main{
              padding: 10px;
            }
        }

        .layout-copy{
            text-align: center;
            padding: 10px 0 20px;
            color: #9ea7b4;
        }
    }
}

</style>
<template>
    <div class="layout">
            <div class="layout-menu-left">
                <Menu active-name="hin" theme="dark" width="auto" :active-name="1" :open-names="['1']" :accordion="true" @on-select="urls">
                    <div class="layout-logo-left">SNIP</div>
                    <Submenu name="1">
                        <template slot="title">
                            <Icon type="ios-compose"></Icon>
                            Dashboard
                        </template>
                        <MenuItem name="/"> Dashboard</MenuItem>
                    </Submenu>
                    <Submenu name="2">
                        <template slot="title">
                            <Icon type="ios-analytics"></Icon>
                            Box-office
                        </template>
                        <MenuItem name="dyn">dynamic impact</MenuItem>
                        <MenuItem name="prd">box-office prediction</MenuItem>
                    </Submenu>
                    <Submenu name="3">
                        <template slot="title">
                            <Icon type="ios-navigate"></Icon>
                            Heterogeneous Networks
                        </template>
                        <MenuItem name="hin">movie hin analyse</MenuItem>
                    </Submenu>
                    <Submenu name="4">
                        <template slot="title">
                            <Icon type="ios-keypad"></Icon>
                            Sentiment Analyse
                        </template>
                        <MenuItem name="sen">film level sentiments</MenuItem>
                    </Submenu>
                    <Submenu name="5">
                        <template slot="title">
                            <Icon type="ios-keypad"></Icon>
                            Cluster
                        </template>
                        <MenuItem name="her">hierarchical clsuter</MenuItem>
                    </Submenu>
                </Menu>

            </div>
            <div class="layout-right">
                <div class="layout-breadcrumb">
                    <Breadcrumb>
                        <BreadcrumbItem >Home</BreadcrumbItem>
                        <BreadcrumbItem>{{this.$route.meta.bread}}</BreadcrumbItem>
                    </Breadcrumb>
                </div>
                <div class="layout-content">
                    <div class="layout-content-main" :style="contentHeight"><router-view></router-view></div>
                </div>
                <div class="layout-copy">
                    2017-2018 &copy; Kisitingna. All Rights Reserved.
                </div>
            </div>

    </div>
</template>
<script>
    export default {
        computed:{
            contentHeight: function(){
                var innerHeight = window.innerHeight;
                var contentHeight = innerHeight-100;
                return "min-height: "+contentHeight+"px";
            }
        },
        methods: {
            urls(router) {
                this.$router.push(router);
            }
        }
    }
</script>

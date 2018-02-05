const routers = [
    {
        path: '/',
        meta: {
            title: 'index',
            bread: 'dashboard'
        },
        component: (resolve) => require(['./views/dash.vue'], resolve)
    },
    {
        path: '/hin',
        meta: {
            title: 'hin',
            bread: 'movie heterogeneous networks analyse'
        },
        component: (resolve) => require(['./views/hin.vue'], resolve)
    },
    {
        path: '/her',
        meta: {
            title: 'her',
            bread: 'hierarchical clsuter'
        },
        component: (resolve) => require(['./views/her.vue'], resolve)
    },
    {
        path: '/dyn',
        meta: {
            title: 'dynamic',
            bread: 'dynamic impact'
        },
        component: (resolve) => require(['./views/dyn.vue'], resolve)
    },
    {
        path: '/sen',
        meta: {
            title: 'sentiment',
            bread: 'film level sentiment'
        },
        component: (resolve) => require(['./views/sen.vue'], resolve)
    },
    {
        path: '/prd',
        meta: {
            title: 'prediction',
            bread: 'phased box-office predicting'
        },
        component: (resolve) => require(['./views/prd.vue'], resolve)
    }
];
export default routers;
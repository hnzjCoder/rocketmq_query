import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'index',
      redirect:'/topic_route',
      component: () => import(/* webpackChunkName: "about" */ './views/index.vue'),
      meta: {
        hide:true,

      },

      children: [

        {
          path: 'producergroup_connection',
          name: 'producergroup_connection',
          component: () => import(/* webpackChunkName: "about" */ './views/producergroup_connection.vue')
        },
        {
          path: 'message_key',
          name: 'message_key',
          component: () => import(/* webpackChunkName: "about" */ './views/message_key.vue')
        },
        {
          path: 'message_id',
          name: 'message_id',
          component: () => import(/* webpackChunkName: "about" */ './views/message_id.vue')
        },
        {
          path: 'consumergroup_tag',
          name: 'consumergroup_tag',
          component: () => import(/* webpackChunkName: "about" */ './views/consumergroup_tag.vue')
        },
        {
          path: 'topic_route',
          name: 'topic_route',
          component: () => import(/* webpackChunkName: "about" */ './views/topic_route.vue')
        },
        {
          path: 'topic_status',
          name: 'topic_status',
          component: () => import(/* webpackChunkName: "about" */ './views/topic_status.vue')
        },
        {
          path: 'topic_consumergroup',
          name: 'topic_consumergroup',
          component: () => import(/* webpackChunkName: "about" */ './views/topic_consumergroup.vue')
        },  {
          path: 'consumergroup_status',
          name: 'consumergroup_status',
          component: () => import(/* webpackChunkName: "about" */ './views/consumergroup_status.vue')
        },  {
          path: 'consumergroup_connection',
          name: 'consumergroup_connection',
          component: () => import(/* webpackChunkName: "about" */ './views/consumergroup_connection.vue')
        }


      ]

    },



  ]
})

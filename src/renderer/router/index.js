import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [{
      path: '/',
      name: 'landing-page',
      component: require('@/components/LandingPage').default
    },
    {
      path: '/new',
      name: 'new-screen',
      component: require('@/components/NewScreen').default
    },
    {
      path: '/calibration',
      name: 'calibration',
      component: require('@/components/CalibrationScreen').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
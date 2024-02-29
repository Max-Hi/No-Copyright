import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage
  },
  {
    path: '/watch/:id',
    name: 'WatchVideo',
    component: () => import(/* webpackChunkName: "watch" */ '../views/WatchVideo.vue')
  },
  {
    path: '/tag/:tagname',
    name: 'Tag',
    component: () => import(/* webpackChunkName: "tag" */ '../views/Tag.vue')
  },
  {
    path: '/star/:starname',
    name: 'Star',
    component: () => import(/* webpackChunkName: "star" */ '../views/Star.vue')
  },
  {
    path: '/studio/:studioname',
    name: 'Studio',
    component: () => import(/* webpackChunkName: "studio" */ '../views/Studio.vue')
  },
  {
    path: '/tags',
    name: 'Tags',
    component: () => import(/* webpackChunkName: "tag" */ '../views/Tags.vue')
  },
  {
    path: '/stars',
    name: 'Stars',
    component: () => import(/* webpackChunkName: "star" */ '../views/Stars.vue')
  },
  {
    path: '/studios',
    name: 'Studios',
    component: () => import(/* webpackChunkName: "studio" */ '../views/Studios.vue')
  },
  {
    path: '/personal',
    name: 'Personal',
    component: () => import(/* webpackChunkName: "personal" */ '../views/Personal.vue')
  },
  {
    path: '/upload',
    name: 'Upload',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Upload.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Login Guard
router.beforeEach((to, from, next) => {
  if (store.getters['isAuthenticated']) {
    if (to.name === 'Login') next({name: 'LandingPage'})
    else next()
  } else {
    if (to.name !== 'Login')
      next({name: 'Login'})
    else next() // prevents infinite rerouting
  }
})

export default router

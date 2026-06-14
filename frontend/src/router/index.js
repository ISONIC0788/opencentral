import { createRouter, createWebHistory } from 'vue-router'
import Landing from '../views/Landing.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: Landing
    },
    {
      path: '/logs',
      name: 'logs',
      component: () => import('../views/Main.vue')
    },
    {
      path: '/auth/login',
      name: 'auth-login',
      component: () => import('../views/AuthLogin.vue')
    },
    {
      path: '/auth/callback',
      name: 'auth-callback',
      component: () => import('../views/AuthCallback.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue')
    },
    {
      path: '/docs',
      component: () => import('../views/Docs.vue'),
      children: [
        {
          path: '',
          redirect: '/docs/overview'
        },
        {
          path: 'overview',
          name: 'docs-overview',
          component: () => import('../views/docs/Overview.vue')
        },
        {
          path: 'viewing-logs',
          name: 'docs-viewing-logs',
          component: () => import('../views/docs/ViewingLogs.vue')
        },
        {
          path: 'python',
          name: 'docs-python',
          component: () => import('../views/docs/Python.vue')
        },
        {
          path: 'javascript',
          name: 'docs-javascript',
          component: () => import('../views/docs/JavaScript.vue')
        },
        {
          path: 'go',
          name: 'docs-go',
          component: () => import('../views/docs/Go.vue')
        },
        {
          path: 'rust',
          name: 'docs-rust',
          component: () => import('../views/docs/Rust.vue')
        },
        {
          path: 'php',
          name: 'docs-php',
          component: () => import('../views/docs/PHP.vue')
        },
      ]
    },
    {
      path: '/admin',
      component: () => import('../views/Admin.vue'),
      children: [
        {
          path: '',
          redirect: '/admin/overview'
        },
        {
          path: 'overview',
          name: 'admin-overview',
          component: () => import('../views/admin/Overview.vue')
        },
      ]
    }
  ]
})

export default router

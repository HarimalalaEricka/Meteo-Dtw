import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Analytics from '../views/Analytics.vue'
import Alerts from '../views/Alerts.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: { icon: '🏠', title: 'Dashboard' }
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: Analytics,
    meta: { icon: '📊', title: 'Analytics' }
  },
  {
    path: '/alerts',
    name: 'Alerts',
    component: Alerts,
    meta: { icon: '🚨', title: 'Alertes' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
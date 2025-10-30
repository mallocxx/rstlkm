import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from './stores/auth'

const Login = () => import('./views/Login.vue')
const Dashboard = () => import('./views/Dashboard.vue')
const Objects = () => import('./views/Objects.vue')
const Reports = () => import('./views/Reports.vue')
const Engineer = () => import('./views/Engineer.vue')

const router = createRouter({
	history: createWebHistory(),
	routes: [
		{ path: '/login', name: 'login', component: Login },
		{ path: '/', name: 'dashboard', component: Dashboard, meta: { requiresAuth: true } },
		{ path: '/objects', name: 'objects', component: Objects, meta: { requiresAuth: true } },
		{ path: '/engineer', name: 'engineer', component: Engineer, meta: { requiresAuth: true } },
		{ path: '/reports', name: 'reports', component: Reports, meta: { requiresAuth: true } },
	]
})

router.beforeEach((to) => {
	const auth = useAuthStore()
	if (to.meta.requiresAuth && !auth.isAuthenticated) {
		return { name: 'login', query: { redirect: to.fullPath } }
	}
})

export default router

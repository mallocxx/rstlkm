import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({
	baseURL: API_BASE,
})

// Initialize Authorization header from stored token on app start
const existingAccess = localStorage.getItem('access')
if (existingAccess) {
    (api.defaults.headers as any).common = (api.defaults.headers as any).common || {}
    api.defaults.headers.common['Authorization'] = `Bearer ${existingAccess}`
}

// Axios response interceptor to refresh token on 401 and retry once
let isRefreshing = false
let pendingQueue: Array<{ resolve: (token: string) => void; reject: (err: any) => void }> = []

function subscribeTokenRefresh(cb: (token: string) => void) { pendingQueue.push({ resolve: cb, reject: () => {} }) }
function onRefreshed(token: string) {
    pendingQueue.forEach(p => p.resolve(token))
    pendingQueue = []
}

export const useAuthStore = defineStore('auth', {
	state: () => ({
		access: localStorage.getItem('access') || '',
		refresh: localStorage.getItem('refresh') || '',
		user: null as null | { username: string },
	}),
	getters: {
		isAuthenticated: (s) => !!s.access,
	},
	actions: {
		async login(username: string, password: string) {
			const r = await api.post('/api/auth/login/', { username, password })
			this.access = r.data.access
			this.refresh = r.data.refresh
			localStorage.setItem('access', this.access)
			localStorage.setItem('refresh', this.refresh)
			api.defaults.headers.common['Authorization'] = `Bearer ${this.access}`
		},
		initInterceptors() {
			api.interceptors.response.use(
				(res) => res,
				async (error) => {
					const original = error.config
					if (error.response && error.response.status === 401 && !original._retry) {
						original._retry = true
						if (!this.refresh) {
							this.logout()
							return Promise.reject(error)
						}
						if (isRefreshing) {
							return new Promise((resolve) => {
								subscribeTokenRefresh((token: string) => {
									original.headers['Authorization'] = `Bearer ${token}`
									resolve(api(original))
								})
							})
						}
						isRefreshing = true
						try {
							const rr = await api.post('/api/auth/refresh/', { refresh: this.refresh })
							this.access = rr.data.access
							localStorage.setItem('access', this.access)
							api.defaults.headers.common['Authorization'] = `Bearer ${this.access}`
							onRefreshed(this.access)
							original.headers['Authorization'] = `Bearer ${this.access}`
							return api(original)
						} catch (e) {
							this.logout()
							return Promise.reject(e)
						} finally {
							isRefreshing = false
						}
					}
					return Promise.reject(error)
				}
			)
		},
		logout() {
			this.access = ''
			this.refresh = ''
			this.user = null
			localStorage.removeItem('access')
			localStorage.removeItem('refresh')
			delete api.defaults.headers.common['Authorization']
		}
	}
})

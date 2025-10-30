import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({
	baseURL: API_BASE,
})

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

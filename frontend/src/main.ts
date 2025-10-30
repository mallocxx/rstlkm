import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './styles.css'
import { useAuthStore } from './stores/auth'

const app = createApp(App)
app.use(createPinia())
app.use(router)
// initialize auth interceptors once Pinia is ready
const auth = useAuthStore()
auth.initInterceptors()
app.mount('#app')

<template>
	<div class="max-w-sm mx-auto mt-16">
		<h1 class="text-xl font-semibold mb-4">Вход</h1>
		<form class="space-y-3" @submit.prevent="submit">
			<input v-model="username" class="w-full px-3 py-2 bg-slate-800 rounded" placeholder="Логин" />
			<input v-model="password" type="password" class="w-full px-3 py-2 bg-slate-800 rounded" placeholder="Пароль" />
			<button class="w-full bg-sky-600 hover:bg-sky-500 px-3 py-2 rounded">Войти</button>
		</form>
		<p v-if="error" class="text-red-400 mt-2">{{ error }}</p>
	</div>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')

async function submit() {
	try {
		await auth.login(username.value, password.value)
		const redirect = (route.query.redirect as string) || '/'
		router.replace(redirect)
	} catch (e) {
		error.value = 'Неверные учетные данные'
	}
}
</script>

<template>
	<div class="max-w-sm mx-auto mt-20">
		<div class="card">
			<h1 class="page-title">Вход</h1>
			<form class="space-y-3" @submit.prevent="submit">
				<input v-model="username" class="input" placeholder="Логин" />
				<input v-model="password" type="password" class="input" placeholder="Пароль" />
				<button class="btn-primary w-full">Войти</button>
			</form>
			<p v-if="error" class="text-red-400 mt-3">{{ error }}</p>
		</div>
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

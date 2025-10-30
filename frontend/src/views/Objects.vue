<template>
	<div>
		<h1 class="text-xl font-semibold mb-4">Объекты</h1>
		<div class="space-y-2 max-w-xl">
			<div class="flex gap-2">
				<input v-model="query" placeholder="Поиск адреса" class="flex-1 px-3 py-2 bg-slate-800 rounded" />
				<button @click="load" class="bg-sky-600 hover:bg-sky-500 px-3 py-2 rounded">Найти</button>
			</div>
			<ul class="divide-y divide-slate-800">
				<li v-for="b in buildings" :key="b.id" class="py-2">{{ b.address }} ({{ b.city.name }})</li>
			</ul>
		</div>
	</div>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, useAuthStore } from '../stores/auth'

const auth = useAuthStore()
if (auth.access) {
	api.defaults.headers.common['Authorization'] = `Bearer ${auth.access}`
}

const buildings = ref<any[]>([])
const query = ref('')

async function load() {
	const r = await api.get('/api/buildings/', { params: query.value ? { search: query.value } : {} })
	buildings.value = r.data.results || r.data
}

onMounted(load)
</script>

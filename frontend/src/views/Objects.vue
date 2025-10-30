<template>
	<div class="space-y-4">
		<h1 class="page-title">Объекты</h1>

		<!-- Filters -->
		<div class="card">
			<div class="flex flex-col sm:flex-row flex-wrap gap-3 items-stretch sm:items-end">
				<div>
					<label class="text-xs">Город</label>
					<select v-model="cityId" class="select min-w-[180px] sm:min-w-[200px]">
						<option value="">— выбрать —</option>
						<option v-for="c in cities" :key="c.id" :value="c.id">{{ c.name }}</option>
					</select>
				</div>
				<div>
					<label class="text-xs">Поиск по адресу</label>
					<input v-model="query" class="input min-w-[200px] sm:min-w-[240px]" placeholder="ул. Ленина" />
				</div>
				<button @click="loadBuildings" class="btn-primary w-full sm:w-auto">Найти</button>
			</div>
		</div>

		<div class="grid gap-4 sm:gap-6 md:grid-cols-2">
			<!-- List -->
			<div class="card">
				<h2 class="card-title">Дома</h2>
				<ul class="divide-y divide-slate-800 max-h-[420px] overflow-auto">
					<li v-for="b in buildings" :key="b.id" class="py-2 flex items-center justify-between gap-3">
						<span class="cursor-pointer hover:underline" @click="selectBuilding(b)">{{ b.address }}</span>
						<span class="text-xs opacity-70">{{ b.city.name }}</span>
					</li>
				</ul>
			</div>

			<!-- Map -->
			<div class="card">
				<h2 class="card-title">Карта</h2>
				<div ref="mapEl" class="h-64 md:h-[420px] rounded overflow-hidden"></div>
			</div>
		</div>

		<!-- Apartment details and comments -->
		<div class="grid gap-4 sm:gap-6 md:grid-cols-2">
			<div class="card space-y-2">
				<h2 class="card-title">Квартиры выбранного дома</h2>
				<div class="flex flex-col sm:flex-row gap-2">
					<select v-model="apartmentId" class="select min-w-[200px]">
						<option value="">— выбрать квартиру —</option>
						<option v-for="a in apartments" :key="a.id" :value="a.id">Кв. {{ a.number }}</option>
					</select>
					<button @click="loadComments" :disabled="!apartmentId" class="btn-secondary w-full sm:w-auto">Показать комментарии</button>
				</div>
			</div>
			<div class="card">
				<h2 class="card-title">Комментарии</h2>
				<ul class="divide-y divide-slate-800 max-h-[300px] overflow-auto">
					<li v-for="v in comments" :key="v.id" class="py-2 text-sm">
						<span class="opacity-70">{{ new Date(v.visited_at).toLocaleString() }}:</span>
						<span class="ml-2">{{ v.note }}<template v-if="v.survey && v.survey.comment"> — {{ v.survey.comment }}</template></span>
					</li>
				</ul>
			</div>
		</div>
	</div>
</template>
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { api } from '../stores/auth'

const cities = ref<any[]>([])
const cityId = ref<any>('')
const buildings = ref<any[]>([])
const apartments = ref<any[]>([])
const apartmentId = ref<any>('')
const comments = ref<any[]>([])
const query = ref('')

const mapEl = ref<HTMLDivElement | null>(null)
let map: any = null
let markers: any[] = []

function initMap() {
	if (!mapEl.value) return
	map = (window as any).L.map(mapEl.value).setView([42.9845, 47.5040], 11)
	;(window as any).L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution: '&copy; OpenStreetMap contributors'
	}).addTo(map)
}
function clearMarkers() {
	markers.forEach(m => m.remove())
	markers = []
}
function drawMarkers() {
	if (!map) return
	clearMarkers()
	const L = (window as any).L
	const pts: [number, number][] = []
	for (const b of buildings.value) {
		if (b.latitude && b.longitude) {
			const m = L.marker([b.latitude, b.longitude]).addTo(map).bindPopup(`${b.address} (${b.city.name})`)
			markers.push(m)
			pts.push([b.latitude, b.longitude])
		}
	}
	if (pts.length) {
		const group = L.featureGroup(markers)
		map.fitBounds(group.getBounds().pad(0.2))
	}
}

async function loadCities() {
	const r = await api.get('/api/cities/')
	cities.value = r.data.results || r.data
	if (!cityId.value && cities.value.length) cityId.value = cities.value[0].id
}
async function loadBuildings() {
	const params: any = {}
	if (cityId.value) params.city = cityId.value
	if (query.value) params.search = query.value
	const r = await api.get('/api/buildings/', { params })
	buildings.value = r.data.results || r.data
	drawMarkers()
}
async function selectBuilding(b: any) {
	// Load apartments
	const r = await api.get('/api/apartments/', { params: { building: b.id } })
	apartments.value = r.data.results || r.data
	apartmentId.value = ''
	comments.value = []
}
async function loadComments() {
	if (!apartmentId.value) return
	const r = await api.get('/api/visits/', { params: { apartment: apartmentId.value } })
	comments.value = r.data.results || r.data
}

onMounted(async () => {
	initMap()
	await loadCities()
	await loadBuildings()
})
watch(cityId, loadBuildings)
</script>

<template>
	<div class="space-y-6">
		<h1 class="page-title">Анкета (инженер)</h1>
		<div class="grid md:grid-cols-2 gap-6">
			<section class="card space-y-3">
				<h2 class="card-title">Объект</h2>
				<div class="space-y-2">
					<label class="block text-sm opacity-80">Город</label>
					<select v-model="cityId" class="select">
						<option v-for="c in cities" :key="c.id" :value="c.id">{{ c.name }}</option>
					</select>
				</div>
				<div class="space-y-2">
					<label class="block text-sm opacity-80">Дом</label>
					<select v-model="buildingId" class="select">
						<option value="">— выбрать —</option>
						<option v-for="b in buildings" :key="b.id" :value="b.id">{{ b.address }}</option>
					</select>
					<div class="flex gap-2">
						<input v-model="newAddress" placeholder="Новый адрес" class="input flex-1" />
						<button @click="addBuilding" class="btn-success">Добавить дом</button>
					</div>
					<p class="text-xs opacity-70">GPS: {{ gpsText }}</p>
				</div>
				<div class="space-y-2">
					<label class="block text-sm opacity-80">Квартира</label>
					<input v-model="apartmentNumber" placeholder="Например, 12" class="input" />
				</div>
				<div class="flex gap-2">
					<button @click="saveVisit" class="btn-primary">Сохранить визит</button>
					<button @click="loadLatestSurvey" :disabled="!apartmentId" class="btn-secondary">Загрузить последнюю анкету</button>
				</div>
			</section>

			<section class="card space-y-3">
				<h2 class="card-title">Анкета</h2>
				<input v-model="clientProfile" placeholder="Портрет клиента" class="input" />
				<div class="space-y-2">
					<label class="block text-sm opacity-80">Чем пользуется</label>
					<div class="flex flex-wrap gap-2 text-sm">
						<label v-for="s in serviceOptions" :key="s" class="inline-flex items-center gap-2">
							<input type="checkbox" :value="s" v-model="servicesCurrent" /> <span>{{ s }}</span>
						</label>
					</div>
				</div>
				<div class="space-y-2">
					<label class="block text-sm opacity-80">Удовлетворенность провайдером</label>
					<select v-model="providerSatisfaction" class="select">
						<option value="">—</option>
						<option v-for="o in satisfactionOptions" :key="o" :value="o">{{ o }}</option>
					</select>
				</div>
				<div class="space-y-2">
					<label class="block text-sm opacity-80">Интерес к услугам</label>
					<div class="flex flex-wrap gap-2 text-sm">
						<label v-for="s in serviceOptions" :key="s" class="inline-flex items-center gap-2">
							<input type="checkbox" :value="s" v-model="interestedServices" /> <span>{{ s }}</span>
						</label>
					</div>
				</div>
				<input v-model="bestCallTime" placeholder="Удобное время для связи" class="input" />
				<input v-model="contactPhone" placeholder="Контактный телефон" class="input" />
				<input v-model.number="fairPrice" type="number" placeholder="Справедливая цена" class="input" />
				<textarea v-model="comment" placeholder="Примечание" class="input"></textarea>
				<button @click="saveSurvey" :disabled="!visitId" class="btn-success disabled:bg-slate-700">Сохранить анкету</button>
			</section>
		</div>

		<section v-if="apartmentId" class="card space-y-2">
			<h2 class="card-title">Комментарии по квартире</h2>
			<ul class="divide-y divide-slate-800">
				<li v-for="v in comments" :key="v.id" class="py-2 text-sm">
					<span class="opacity-70">{{ new Date(v.visited_at).toLocaleString() }}:</span>
					<span class="ml-2">{{ v.note }}<template v-if="v.survey && v.survey.comment"> — {{ v.survey.comment }}</template></span>
				</li>
			</ul>
		</section>
	</div>
</template>
<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { api } from '../stores/auth'

const cities = ref<any[]>([])
const cityId = ref<number | ''>('')
const buildings = ref<any[]>([])
const buildingId = ref<number | ''>('')
const newAddress = ref('')

const apartmentNumber = ref('')
const apartmentId = ref<number | null>(null)

const latitude = ref<number | null>(null)
const longitude = ref<number | null>(null)
const gpsText = ref('получаю...')

const clientProfile = ref('')
const servicesCurrent = ref<string[]>([])
const providerSatisfaction = ref('')
const interestedServices = ref<string[]>([])
const bestCallTime = ref('')
const contactPhone = ref('')
const fairPrice = ref<number | null>(null)
const comment = ref('')

const serviceOptions = ['INTERNET','TV','CCTV','NANNY']
const satisfactionOptions = ['1','2','3','4','5','SAT','UNSAT']

const visitId = ref<number | null>(null)
const comments = ref<any[]>([])

function getGPS() {
	navigator.geolocation.getCurrentPosition((pos) => {
		latitude.value = pos.coords.latitude
		longitude.value = pos.coords.longitude
		gpsText.value = `${latitude.value?.toFixed(5)}, ${longitude.value?.toFixed(5)}`
	}, () => {
		gpsText.value = 'GPS недоступен'
	})
}

async function loadCities() {
	const r = await api.get('/api/cities/')
	cities.value = r.data.results || r.data
	if (!cityId.value && cities.value.length) cityId.value = cities.value[0].id
}

async function loadBuildings() {
	if (!cityId.value) { buildings.value = []; return }
	const r = await api.get('/api/buildings/', { params: { city: cityId.value } })
	buildings.value = r.data.results || r.data
}

async function addBuilding() {
	if (!cityId.value || !newAddress.value) return
	const payload = { city_id: cityId.value, address: newAddress.value, latitude: latitude.value, longitude: longitude.value }
	try {
		const r = await api.post('/api/buildings/', payload)
		buildings.value.unshift(r.data)
		buildingId.value = r.data.id
		newAddress.value = ''
	} catch (e) {
		queueOffline('/api/buildings/', payload)
	}
}

async function ensureApartment(): Promise<number | null> {
	if (!buildingId.value || !apartmentNumber.value) return null
	try {
		const r = await api.post('/api/apartments/', { building: buildingId.value, number: apartmentNumber.value })
		return r.data.id
	} catch (e) {
		const list = await api.get('/api/apartments/', { params: { building: buildingId.value, search: apartmentNumber.value } })
		const found = (list.data.results || list.data).find((a: any) => a.number === apartmentNumber.value)
		return found?.id || null
	}
}

async function saveVisit() {
	const apt = await ensureApartment()
	if (!apt) return
	apartmentId.value = apt
	const payload = { apartment: apt, latitude: latitude.value, longitude: longitude.value, location_source: 'gps', note: comment.value }
	try {
		const r = await api.post('/api/visits/', payload)
		visitId.value = r.data.id
		await loadComments()
	} catch (e) {
		queueOffline('/api/visits/', payload)
	}
}

async function loadLatestSurvey() {
	if (!apartmentId.value) return
	const r = await api.get('/api/visits/', { params: { apartment: apartmentId.value } })
	const items = r.data.results || r.data
	if (!items.length) return
	const last = items[0]
	visitId.value = last.id
	if (last.survey) {
		const s = last.survey
		clientProfile.value = s.client_profile || ''
		servicesCurrent.value = s.services_current || []
		providerSatisfaction.value = s.provider_satisfaction || ''
		interestedServices.value = s.interested_services || []
		bestCallTime.value = s.best_call_time || ''
		contactPhone.value = s.contact_phone || ''
		fairPrice.value = s.fair_price || null
		comment.value = s.comment || ''
	}
}

async function saveSurvey() {
	if (!visitId.value) return
	const payload = {
		visit: visitId.value,
		client_profile: clientProfile.value,
		services_current: servicesCurrent.value,
		provider_satisfaction: providerSatisfaction.value,
		interested_services: interestedServices.value,
		best_call_time: bestCallTime.value,
		contact_phone: contactPhone.value,
		fair_price: fairPrice.value,
		comment: comment.value,
	}
	try {
		// Try PATCH existing survey
		const vis = await api.get(`/api/visits/`, { params: { id: visitId.value } })
		const found = (vis.data.results || vis.data).find((v:any)=> v.id === visitId.value)
		if (found && found.survey) {
			await api.patch(`/api/surveys/${found.survey.id}/`, payload)
		} else {
			await api.post('/api/surveys/', payload)
		}
		await loadComments()
	} catch (e) {
		queueOffline('/api/surveys/', payload)
	}
}

async function loadComments() {
	if (!apartmentId.value) return
	const r = await api.get('/api/visits/', { params: { apartment: apartmentId.value } })
	const items = r.data.results || r.data
	comments.value = items
}

function queueOffline(url: string, payload: any) {
	const key = 'offlineQueue'
	const q = JSON.parse(localStorage.getItem(key) || '[]')
	q.push({ url, payload, ts: Date.now() })
	localStorage.setItem(key, JSON.stringify(q))
}

async function flushQueue() {
	const key = 'offlineQueue'
	const q = JSON.parse(localStorage.getItem(key) || '[]')
	const remain: any[] = []
	for (const item of q) {
		try { await api.post(item.url, item.payload) } catch { remain.push(item) }
	}
	localStorage.setItem(key, JSON.stringify(remain))
}

onMounted(async () => {
	getGPS()
	await loadCities()
	await loadBuildings()
	await flushQueue()
})

watch(cityId, loadBuildings)
</script>

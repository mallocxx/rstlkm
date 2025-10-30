<template>
<div>
  <h1 class="text-xl font-semibold mb-4">Отчеты (XLSX)</h1>
  <form class="flex flex-wrap gap-2 items-end mb-5" @submit.prevent="generateReport">
    <div>
      <label class="text-xs">Город</label>
      <select v-model="city" class="bg-slate-800 px-2 py-1 rounded">
        <option value="">— любой —</option>
        <option v-for="c in cities" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>
    </div>
    <div>
      <label class="text-xs">Дом</label>
      <select v-model="building" class="bg-slate-800 px-2 py-1 rounded">
        <option value="">— любой —</option>
        <option v-for="b in buildings" :key="b.id" :value="b.id">{{ b.address }}</option>
      </select>
    </div>
    <div>
      <label class="text-xs">Удовлетворенность</label>
      <select v-model="providerSatisfaction" class="bg-slate-800 px-2 py-1 rounded">
        <option value="">— любой —</option>
        <option v-for="s in satisfactionOptions" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>
    <div>
      <label class="text-xs">Интерес</label>
      <select v-model="interestedService" class="bg-slate-800 px-2 py-1 rounded">
        <option value="">— любой —</option>
        <option v-for="s in serviceOptions" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>
    <div>
      <label class="text-xs">Дата с</label>
      <input type="date" v-model="dateFrom" class="bg-slate-800 px-2 py-1 rounded" />
    </div>
    <div>
      <label class="text-xs">Дата по</label>
      <input type="date" v-model="dateTo" class="bg-slate-800 px-2 py-1 rounded" />
    </div>
    <button class="bg-emerald-600 px-4 py-2 rounded ml-2">Создать отчет</button>
  </form>

  <div v-if="reports.length" class="mb-8">
    <h2 class="font-semibold mb-2 text-lg">Последние отчеты</h2>
    <ul class="space-y-2">
      <li v-for="r in reports" :key="r.id" class="px-2 py-2 bg-slate-800 rounded flex gap-2 items-center">
        <span class="opacity-70 text-sm">{{ new Date(r.created_at).toLocaleString() }}</span>
        <a v-if="r.file_path" class="text-sky-400 hover:underline" :href="'/static/' + r.file_path" download>скачать XLSX</a>
        <span>фильтры: {{ JSON.stringify(r.filters, null, 1) }}</span>
      </li>
    </ul>
  </div>
</div>
</template>
<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { api } from '../stores/auth'

const cities = ref<any[]>([]), city = ref('')
const buildings = ref<any[]>([]), building = ref('')
const providerSatisfaction = ref('')
const interestedService = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const reports = ref<any[]>([])

const satisfactionOptions = ['1','2','3','4','5','SAT','UNSAT']
const serviceOptions = ['INTERNET','TV','CCTV','NANNY']

async function loadCities() {
  const r = await api.get('/api/cities/')
  cities.value = r.data.results || r.data
}
async function loadBuildings() {
  if (!city.value) { buildings.value=[]; return }
  const r = await api.get('/api/buildings/', { params: { city: city.value } })
  buildings.value = r.data.results || r.data
}
async function loadReports() {
  const r = await api.get('/api/reports/')
  reports.value = r.data.results || r.data
}

watch(city, loadBuildings)

async function generateReport() {
  const filters: Record<string, any> = {}
  if (city.value) filters.city = city.value
  if (building.value) filters.building = building.value
  if (providerSatisfaction.value) filters.provider_satisfaction = providerSatisfaction.value
  if (interestedService.value) filters.interested_service = interestedService.value
  if (dateFrom.value) filters.date_from = dateFrom.value
  if (dateTo.value) filters.date_to = dateTo.value
  await api.post('/api/reports/generate/', { filters })
  setTimeout(loadReports, 1000)
}

onMounted(() => { loadCities(); loadReports(); })
</script>

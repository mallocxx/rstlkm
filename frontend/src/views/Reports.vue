<template>
<div>
  <h1 class="page-title">Отчеты</h1>
  <div class="card mb-5">
    <form class="flex flex-col sm:flex-row flex-wrap gap-3 items-stretch sm:items-end" @submit.prevent="generateReport">
      <div>
        <label class="text-xs">Город</label>
        <select v-model="city" class="select min-w-[160px] sm:min-w-[180px]">
          <option value="">— не указан —</option>
          <option v-for="c in cities" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>
      <div>
        <label class="text-xs">Дом</label>
        <select v-model="building" class="select min-w-[180px] sm:min-w-[220px]">
          <option value="">— не указан —</option>
          <option v-for="b in buildings" :key="b.id" :value="b.id">{{ b.address }}</option>
        </select>
      </div>
      <div>
        <label class="text-xs">Удовлетворенность</label>
        <select v-model="providerSatisfaction" class="select min-w-[140px] sm:min-w-[160px]">
          <option value="">— не указан —</option>
          <option v-for="s in satisfactionOptions" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
      <div>
        <label class="text-xs">Интерес</label>
        <select v-model="interestedService" class="select min-w-[140px] sm:min-w-[160px]">
          <option value="">— не указан —</option>
          <option v-for="s in serviceOptions" :key="s" :value="s">{{ s }}</option>
        </select>
      </div>
      <div>
        <label class="text-xs">Дата с</label>
        <input type="date" v-model="dateFrom" class="input" />
      </div>
      <div>
        <label class="text-xs">Дата по</label>
        <input type="date" v-model="dateTo" class="input" />
      </div>
      <button class="btn-success ml-0 sm:ml-auto w-full sm:w-auto">Создать отчет</button>
    </form>
  </div>

  <div v-if="notice" class="mb-3 text-sm text-emerald-400">{{ notice }}</div>

  <div v-if="reports.length" class="mb-8">
    <h2 class="card-title">Последние отчеты</h2>
    <ul class="space-y-2">
      <li v-for="r in reports" :key="r.id" class="card flex flex-col sm:flex-row gap-2 sm:gap-3 sm:items-center">
        <span class="opacity-70 text-sm">{{ new Date(r.created_at).toLocaleString() }}</span>
        <a v-if="r.file_path" class="text-sky-400 hover:underline" :href="'/static/' + r.file_path" download>скачать XLSX</a>
        <span class="text-xs opacity-80 break-all">фильтры: {{ JSON.stringify(r.filters, null, 1) }}</span>
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
const notice = ref('')

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

watch(city, () => { building.value=''; loadBuildings() })

async function generateReport() {
  const filters: Record<string, any> = {}
  if (city.value) filters.city = city.value
  if (building.value) filters.building = building.value
  if (providerSatisfaction.value) filters.provider_satisfaction = providerSatisfaction.value
  if (interestedService.value) filters.interested_service = interestedService.value
  if (dateFrom.value) filters.date_from = dateFrom.value
  if (dateTo.value) filters.date_to = dateTo.value
  const r = await api.post('/api/reports/generate/', { filters })
  notice.value = 'Отчет готов — скачивание началось.'
  if (r.data?.file) window.location.href = r.data.file
  setTimeout(() => { notice.value=''; }, 3000)
  setTimeout(loadReports, 800)
}

onMounted(() => { loadCities(); loadReports(); })
</script>

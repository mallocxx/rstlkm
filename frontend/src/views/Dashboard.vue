<template>
<div>
  <h1 class="page-title">Статистика</h1>
  <div class="card mb-4">
    <form class="flex flex-col sm:flex-row gap-3 sm:gap-4 items-stretch sm:items-end" @submit.prevent>
      <div>
        <label class="text-xs">Город:</label>
        <select v-model="city" class="select min-w-[180px] sm:min-w-[200px]">
          <option value="">Все</option>
          <option v-for="(c,i) in cities" :key="c?.id ?? i" :value="c?.id ?? ''">{{ c?.name || '—' }}</option>
        </select>
      </div>
    </form>
    </div>
  </div>
  <div v-if="stats && !loading && !error" class="text-sm text-gray-600 mb-2">Всего записей: {{ stats.total }}</div>
  <div v-if="loading" class="text-sm text-gray-500">Загрузка данных…</div>
  <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>
  <div v-else-if="stats">
    <div class="grid gap-3 sm:gap-4 md:grid-cols-3 mb-4">
      <div class="card"><div class="card-title mb-1">Всего анкет</div><div class="text-2xl font-semibold">{{ stats.total }}</div></div>
      <div class="card"><div class="card-title mb-1">Групп по оценке</div><div class="text-sm text-gray-600">{{ Object.keys(stats.by_satisfaction || {}).length }}</div></div>
      <div class="card"><div class="card-title mb-1">Интересов</div><div class="text-sm text-gray-600">{{ Object.keys(stats.by_interest || {}).length }}</div></div>
    </div>
    <div class="grid gap-4 sm:gap-6 md:grid-cols-2">
    <div class="card">
      <h2 class="card-title">Уровень удовлетворённости</h2>
      <div class="w-full overflow-x-auto" v-if="hasSatisfaction">
        <canvas ref="satChart" class="w-full h-64 md:h-80"></canvas>
      </div>
      <p v-else class="text-sm text-gray-500">Нет данных для отображения.</p>
    </div>
    <div class="card">
      <h2 class="card-title">Доля интересов к услугам</h2>
      <div class="w-full overflow-x-auto" v-if="hasInterest">
        <canvas ref="intChart" class="w-full h-64 md:h-80"></canvas>
      </div>
      <p v-else class="text-sm text-gray-500">Нет данных для отображения.</p>
    </div>
    <div class="card md:col-span-2">
      <h2 class="card-title">Динамика визитов по дням</h2>
      <div class="w-full overflow-x-auto" v-if="hasDynamics">
        <canvas ref="dynChart" class="w-full h-64 md:h-80"></canvas>
      </div>
      <p v-else class="text-sm text-gray-500">Нет данных для отображения.</p>
    </div>
    </div>
</div>
</template>
<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { api } from '../stores/auth'
import Chart from 'chart.js/auto'

const cities = ref<any[]>([]), city = ref('')
const stats = ref<any>(null)
const satChart = ref(), intChart = ref(), dynChart = ref()
let satChartInstance: any, intChartInstance: any, dynChartInstance: any
const loading = ref(false)
const error = ref('')

const hasSatisfaction = computed(() => !!stats.value && Object.values(stats.value.by_satisfaction || {}).some((v: any) => Number(v) > 0))
const hasInterest = computed(() => !!stats.value && Object.values(stats.value.by_interest || {}).some((v: any) => Number(v) > 0))
const hasDynamics = computed(() => !!stats.value && Array.isArray(stats.value.by_day) && stats.value.by_day.length > 0)

async function loadCities() {
  const r = await api.get('/api/cities/')
  const raw = r.data?.results ?? r.data ?? []
  cities.value = (Array.isArray(raw) ? raw : []).filter(Boolean).map((c:any)=> ({ id: c.id, name: c.name }))
}

async function loadStats() {
  loading.value = true
  error.value = ''
  try {
    const params: any = {}
    if (city.value) params.city = city.value
    const r = await api.get('/api/reports/stats_summary/', { params })
    stats.value = {
      total: r.data?.total || 0,
      by_satisfaction: r.data?.by_satisfaction || {},
      by_interest: r.data?.by_interest || {},
      by_day: Array.isArray(r.data?.by_day) ? r.data.by_day : [],
    }
    await nextTick()
    drawCharts()
  } catch (e: any) {
    const msg = e?.response?.data?.detail || e?.response?.data?.message || e?.message
    error.value = `Не удалось загрузить статистику${msg ? `: ${msg}` : ''}`
    stats.value = null
  } finally {
    loading.value = false
  }
}
function destroyCharts() {
  if (satChartInstance) satChartInstance.destroy()
  if (intChartInstance) intChartInstance.destroy()
  if (dynChartInstance) dynChartInstance.destroy()
}
function drawCharts() {
  destroyCharts()
  if (stats.value) {
    const basePlugins = {
      legend: { position: 'bottom' as const },
      tooltip: { enabled: true },
      title: { display: false, text: '' },
    }

    if (hasSatisfaction.value) {
      satChartInstance = new Chart(satChart.value, {
        type: 'doughnut',
        data: {
          labels: Object.keys(stats.value.by_satisfaction),
          datasets: [{
            data: Object.values(stats.value.by_satisfaction) as number[],
            backgroundColor: ['#38bdf8','#34d399','#eab308','#f87171','#a78bfa','#fbbf24','#f472b6'],
            borderWidth: 1,
          }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: basePlugins }
      })
    }

    if (hasInterest.value) {
      const entries = Object.entries(stats.value.by_interest as Record<string, number>)
        .sort((a,b)=> b[1]-a[1]).slice(0, 10)
      intChartInstance = new Chart(intChart.value, {
        type: 'bar',
        data: {
          labels: entries.map(e=> e[0]),
          datasets: [{
            data: entries.map(e=> e[1]),
            label: 'Интерес',
            backgroundColor: '#a78bfa',
            borderRadius: 6,
          }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: basePlugins, scales: { y: { beginAtZero: true } } }
      })
    }

    if (hasDynamics.value) {
      dynChartInstance = new Chart(dynChart.value, {
        type: 'line',
        data: {
          labels: stats.value.by_day.map((p:any)=>p[0]),
          datasets: [{
            data: stats.value.by_day.map((p:any)=>p[1]),
            label: 'Визиты',
            borderColor: '#38bdf8',
            backgroundColor: '#38bdf888',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
          }]
        },
        options: { responsive: true, maintainAspectRatio: false, plugins: basePlugins, scales: { y: { beginAtZero: true } } }
      })
    }
  }
}

watch(city, loadStats)
onMounted(() => { loadCities(); loadStats() })
onUnmounted(() => destroyCharts())
</script>

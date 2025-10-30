<template>
<div>
  <h1 class="page-title">Статистика</h1>
  <div class="card mb-4">
    <form class="flex flex-col sm:flex-row gap-3 sm:gap-4 items-stretch sm:items-end" @submit.prevent>
      <div>
        <label class="text-xs">Город:</label>
        <select v-model="city" class="select min-w-[180px] sm:min-w-[200px]">
          <option value="">Все</option>
          <option v-for="c in cities" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>
    </form>
  </div>
  <div v-if="stats" class="grid gap-4 sm:gap-6 md:grid-cols-2">
    <div class="card">
      <h2 class="card-title">Уровень удовлетворённости</h2>
      <div class="w-full overflow-x-auto">
        <canvas ref="satChart" class="w-full h-64 md:h-80"></canvas>
      </div>
    </div>
    <div class="card">
      <h2 class="card-title">Доля интересов к услугам</h2>
      <div class="w-full overflow-x-auto">
        <canvas ref="intChart" class="w-full h-64 md:h-80"></canvas>
      </div>
    </div>
    <div class="card md:col-span-2">
      <h2 class="card-title">Динамика визитов по дням</h2>
      <div class="w-full overflow-x-auto">
        <canvas ref="dynChart" class="w-full h-64 md:h-80"></canvas>
      </div>
    </div>
  </div>
</div>
</template>
<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'
import { api } from '../stores/auth'
import Chart from 'chart.js/auto'

const cities = ref<any[]>([]), city = ref('')
const stats = ref<any>(null)
const satChart = ref(), intChart = ref(), dynChart = ref()
let satChartInstance: any, intChartInstance: any, dynChartInstance: any

async function loadCities() {
  const r = await api.get('/api/cities/')
  cities.value = r.data.results || r.data
}

async function loadStats() {
  const params: any = {}
  if (city.value) params.city = city.value
  const r = await api.get('/api/reports/stats_summary/', { params })
  stats.value = r.data
  await nextTick()
  drawCharts()
}
function destroyCharts() {
  if (satChartInstance) satChartInstance.destroy()
  if (intChartInstance) intChartInstance.destroy()
  if (dynChartInstance) dynChartInstance.destroy()
}
function drawCharts() {
  destroyCharts()
  if (stats.value) {
    satChartInstance = new Chart(satChart.value, {
      type: 'pie',
      data: {
        labels: Object.keys(stats.value.by_satisfaction),
        datasets: [{
          data: Object.values(stats.value.by_satisfaction),
          backgroundColor: ['#38bdf8','#34d399','#eab308','#f87171','#a78bfa','#818cf8','#fbbf24'],
        }]
      }
    })
    intChartInstance = new Chart(intChart.value, {
      type: 'pie',
      data: {
        labels: Object.keys(stats.value.by_interest),
        datasets: [{
          data: Object.values(stats.value.by_interest),
          backgroundColor: ['#f87171','#38bdf8','#34d399','#a78bfa','#fbbf24','#f472b6'],
        }]
      }
    })
    dynChartInstance = new Chart(dynChart.value, {
      type: 'line',
      data: {
        labels: stats.value.by_day.map((p:any)=>p[0]),
        datasets: [{
          data: stats.value.by_day.map((p:any)=>p[1]),
          label: 'Визиты',
          borderColor: '#38bdf8',
          backgroundColor: '#38bdf888',
          fill: true,
        }]
      }
    })
  }
}

watch(city, loadStats)
onMounted(() => { loadCities(); loadStats() })
</script>

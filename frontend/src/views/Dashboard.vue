<template>
<div class="max-w-6xl mx-auto">
  <h1 class="text-xl font-semibold mb-4">Статистика</h1>
  <form class="flex gap-4 mb-4" @submit.prevent>
    <div>
      <label class="text-xs">Город:</label>
      <select v-model="city" class="bg-slate-800 px-2 py-1 rounded">
        <option value="">Все</option>
        <option v-for="c in cities" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>
    </div>
  </form>
  <div v-if="stats">
    <div class="grid md:grid-cols-2 gap-8">
      <div>
        <h2 class="font-semibold mb-2">Уровень удовлетворённости</h2>
        <canvas ref="satChart"></canvas>
      </div>
      <div>
        <h2 class="font-semibold mb-2">Доля интересов к услугам</h2>
        <canvas ref="intChart"></canvas>
      </div>
      <div class="md:col-span-2">
        <h2 class="font-semibold mb-2">Динамика визитов по дням</h2>
        <canvas ref="dynChart"></canvas>
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

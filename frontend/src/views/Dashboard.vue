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
    <div v-if="stats && !loading && !error" class="text-sm text-gray-600 mb-2">Всего записей: {{ stats.total }}</div>
    <div v-if="loading" class="text-sm text-gray-500">Загрузка данных…</div>
    <div v-else-if="error" class="text-sm text-red-600">{{ error }}</div>
    <div v-else-if="stats">
      <div class="grid gap-4 sm:gap-6 md:grid-cols-2">
        <!-- 1. Количество объектов по статусам -->
        <div class="card">
          <h2 class="card-title">Количество объектов по статусам</h2>
          <div class="w-full overflow-x-auto">
            <img :src="objectsImageSrc" alt="Количество объектов по статусам" class="w-full h-auto object-contain" />
          </div>
        </div>

        <!-- 2. Уровень удовлетворённости провайдерами -->
        <div class="card">
          <h2 class="card-title">Уровень удовлетворённости провайдерами</h2>
          <div class="w-full overflow-x-auto">
            <img :src="providersImageSrc" alt="Уровень удовлетворённости провайдерами" class="w-full h-auto object-contain" />
          </div>
        </div>

        <!-- 3. Доля потенциальных клиентов по районам -->
        <div class="card">
          <h2 class="card-title">Доля потенциальных клиентов по районам</h2>
          <div class="w-full overflow-x-auto">
            <img :src="clientsImageSrc" alt="Доля потенциальных клиентов по районам" class="w-full h-auto object-contain" />
          </div>
        </div>

        <!-- 4. Динамика визитов по времени -->
        <div class="card">
          <h2 class="card-title">Динамика визитов по времени</h2>
          <div class="w-full overflow-x-auto">
            <img :src="visitsImageSrc" alt="Динамика визитов по времени" class="w-full h-auto object-contain" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { api } from '../stores/auth'

const cities = ref<any[]>([]), city = ref('')
const stats = ref<any>(null)
const loading = ref(false)
const error = ref('')

// Получаем имя текущего выбранного города
const selectedCityName = computed(() => {
  if (!city.value) return 'all'
  const found = cities.value.find((c: any) => c.id === city.value)
  if (!found) return null
  
  const name = found.name?.toLowerCase() || ''
  if (name.includes('каспийск')) return 'kasp'
  if (name.includes('махачкала') || name.includes('махач')) return 'makh'
  return null
})

// Функция для определения номера изображения на основе ID города (1-6)
const getImageNumber = (cityId: string | null): number => {
  if (!cityId) return 1
  // Используем ID города для выбора номера (1-6)
  const num = parseInt(cityId) % 6
  return num === 0 ? 6 : num
}

// Путь к изображению для графика "Количество объектов по статусам"
const objectsImageSrc = computed(() => {
  const cityPostfix = selectedCityName.value
  // Для objects нет файлов с постфиксами городов (kasp, makh), только all и номера
  if (cityPostfix === 'all') return '/images/objects_all.png'
  const num = getImageNumber(city.value || null)
  // Для objects есть только 2-6, поэтому маппим 1-6 -> 2-6
  const objectsNum = ((num - 1) % 5) + 2
  return `/images/objects${objectsNum}.png`
})

// Путь к изображению для графика "Уровень удовлетворённости провайдерами"
const providersImageSrc = computed(() => {
  const cityPostfix = selectedCityName.value
  // Для providers нет файлов с постфиксами городов, используем только номера
  const num = cityPostfix === 'all' ? 1 : getImageNumber(city.value || null)
  return `/images/providers${num}.png`
})

// Путь к изображению для графика "Доля потенциальных клиентов по районам"
const clientsImageSrc = computed(() => {
  const cityPostfix = selectedCityName.value
  if (cityPostfix === 'kasp') return '/images/clients_kasp.png'
  if (cityPostfix === 'makh') return '/images/clients_makh.png'
  if (cityPostfix === 'all') return '/images/clients_all.png'
  const num = getImageNumber(city.value || null)
  // Для clients есть только 3, 4, 5, поэтому маппим 1-6 -> 3-5
  const clientNum = ((num - 1) % 3) + 3
  return `/images/clients${clientNum}.png`
})

// Путь к изображению для графика "Динамика визитов по времени"
const visitsImageSrc = computed(() => {
  const cityPostfix = selectedCityName.value
  // Для visits нет файлов с постфиксами городов, используем только номера
  const num = cityPostfix === 'all' ? 1 : getImageNumber(city.value || null)
  return `/images/visits${num}.png`
})

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
      by_status: r.data?.by_status || {},
      by_provider_satisfaction: r.data?.by_provider_satisfaction || {},
      by_district: r.data?.by_district || {},
    }
  } catch (e: any) {
    const msg = e?.response?.data?.detail || e?.response?.data?.message || e?.message
    error.value = `Не удалось загрузить статистику${msg ? `: ${msg}` : ''}`
    stats.value = null
  } finally {
    loading.value = false
  }
}

watch(city, loadStats)
onMounted(() => { loadCities(); loadStats() })
</script>
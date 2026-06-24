<template>
  <div class="container mt-4">
    <h1 class="mb-4">Заповедники Крыма</h1>

    <!-- Статистика -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-white bg-primary">
          <div class="card-body">
            <h5 class="card-title">Заповедников</h5>
            <h2>{{ stats.reserves_count }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-success">
          <div class="card-body">
            <h5 class="card-title">Видов животных</h5>
            <h2>{{ stats.animals_count }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-danger">
          <div class="card-body">
            <h5 class="card-title">Краснокнижных</h5>
            <h2>{{ stats.redbook_count }}</h2>
          </div>
        </div>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row">
          <div class="col-md-5">
            <input 
              v-model="searchQuery" 
              type="text" 
              class="form-control" 
              placeholder="🔍 Поиск по названию..."
            >
          </div>
          <div class="col-md-3">
            <select v-model="selectedRegion" class="form-select">
              <option value="">Все регионы</option>
              <option value="Южный берег Крыма">Южный берег Крыма</option>
              <option value="Керченский полуостров">Керченский полуостров</option>
              <option value="Раздольненский район">Раздольненский район</option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="selectedClimate" class="form-select">
              <option value="">Все климаты</option>
              <option value="Умеренно-теплый">Умеренно-теплый</option>
              <option value="Степной">Степной</option>
              <option value="Сухой степной">Сухой степной</option>
              <option value="Умеренный">Умеренный</option>
            </select>
          </div>
          <div class="col-md-1">
            <button @click="exportToCSV" class="btn btn-success w-100">📊 CSV</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Список заповедников -->
    <div v-if="loading" class="alert alert-info">Загрузка...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="filteredReserves.length === 0" class="alert alert-warning">Заповедников не найдено</div>

    <div class="row">
      <div v-for="reserve in filteredReserves" :key="reserve.id" class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100 shadow">
          <img 
            :src="reserve.image_url || 'https://placehold.co/600x400/2c3e50/white?text=' + encodeURIComponent(reserve.name)" 
            class="card-img-top" 
            :alt="reserve.name" 
            style="height: 200px; object-fit: cover;"
            @error="handleImageError($event, reserve)"
          >
          <div class="card-body">
            <h5 class="card-title">{{ reserve.name }}</h5>
            <p class="card-text">
              <strong>📍 Регион:</strong> {{ reserve.region }}<br>
              <strong>🌡 Климат:</strong> {{ reserve.climate }}<br>
              <strong>📏 Площадь:</strong> {{ reserve.area }}<br>
              <strong>📅 Основан:</strong> {{ reserve.established_date || 'н/д' }}
            </p>
            <p class="card-text text-muted small">{{ reserve.description?.substring(0, 100) }}...</p>
            <router-link :to="`/reserves/${reserve.id}`" class="btn btn-primary w-100">Подробнее →</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      reserves: [],
      loading: true,
      error: null,
      searchQuery: '',
      selectedRegion: '',
      selectedClimate: '',
      stats: {
        reserves_count: 0,
        animals_count: 0,
        redbook_count: 0
      }
    }
  },
  computed: {
    filteredReserves() {
      let filtered = this.reserves
      
      if (this.searchQuery) {
        filtered = filtered.filter(r => 
          r.name.toLowerCase().includes(this.searchQuery.toLowerCase())
        )
      }
      if (this.selectedRegion) {
        filtered = filtered.filter(r => r.region === this.selectedRegion)
      }
      if (this.selectedClimate) {
        filtered = filtered.filter(r => r.climate === this.selectedClimate)
      }
      
      return filtered
    }
  },
  async mounted() {
    await this.loadReserves()
    await this.loadStats()
  },
  methods: {
    async loadReserves() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/reserves')
        this.reserves = response.data
        this.loading = false
      } catch (err) {
        this.error = 'Ошибка загрузки заповедников'
        this.loading = false
      }
    },
    async loadStats() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/stats')
        this.stats = response.data
      } catch (err) {
        console.error('Ошибка загрузки статистики', err)
      }
    },
    handleImageError(event, reserve) {
      // Если картинка не загрузилась, ставим заглушку
      event.target.src = `https://placehold.co/600x400/2c3e50/white?text=${encodeURIComponent(reserve.name)}`
    },
    exportToCSV() {
      const headers = ['Название', 'Регион', 'Климат', 'Площадь', 'Описание']
      const rows = this.filteredReserves.map(r => [
        r.name, r.region, r.climate, r.area, r.description
      ])
      
      const csvContent = [headers, ...rows]
        .map(row => row.map(cell => `"${cell || ''}"`).join(','))
        .join('\n')
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.href = url
      link.setAttribute('download', 'заповедники.csv')
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
    }
  }
}
</script>
<template>
  <div class="container mt-4">
    <!-- Информация о входе -->
    <div class="alert alert-success">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          ✅ Вы вошли как <strong>{{ adminLogin }}</strong>
        </div>
        <button @click="logout" class="btn btn-danger btn-sm">🚪 Выйти</button>
      </div>
    </div>

    <h1>Админ-панель</h1>
    
    <!-- Вкладки -->
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <button class="nav-link" :class="{ active: tab === 'reserves' }" @click="tab = 'reserves'">Заповедники</button>
      </li>
      <li class="nav-item">
        <button class="nav-link" :class="{ active: tab === 'animals' }" @click="tab = 'animals'">Животные</button>
      </li>
    </ul>

    <!-- Форма добавления -->
    <div class="card mb-4">
      <div class="card-header">
        <h4>Добавить {{ tab === 'reserves' ? 'заповедник' : 'животное' }}</h4>
      </div>
      <div class="card-body">
        <form @submit.prevent="addItem">
          <div class="row">
            <div class="col-md-6 mb-2">
              <input v-model="newItem.name" type="text" class="form-control" placeholder="Название" required>
            </div>
            <div class="col-md-6 mb-2">
              <input v-model="newItem.description" type="text" class="form-control" placeholder="Описание">
            </div>
            <div v-if="tab === 'reserves'" class="col-md-6 mb-2">
              <input v-model="newItem.region" type="text" class="form-control" placeholder="Регион">
            </div>
            <div v-if="tab === 'reserves'" class="col-md-6 mb-2">
              <input v-model="newItem.climate" type="text" class="form-control" placeholder="Климат">
            </div>
            <div v-if="tab === 'reserves'" class="col-md-6 mb-2">
              <input v-model="newItem.area" type="text" class="form-control" placeholder="Площадь">
            </div>
            <div v-if="tab === 'reserves'" class="col-md-6 mb-2">
              <input v-model="newItem.latitude" type="number" step="any" class="form-control" placeholder="Широта">
            </div>
            <div v-if="tab === 'reserves'" class="col-md-6 mb-2">
              <input v-model="newItem.longitude" type="number" step="any" class="form-control" placeholder="Долгота">
            </div>
            <div v-if="tab === 'reserves'" class="col-md-12 mb-2">
              <input v-model="newItem.image_url" type="url" class="form-control" placeholder="URL фото">
            </div>
            <div v-if="tab === 'animals'" class="col-md-6 mb-2">
              <input v-model="newItem.species" type="text" class="form-control" placeholder="Тип животного">
            </div>
            <div v-if="tab === 'animals'" class="col-md-6 mb-2">
              <select v-model="newItem.rarity" class="form-select">
                <option value="Обычный">Обычный</option>
                <option value="Редкий">Редкий</option>
                <option value="Краснокнижный">Краснокнижный</option>
              </select>
            </div>
            <div v-if="tab === 'animals'" class="col-md-6 mb-2">
              <select v-model="newItem.reserve_id" class="form-select">
                <option :value="null">Выберите заповедник</option>
                <option v-for="r in reserves" :key="r.id" :value="r.id">{{ r.name }}</option>
              </select>
            </div>
            <div class="col-md-12">
              <button type="submit" class="btn btn-primary">➕ Добавить</button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Список с возможностью редактирования/удаления -->
    <h3>Список {{ tab === 'reserves' ? 'заповедников' : 'животных' }}</h3>
    <div v-if="loading">Загрузка...</div>
    <div v-else>
      <div v-for="item in items" :key="item.id" class="card mb-2">
        <div class="card-body">
          <div class="row">
            <div class="col-md-8">
              <h5>{{ item.name }}</h5>
              <p class="small text-muted">{{ item.description }}</p>
            </div>
            <div class="col-md-4 text-end">
              <button @click="deleteItem(item.id)" class="btn btn-danger btn-sm">🗑 Удалить</button>
            </div>
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
      tab: 'reserves',
      reserves: [],
      items: [],
      loading: false,
      newItem: {},
      adminLogin: localStorage.getItem('adminLogin') || 'admin'
    }
  },
  watch: {
    tab() {
      this.loadItems()
      this.newItem = {}
    }
  },
  mounted() {
    // Проверка, что пользователь админ
    if (localStorage.getItem('isAdmin') !== 'true') {
      this.$router.push('/login')
    }
    this.loadReserves()
    this.loadItems()
  },
  methods: {
    async loadReserves() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/reserves')
        this.reserves = response.data
      } catch (err) {
        console.error('Ошибка загрузки заповедников', err)
      }
    },
    async loadItems() {
      this.loading = true
      try {
        const endpoint = this.tab === 'reserves' ? '/reserves' : '/animals'
        const response = await axios.get(`http://127.0.0.1:5000${endpoint}`)
        this.items = response.data
      } catch (err) {
        console.error('Ошибка загрузки', err)
      }
      this.loading = false
    },
    async addItem() {
      try {
        const endpoint = this.tab === 'reserves' ? '/reserves' : '/animals'
        await axios.post(`http://127.0.0.1:5000${endpoint}`, this.newItem)
        this.newItem = {}
        await this.loadItems()
        if (this.tab === 'reserves') await this.loadReserves()
        alert('Добавлено успешно!')
      } catch (err) {
        alert('Ошибка добавления')
        console.error(err)
      }
    },
    async deleteItem(id) {
      if (!confirm('Удалить?')) return
      try {
        const endpoint = this.tab === 'reserves' ? '/reserves' : '/animals'
        await axios.delete(`http://127.0.0.1:5000${endpoint}/${id}`)
        await this.loadItems()
        if (this.tab === 'reserves') await this.loadReserves()
        alert('Удалено успешно!')
      } catch (err) {
        alert('Ошибка удаления')
        console.error(err)
      }
    },
    logout() {
      localStorage.removeItem('isAdmin')
      localStorage.removeItem('adminLogin')
      this.$router.push('/')
    }
  }
}
</script>
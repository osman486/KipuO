<template>
  <div class="container mt-4" v-if="reserve">
    <button @click="$router.back()" class="btn btn-secondary mb-3">← Назад</button>
    
    <div class="row">
      <div class="col-md-6">
        <!-- Основное фото с увеличением -->
        <img 
          :src="reserve.image_url || 'https://placehold.co/600x400/2c3e50/white?text=Заповедник'" 
          class="img-fluid rounded shadow" 
          :alt="reserve.name"
          style="width: 100%; height: 300px; object-fit: cover; cursor: pointer;"
          @click="showFullImage(reserve.image_url)"
          @error="handleMainImageError"
        >
        
        <!-- Маленькая галерея -->
        <div class="row mt-2" v-if="galleryImages.length > 0">
          <div class="col-3" v-for="(img, idx) in galleryImages" :key="idx">
            <img 
              :src="img" 
              class="img-thumbnail" 
              style="height: 70px; width: 100%; object-fit: cover; cursor: pointer;"
              @click="showFullImage(img)"
            >
          </div>
        </div>
      </div>
      <div class="col-md-6">
        <h1>{{ reserve.name }}</h1>
        <p><strong>📍 Регион:</strong> {{ reserve.region }}</p>
        <p><strong>🌡 Климат:</strong> {{ reserve.climate }}</p>
        <p><strong>📏 Площадь:</strong> {{ reserve.area }}</p>
        <p><strong>📅 Год основания:</strong> {{ reserve.established_date || 'н/д' }}</p>
        <p><strong>📝 Описание:</strong></p>
        <p>{{ reserve.description }}</p>
      </div>
    </div>

    <!-- Карта -->
    <div class="card mt-4">
      <div class="card-header">
        <h4>🗺 Карта заповедника</h4>
      </div>
      <div class="card-body">
        <div v-if="reserve.latitude && reserve.longitude" style="height: 400px;">
          <l-map :use-global-web-worker="false" :center="[reserve.latitude, reserve.longitude]" :zoom="10" style="height: 100%;">
            <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"></l-tile-layer>
            <l-marker :lat-lng="[reserve.latitude, reserve.longitude]">
              <l-tooltip>{{ reserve.name }}</l-tooltip>
            </l-marker>
          </l-map>
        </div>
        <div v-else class="alert alert-warning">Координаты не указаны</div>
      </div>
    </div>

    <!-- Животные заповедника -->
    <div class="card mt-4">
      <div class="card-header">
        <h4>🐾 Животные заповедника</h4>
      </div>
      <div class="card-body">
        <div v-if="animalsLoading">Загрузка...</div>
        <div v-else-if="animals.length === 0" class="alert alert-info">Нет данных о животных</div>
        <div class="row">
          <div v-for="animal in animals" :key="animal.id" class="col-md-6 col-lg-4 mb-3">
            <div class="card h-100">
              <img 
                :src="animal.image_url || 'https://placehold.co/400x300/27ae60/white?text=Животное'" 
                class="card-img-top" 
                style="height: 150px; object-fit: cover;"
                @error="e => e.target.src = 'https://placehold.co/400x300/27ae60/white?text=Животное'"
              >
              <div class="card-body">
                <h5 class="card-title">{{ animal.name }}</h5>
                <p><strong>Тип:</strong> {{ animal.species }}</p>
                <p><strong>Статус:</strong> 
                  <span :class="animal.rarity === 'Краснокнижный' ? 'text-danger fw-bold' : ''">
                    {{ animal.rarity }}
                  </span>
                </p>
                <p class="small">{{ animal.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Отзывы -->
    <div class="card mt-4">
      <div class="card-header">
        <h4>💬 Отзывы посетителей</h4>
      </div>
      <div class="card-body">
        <div v-if="reviewsLoading">Загрузка...</div>
        <div v-else>
          <div v-for="review in reviews" :key="review.id" class="border-bottom mb-3 pb-3">
            <div class="d-flex justify-content-between">
              <strong>{{ review.author }}</strong>
              <span>
                <span v-for="s in review.rating" class="text-warning">★</span>
                <span v-for="s in (5-review.rating)" class="text-secondary">★</span>
              </span>
            </div>
            <p class="mt-2">{{ review.comment }}</p>
            <small class="text-muted">{{ new Date(review.created_at).toLocaleDateString() }}</small>
          </div>
        </div>

        <!-- Форма добавления отзыва -->
        <h5 class="mt-4">Оставить отзыв</h5>
        <form @submit.prevent="submitReview">
          <div class="mb-3">
            <input v-model="newReview.author" type="text" class="form-control" placeholder="Ваше имя">
          </div>
          <div class="mb-3">
            <select v-model="newReview.rating" class="form-select" required>
              <option value="5">⭐⭐⭐⭐⭐ Отлично</option>
              <option value="4">⭐⭐⭐⭐ Хорошо</option>
              <option value="3">⭐⭐⭐ Нормально</option>
              <option value="2">⭐⭐ Плохо</option>
              <option value="1">⭐ Ужасно</option>
            </select>
          </div>
          <div class="mb-3">
            <textarea v-model="newReview.comment" class="form-control" rows="3" placeholder="Ваш отзыв..." required></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Отправить отзыв</button>
        </form>
      </div>
    </div>

    <!-- Модальное окно для увеличенного фото -->
    <div v-if="fullImageVisible" class="modal show d-block" tabindex="-1" @click.self="closeFullImage">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ reserve.name }}</h5>
            <button type="button" class="btn-close" @click="closeFullImage"></button>
          </div>
          <div class="modal-body text-center">
            <img :src="fullImageUrl" class="img-fluid" style="max-height: 70vh;">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { LMap, LTileLayer, LMarker, LTooltip } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'

export default {
  components: { LMap, LTileLayer, LMarker, LTooltip },
  data() {
    return {
      reserve: null,
      animals: [],
      reviews: [],
      animalsLoading: true,
      reviewsLoading: true,
      fullImageVisible: false,
      fullImageUrl: '',
      galleryImages: [],
      newReview: {
        author: '',
        rating: 5,
        comment: ''
      }
    }
  },
  async mounted() {
    const reserveId = this.$route.params.id
    await this.loadReserve(reserveId)
    await Promise.all([
      this.loadAnimals(reserveId),
      this.loadReviews(reserveId)
    ])
    this.setupGallery()
  },
  methods: {
    async loadReserve(id) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/reserves/${id}`)
        this.reserve = response.data
      } catch (err) {
        this.$router.push('/reserves')
      }
    },
    async loadAnimals(reserveId) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/animals?reserve_id=${reserveId}`)
        this.animals = response.data
        this.animalsLoading = false
      } catch (err) {
        this.animalsLoading = false
      }
    },
    async loadReviews(reserveId) {
      try {
        const response = await axios.get(`http://127.0.0.1:5000/reviews?reserve_id=${reserveId}`)
        this.reviews = response.data
        this.reviewsLoading = false
      } catch (err) {
        this.reviewsLoading = false
      }
    },
    setupGallery() {
      // Добавляем дополнительные картинки для галереи
      const mainImage = this.reserve.image_url
      if (mainImage && !mainImage.includes('placehold')) {
        this.galleryImages = [mainImage]
      }
      // Можно добавить ещё картинки
      this.galleryImages.push('https://placehold.co/600x400/3498db/white?text=Фото+2')
      this.galleryImages.push('https://placehold.co/600x400/e74c3c/white?text=Фото+3')
    },
    showFullImage(url) {
      this.fullImageUrl = url
      this.fullImageVisible = true
    },
    closeFullImage() {
      this.fullImageVisible = false
      this.fullImageUrl = ''
    },
    handleMainImageError(event) {
      event.target.src = `https://placehold.co/600x400/2c3e50/white?text=${encodeURIComponent(this.reserve.name)}`
    },
    async submitReview() {
      try {
        await axios.post('http://127.0.0.1:5000/reviews', {
          reserve_id: this.reserve.id,
          author: this.newReview.author || 'Аноним',
          rating: parseInt(this.newReview.rating),
          comment: this.newReview.comment
        })
        this.newReview = { author: '', rating: 5, comment: '' }
        await this.loadReviews(this.reserve.id)
      } catch (err) {
        alert('Ошибка при отправке отзыва')
      }
    }
  }
}
</script>

<style scoped>
.modal {
  background-color: rgba(0,0,0,0.7);
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1050;
}
</style>
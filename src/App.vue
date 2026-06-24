<template>
  <div>
    <nav class="navbar navbar-dark bg-dark p-3">
      <div class="container">
        <h3 class="text-white">
          Заповедники Крыма
        </h3>
        <div>
          <router-link
            class="btn btn-outline-light me-2"
            to="/"
          >
            Главная
          </router-link>
          <router-link
            class="btn btn-outline-light me-2"
            to="/reserves"
          >
            Заповедники
          </router-link>
          
          <!-- Показываем разные кнопки в зависимости от статуса -->
          <template v-if="isAdmin">
            <router-link
              class="btn btn-outline-danger me-2"
              to="/admin"
            >
              🔧 Админ
            </router-link>
            <button
              class="btn btn-outline-warning"
              @click="logout"
            >
              🚪 Выход
            </button>
          </template>
          
          <router-link
            v-else
            class="btn btn-outline-success"
            to="/login"
          >
            🔐 Вход
          </router-link>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  data() {
    return {
      isAdmin: false
    }
  },
  mounted() {
    this.checkAdminStatus()
    // Следим за изменениями в localStorage
    window.addEventListener('storage', this.checkAdminStatus)
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.checkAdminStatus)
  },
  methods: {
    checkAdminStatus() {
      this.isAdmin = localStorage.getItem('isAdmin') === 'true'
    },
    logout() {
      localStorage.removeItem('isAdmin')
      localStorage.removeItem('adminLogin')
      this.isAdmin = false
      this.$router.push('/')
    }
  }
}
</script>
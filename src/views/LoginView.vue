<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow">
          <div class="card-header bg-primary text-white text-center">
            <h4>🔐 Вход в админ-панель</h4>
          </div>
          <div class="card-body">
            <div v-if="error" class="alert alert-danger">{{ error }}</div>
            
            <form @submit.prevent="login">
              <div class="mb-3">
                <label class="form-label">Логин</label>
                <input 
                  type="text" 
                  class="form-control" 
                  v-model="form.login" 
                  placeholder="Введите логин"
                  required
                >
              </div>
              
              <div class="mb-3">
                <label class="form-label">Пароль</label>
                <input 
                  type="password" 
                  class="form-control" 
                  v-model="form.password" 
                  placeholder="Введите пароль"
                  required
                >
              </div>
              
              <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                {{ loading ? 'Вход...' : 'Войти' }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        login: '',
        password: ''
      },
      loading: false,
      error: null
    }
  },
  methods: {
    login() {
      this.loading = true
      this.error = null
      
      // Логин и пароль (можно поменять на свои)
      const adminLogin = 'admin'
      const adminPassword = 'admin123'
      
      setTimeout(() => {
        if (this.form.login === adminLogin && this.form.password === adminPassword) {
          // Сохраняем статус админа
          localStorage.setItem('isAdmin', 'true')
          localStorage.setItem('adminLogin', this.form.login)
          this.$router.push('/admin')
        } else {
          this.error = 'Неверный логин или пароль'
        }
        this.loading = false
      }, 500)
    }
  },
  mounted() {
    // Если уже залогинены, перенаправляем в админку
    if (localStorage.getItem('isAdmin') === 'true') {
      this.$router.push('/admin')
    }
  }
}
</script>
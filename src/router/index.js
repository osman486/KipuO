import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ReservesView from '../views/ReservesView.vue'
import AnimalsView from '../views/AnimalsView.vue'
import ReserveDetailView from '../views/ReserveDetailView.vue'
import AdminView from '../views/AdminView.vue'
import LoginView from '../views/LoginView.vue'

// Функция проверки админа
const isAdmin = () => {
  return localStorage.getItem('isAdmin') === 'true'
}

const routes = [
  { path: '/', component: HomeView },
  { path: '/reserves', component: ReservesView },
  { path: '/reserves/:id', component: ReserveDetailView },
  { path: '/animals', component: AnimalsView },
  { path: '/login', component: LoginView },
  { 
    path: '/admin', 
    component: AdminView,
    beforeEnter: (to, from, next) => {
      if (isAdmin()) {
        next()
      } else {
        next('/login')
      }
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegistrationView from '../views/RegistrationView.vue'
import SignInView from '../views/SignInView.vue'
import LoginHome from '../views/LoginHomeView.vue'
import Section from '../views/SectionView.vue'
import Book from '../views/BookView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/Registration',
      name: 'Registration',
      component: RegistrationView
    },
    {
      path: '/Login',
      name: 'Login',
      component: SignInView
    },
    {
      path: '/LoginHome',
      name: 'LoginHome',
      component: LoginHome,
      meta: { requiresAuth: true } 
    },
    {
      path: '/Section',
      name: 'Section',
      component: Section,
      meta: { requiresAuth: true } 
    },
    {
      path: '/Section/:section_id/Book',
      name: 'Book',
      component: Book,
      props: true, 
      /* meta: { requiresAuth: true }  */
    }
  ]
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('accessToken');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'Login' }); // Redirect to Login view if not authenticated
    } else {
      next(); // Proceed to the route
    }
  } else {
    next(); // Proceed to non-authenticated routes
  }
});

export default router

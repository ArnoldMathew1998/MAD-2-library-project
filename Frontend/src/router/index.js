import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue'
import SignInView from '../views/SignInView.vue'
import SignUpView from '../views/SignUpView.vue'
import LoginHome from '../views/LoginView.vue'
import Section from '../views/SectionView.vue'
import Book from '../views/BookView.vue'
import Product from '../views/ProductView.vue'
import Profile from '../views/ProfileView.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/SignIn',
    name: 'SignIn',
    component: SignInView
  },
  {
    path: '/SignUp',
    name: 'SignUp',
    component: SignUpView
  },
  {
    path: '/Home',
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
    meta: { requiresAuth: true } 
  },
  {
    path: '/Book/:book_id/Product',
    name: 'Product',
    component: Product,
    props: true, 
    meta: { requiresAuth: true } 
  },
  {
    path: '/Profile',
    name: 'Profile',
    component: Profile,
    props: true, 
    meta: { requiresAuth: true } 
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('accessToken');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'SignIn' }); // Redirect to SignIn view if not authenticated
    } else {
      next(); // Proceed to the route
    }
  } else {
    // Clear localStorage if navigating to non-authenticated routes
    localStorage.removeItem('accessToken');
    localStorage.removeItem('isAdmin');
    localStorage.removeItem('user_id');
    next(); // Proceed to non-authenticated routes
  }
});
export default router;

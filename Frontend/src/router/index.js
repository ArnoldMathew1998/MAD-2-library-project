import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import SignInView from '../views/SignInView.vue';
import SignUpView from '../views/SignUpView.vue';
import LoginHome from '../views/LoginView.vue';
import Section from '../views/SectionView.vue';
import Book from '../views/BookView.vue';
import Product from '../views/ProductView.vue';
import Profile from '../views/ProfileView.vue';
import MyBooks from '../views/OrderView.vue';
import Checkout from '../views/BuyView.vue';
import search from '../views/SearchView.vue';
import Dashboard from '@/views/DashboardView.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/SignIn',
    name: 'SignIn',
    component: SignInView,
  },
  {
    path: '/SignUp',
    name: 'SignUp',
    component: SignUpView,
  },
  {
    path: '/Home',
    name: 'LoginHome',
    component: LoginHome,
    meta: { requiresAuth: true },
  },
  {
    path: '/Section',
    name: 'Section',
    component: Section,
    meta: { requiresAuth: true },
  },
  {
    path: '/Section/:section_id/Book',
    name: 'Book',
    component: Book,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/Book/:book_id/Product',
    name: 'Product',
    component: Product,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/Profile',
    name: 'Profile',
    component: Profile,
    props: true,
    meta: { requiresAuth: true },
  },
  {
    path: '/MyBooks',
    name: 'MyBooks',
    component: MyBooks,
    props: true,
    meta: { requiresAuth: true},
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: Checkout,
    props: true,
    meta: { requiresAuth: true, requiresUser: true },
  },
  {
    path: '/search',
    name: 'search',
    component: search,
    props: true,
  },
  {
    path: '/Dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('accessToken');
  const isAdmin = localStorage.getItem('isAdmin') === 'true';

  // Check if the route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'SignIn' }); // Redirect to SignIn view if not authenticated
    } else if (to.matched.some(record => record.meta.requiresAdmin) && !isAdmin) {
      next({ name: 'LoginHome' }); // Redirect to Home if user is not an admin but accessing admin route
    } else if (to.matched.some(record => record.meta.requiresUser) && isAdmin) {
      next({ name: 'LoginHome' }); // Redirect to Home if admin tries to access user route
    } else {
      next(); // Proceed to the route
    }
  } else {
    next(); // Proceed to the route
  }
});

export default router;

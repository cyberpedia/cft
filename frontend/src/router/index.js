# frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ChallengesView from '../views/ChallengesView.vue'
import ChallengeDetailView from '../views/ChallengeDetailView.vue' // New import
import LeaderboardView from '../views/LeaderboardView.vue'
import TeamsView from '../views/TeamsView.vue'

import { useAuthStore } from '@/stores/auth'; // Import the auth store


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true } // Example: Home requires auth
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { requiresAuth: false }
    },
    {
      path: '/challenges',
      name: 'challenges',
      component: ChallengesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/challenges/:id', // New route for challenge detail
      name: 'challenge-detail',
      component: ChallengeDetailView,
      props: true, // Allows component to receive route params as props
      meta: { requiresAuth: true }
    },
    {
      path: '/leaderboard',
      name: 'leaderboard',
      component: LeaderboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/teams',
      name: 'teams',
      component: TeamsView,
      meta: { requiresAuth: true }
    },
    // Add other routes as they are implemented
  ]
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // If the route requires authentication and the user is not logged in, redirect to login
    next({ name: 'login' });
  } else if ((to.name === 'login' || to.name === 'register') && authStore.isAuthenticated) {
    // If the user is logged in and tries to go to login or register, redirect to home
    next({ name: 'home' });
  } else {
    // Otherwise, allow navigation
    next();
  }
});

export default router

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ChallengesView from '../views/ChallengesView.vue'
import ChallengeDetailView from '../views/ChallengeDetailView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'
import TeamsView from '../views/TeamsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guestOnly: true }
    },
    {
      path: '/challenges',
      name: 'challenges',
      component: ChallengesView,
      meta: { requiresAuth: true }
    },
    {
      path: '/challenges/:id',
      name: 'challenge-detail',
      component: ChallengeDetailView,
      props: true, // Pass route params as props to the component
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
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = !!authStore.accessToken;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' });
  } else if (to.meta.guestOnly && isAuthenticated) {
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router

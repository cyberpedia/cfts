import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

// Layouts
import AdminLayout from '../layouts/AdminLayout.vue'

// Public Views
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AuthCallbackView from '../views/AuthCallbackView.vue'

// Authenticated User Views
import ChallengesView from '../views/ChallengesView.vue'
import ChallengeDetailView from '../views/ChallengeDetailView.vue'
import LeaderboardView from '../views/LeaderboardView.vue'
import TeamsView from '../views/TeamsView.vue'
import ProfileView from '../views/ProfileView.vue'
import NotificationsView from '../views/NotificationsView.vue'

// Admin Views
import AdminDashboardView from '../views/admin/AdminDashboardView.vue'
import AdminUserListView from '../views/admin/AdminUserListView.vue'
import AdminUserEditView from '../views/admin/AdminUserEditView.vue'
import AdminChallengeListView from '../views/admin/AdminChallengeListView.vue'
import AdminChallengeEditView from '../views/admin/AdminChallengeEditView.vue'
import AdminSettingsView from '../views/admin/AdminSettingsView.vue'
import AdminWriteupQueueView from '../views/admin/AdminWriteupQueueView.vue'
import AdminAuditLogView from '../views/admin/AdminAuditLogView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/login', name: 'login', component: LoginView, meta: { guestOnly: true } },
    { path: '/register', name: 'register', component: RegisterView, meta: { guestOnly: true } },
    { path: '/auth/callback', name: 'auth-callback', component: AuthCallbackView },
    { path: '/challenges', name: 'challenges', component: ChallengesView, meta: { requiresAuth: true } },
    { path: '/challenges/:id', name: 'challenge-detail', component: ChallengeDetailView, props: true, meta: { requiresAuth: true } },
    { path: '/leaderboard', name: 'leaderboard', component: LeaderboardView, meta: { requiresAuth: true } },
    { path: '/teams', name: 'teams', component: TeamsView, meta: { requiresAuth: true } },
    { path: '/profile', name: 'profile', component: ProfileView, meta: { requiresAuth: true } },
    { path: '/notifications', name: 'notifications', component: NotificationsView, meta: { requiresAuth: true } },
    
    // Admin Routes
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        { path: '', redirect: '/admin/dashboard' },
        { path: 'dashboard', name: 'admin-dashboard', component: AdminDashboardView },
        { path: 'users', name: 'admin-users', component: AdminUserListView },
        { path: 'users/:id/edit', name: 'admin-user-edit', component: AdminUserEditView, props: true },
        { path: 'challenges', name: 'admin-challenges', component: AdminChallengeListView },
        { path: 'challenges/new', name: 'admin-challenge-new', component: AdminChallengeEditView },
        { path: 'challenges/:id/edit', name: 'admin-challenge-edit', component: AdminChallengeEditView, props: true },
        { path: 'settings', name: 'admin-settings', component: AdminSettingsView },
        { path: 'writeups', name: 'admin-writeups', component: AdminWriteupQueueView },
        { path: 'logs', name: 'admin-logs', component: AdminAuditLogView },
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const isAuthenticated = !!authStore.accessToken;
  const isAdmin = authStore.user?.is_staff;

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if (to.meta.requiresAdmin && !isAdmin) {
    next({ name: 'home' }); 
  } else if (to.meta.guestOnly && isAuthenticated) {
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router

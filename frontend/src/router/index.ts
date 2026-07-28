/** Vue Router with auth and permission guards. */

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { getToken } from '@/utils/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/LoginView.vue'),
    meta: { public: true, title: '登录' },
  },
  {
    path: '/',
    component: () => import('@/layouts/AdminLayout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/DashboardView.vue'),
        meta: { title: '仪表盘' },
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/user/UserListView.vue'),
        meta: { title: '用户管理', permission: 'user:list' },
      },
      {
        path: 'roles',
        name: 'Roles',
        component: () => import('@/views/role/RoleListView.vue'),
        meta: { title: '角色管理', permission: 'role:list' },
      },
      {
        path: 'movies',
        name: 'Movies',
        component: () => import('@/views/movie/MovieListView.vue'),
        meta: { title: '电影管理', permission: 'movie:list' },
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/NotFoundView.vue'),
    meta: { public: true, title: '404' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  document.title = `${String(to.meta.title || 'Polaris')} - Polaris Admin`

  if (to.meta.public) {
    return true
  }

  const token = getToken()
  if (!token) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }

  const authStore = useAuthStore()
  if (!authStore.user) {
    try {
      await authStore.fetchProfile()
    } catch {
      await authStore.logout()
      return { path: '/login', query: { redirect: to.fullPath } }
    }
  }

  const permission = to.meta.permission as string | undefined
  if (permission && !authStore.hasPermission(permission)) {
    return { path: '/dashboard' }
  }

  return true
})

export default router

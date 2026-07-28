/** Auth Pinia store: login state, permissions, logout. */

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { getMeApi, loginApi, logoutApi } from '@/api/auth'
import type { UserBrief } from '@/types'
import { clearToken, getToken, setToken } from '@/utils/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(getToken())
  const user = ref<UserBrief | null>(null)

  const isAuthenticated = computed(() => Boolean(token.value))
  const permissions = computed(() => user.value?.permissions ?? [])
  const roles = computed(() => user.value?.roles ?? [])
  const displayName = computed(
    () => user.value?.full_name || user.value?.username || 'User',
  )

  function hasPermission(code: string | string[]): boolean {
    if (user.value?.is_superuser) return true
    const owned = new Set(permissions.value)
    const codes = Array.isArray(code) ? code : [code]
    return codes.every((item) => owned.has(item))
  }

  function hasAnyPermission(codes: string[]): boolean {
    if (user.value?.is_superuser) return true
    const owned = new Set(permissions.value)
    return codes.some((item) => owned.has(item))
  }

  async function login(username: string, password: string) {
    const result = await loginApi(username, password)
    token.value = result.access_token
    user.value = result.user
    setToken(result.access_token)
  }

  async function fetchProfile() {
    if (!token.value) return
    user.value = await getMeApi()
  }

  async function logout() {
    try {
      if (token.value) {
        await logoutApi()
      }
    } finally {
      token.value = null
      user.value = null
      clearToken()
    }
  }

  return {
    token,
    user,
    isAuthenticated,
    permissions,
    roles,
    displayName,
    hasPermission,
    hasAnyPermission,
    login,
    fetchProfile,
    logout,
  }
})
